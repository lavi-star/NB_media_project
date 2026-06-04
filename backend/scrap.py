import json
import os
from apify_client import ApifyClient

# 1. Initialize the Apify client
# Replace with your actual token from the Apify console
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
client = ApifyClient(APIFY_API_TOKEN)

def fetch_nikit_posts():
    print("🚀 Firing up Apify to scrape Nikit's LinkedIn posts...")
    
    # We use a "No Cookies" actor to keep your personal account safe
    actor_id = "apimaestro/linkedin-profile-posts"
    
    # Define the input for the actor
    # Simply provide a LinkedIn profile URL or username [cite: 9]
    run_input = {
        "profile_urls": ["https://www.linkedin.com/in/nikitbassi/"], 
        "total_posts": 5, # Pulling up to 100 posts per page [cite: 9]
    }
    
    print("⏳ Scraping in progress. This may take a minute or two...")
    
    # Run the actor and wait for it to finish
    run = client.actor(actor_id).call(run_input=run_input)
    
    # Fetch the results from the run's default dataset
    print("✅ Scraping complete. Downloading dataset...")
    dataset_items = client.dataset(run.default_dataset_id ).list_items().items
    
    # Extract only the text to keep our JSON clean and LLM context-window friendly
    cleaned_posts = []
    for item in dataset_items:
        # Check if the text field exists in the output [cite: 9]
        if "text" in item and item.get("text"):
            cleaned_posts.append({"text": item["text"]})
            
    # Ensure your target directory exists
    os.makedirs("backend/prompts", exist_ok=True)
    
    # Save the output to your target JSON file
    output_path = "backend/prompts/nikit_posts.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_posts, f, indent=4, ensure_ascii=False)


        
    print(f"🎉 Success! Saved {len(cleaned_posts)} posts to {output_path}")

if __name__ == "__main__":
    fetch_nikit_posts()