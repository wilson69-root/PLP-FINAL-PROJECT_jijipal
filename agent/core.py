from agent.tips import get_dynamic_tips
from agent.data import get_static_tips
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_city_guide(city: str, budget: int, goal: str) -> list[str]:
    """
    Combines static survival tips and dynamic city insights
    to help users thrive in the new city.

    Args:
        city (str): The city name (e.g., 'Nairobi')
        budget (int): Daily survival budget in KES
        goal (str): 'Survive and save' or 'Explore and enjoy'

    Returns:
        List[str]: Survival guide tips
    """
    static_tips = get_static_tips(city)
    dynamic_tips = get_dynamic_tips(city, budget, goal)

    return static_tips + dynamic_tips

def get_ai_summary(city: str, budget: int, goal: str) -> str:
    """Generate an AI summary of how to thrive in the city."""
    prompt = f"You are MtaaBot — a friendly, helpful assistant for newcomers in {city}.\n" \
            f"Summarize how someone can thrive in {city} with KES {budget} budget, " \
            f"especially if they want to '{goal}'. Respond in 2-3 bullet points."
    
    try:
        response = client.chat.completions.create(
            model="mistral-saba-24b",  # Current recommended Groq model
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ AI Summary failed: {e}"

