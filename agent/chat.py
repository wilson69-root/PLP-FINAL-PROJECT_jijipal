import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def chat_response(user_input, personality, context_city, context_goal, context_budget, strict_mode=False):
    tone = {
        "💡 Practical": "Give direct, useful responses focused on safety, budgeting, and local navigation. Avoid slang.",
        "😊 Friendly": "Be warm, polite, and helpful like a friendly guide. Keep it accurate.",
        "🧘 Calm": "Speak gently, offer thoughtful advice, and stay clear and relaxing."
    }.get(personality, "Be helpful and factual.")

    base_prompt = f"""
    You are MtaaBot, an AI assistant helping Kenyans relocate and navigate urban life.
    Context:
    - City: {context_city}
    - Goal: {context_goal}
    - Daily Budget: KES {context_budget}

    User asked: "{user_input}"

    Style: {tone}

    Respond clearly in English with no hallucinated places, fake slang, or invented names. Use 1–3 concise bullet points.
    """

    if strict_mode:
        base_prompt += "\nStay strictly factual. If unsure, say you don't know. Avoid exaggeration or random creativity."

    try:
        response = groq_client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": base_prompt}],
            temperature=0.4 if strict_mode else 0.7,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ MtaaBot encountered an error: {e}"
