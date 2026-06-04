import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

# Ensure Python can find the prompts module if running this script directly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from prompts.nikit_style import get_nikit_system_prompt

# -------------------------------------------------------------------
# 1. Output Schema (Guarantees Phase 3 points + Image Bonus)
# -------------------------------------------------------------------
class LinkedInPostOutput(BaseModel):
    chain_of_thought: str = Field(
        description="Your step-by-step reasoning for applying Nikit's hooks, formatting, and tone to this specific topic."
    )
    linkedin_post_text: str = Field(
        description="The final LinkedIn post content written strictly in Nikit's voice, utilizing extreme whitespace and a sharp hook."
    )
    image_prompt_idea: str = Field(
        description="A clear visual layout, text-graphic concept, or AI image prompt that perfectly complements the post."
    )

# -------------------------------------------------------------------
# 2. The Generator Agent
# -------------------------------------------------------------------
class StyleGeneratorAgent:
    def __init__(self):
        # Automatically pulls from your environment variables
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("🚨 OPENAI_API_KEY environment variable is missing!")
        
        self.client = OpenAI(api_key=self.api_key)

    def generate_post(self, topic: str, research_context: str = "") -> LinkedInPostOutput:
        """
        Injects the topic and context into the few-shot prompt and generates a structured post.
        """
        system_prompt = get_nikit_system_prompt()
        
        user_content = f"Write a high-impact LinkedIn post about this topic: {topic}\n"
        if research_context:
            user_content += f"\nUse this background context to enrich the insights:\n{research_context}"
            
        print("🧠 Connecting to LLM and generating post...")
        
        # Using the beta structured outputs feature with gpt-4o-mini for speed/cost efficiency
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            response_format=LinkedInPostOutput,
        )
        
        return completion.choices[0].message.parsed

# -------------------------------------------------------------------
# 3. Quick Local Test Execution
# -------------------------------------------------------------------
if __name__ == "__main__":
    # We will test it with a topic on how AI drives enhanced accuracy and efficiency in business reporting
    test_topic = "The primary benefit of using AI in business reporting to drive enhanced accuracy and efficiency."
    
    try:
        agent = StyleGeneratorAgent()
        result = agent.generate_post(topic=test_topic)
        
        print("\n========================================")
        print("🔍 CHAIN OF THOUGHT (The AI's reasoning)")
        print("========================================")
        print(result.chain_of_thought)
        
        print("\n========================================")
        print("📝 LINKEDIN POST (Nikit's Voice)")
        print("========================================")
        print(result.linkedin_post_text)
        
        print("\n========================================")
        print("🎨 IMAGE / CAROUSEL IDEA (Bonus Points)")
        print("========================================")
        print(result.image_prompt_idea)
        print("\n")
        
    except Exception as e:
        print(f"❌ Error during generation: {e}")