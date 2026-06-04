import os
import sys
from apscheduler.schedulers.background import BackgroundScheduler
from db.models import SessionLocal, NBGeneratedPost

# Ensure the backend directory is in the system path for seamless relative imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.researcher import AutoResearcherAgent
from agents.generator import StyleGeneratorAgent

def run_auto_content_pipeline():
    """
    The main execution pipeline. It orchestrates the flow of data
    from raw web research into fully stylized LinkedIn posts.
    """
    print("\n [PIPELINE] Starting automated research and generation cycle...")
    
    # Initialize both agents
    researcher = AutoResearcherAgent()
    generator = StyleGeneratorAgent()
    
    # 1. Gather fresh trending topics from the web
    research_data = researcher.execute_auto_research()
    
    if not research_data:
        print(" [PIPELINE] No trending topics found. Aborting generation step.")
        return

    # 2. Iterate over each discovered article and pass it to the Nikit Style LLM
    for item in research_data:
        try:
            print(f"\n [PIPELINE] Processing Topic: '{item['topic_title']}'")
            
            post_package = generator.generate_post(
                topic=item["topic_title"], 
                research_context=item["scraped_context"]
            )
            
            # --- NEW DATABASE SAVE LOGIC ---
            db_session = SessionLocal()
            new_post = NBGeneratedPost(
                topic_title=item["topic_title"],
                source_url=item["source_url"],
                # Grab just the first line as the hook for easy dashboard viewing
                hook=post_package.linkedin_post_text.splitlines()[0] if post_package.linkedin_post_text else "No hook generated",
                full_post_body=post_package.linkedin_post_text,
                image_concept=post_package.image_prompt_idea
            )
            
            db_session.add(new_post)
            db_session.commit()
            db_session.close()
            # -------------------------------
            
            print(f" [PIPELINE] Successfully generated and SAVED asset package to database!")
            
        except Exception as e:
            print(f" [PIPELINE] Generation failed for topic '{item['topic_title']}': {e}")
            continue
    print("\n [PIPELINE] Content automation cycle finished.")


def start_scheduler():
    """
    Starts the background cron process to run the pipeline automatically.
    """
    scheduler = BackgroundScheduler()
    
    # Example: Configured to fire automatically every single day at 9:00 AM
    scheduler.add_job(run_auto_content_pipeline, 'cron', hour=9, minute=0)
    
    scheduler.start()
    print(" [SCHEDULER] Background daemon active. Monitoring schedule (Daily at 9:00 AM).")


# Local testing block to run the joint pipeline manually
if __name__ == "__main__":
    # Ensure you have your OPENAI_API_KEY exported in your environment before running this test
    run_auto_content_pipeline()