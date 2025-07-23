"""
Prompt templates for HuggingFace model interactions.
All AI prompts and templates are defined here.
"""

# Base system prompt for the Mtaa Agent
SYSTEM_PROMPT = """
You are MtaaBot, a helpful AI assistant specialized in helping people survive, explore, and relocate in Kenyan cities. 
You provide practical, local, and culturally relevant advice for daily life in Kenya.

Your personality is: {personality}
Current context:
- City: {city}
- User Goal: {goal}
- Budget: KES {budget}

Always provide specific, actionable advice that considers the local Kenyan context, culture, and economic realities.
"""

# Chat response template
CHAT_TEMPLATE = """
{system_prompt}

Previous conversation:
{conversation_history}

User question: {user_input}

Please provide a helpful response that is:
1. Practical and actionable
2. Culturally relevant to Kenya
3. Budget-conscious (considering their KES {budget} budget)
4. Specific to {city} when applicable

Response:"""

# Itinerary generation template
ITINERARY_TEMPLATE = """
Create a detailed daily itinerary for someone in {city}, Kenya with a budget of KES {budget}.

User goal: {goal}
Duration: {duration} days
Preferences: {preferences}

Available data:
- Rentals: {rentals}
- Food options: {food}
- Places to visit: {places}
- Transport options: {transport}

Please create a day-by-day itinerary that:
1. Fits within the KES {budget} budget
2. Includes specific places and activities
3. Considers realistic transport costs and time
4. Incorporates local Kenyan culture and experiences
5. Provides practical tips for each day

Format as a clear day-by-day breakdown with costs and practical advice.

Itinerary:"""

# Survival guide template
SURVIVAL_GUIDE_TEMPLATE = """
Generate a comprehensive survival guide for {city}, Kenya.

User details:
- Goal: {goal}
- Budget: KES {budget} per month
- Duration: {duration}

City data available:
- Housing options: {rentals}
- Food venues: {food}
- Transport costs: {transport}
- Local places: {places}

Create a practical survival guide that includes:
1. Essential first steps upon arrival
2. Budget breakdown and money-saving tips
3. Housing recommendations within budget
4. Food and dining strategies
5. Transportation tips
6. Safety and cultural considerations
7. Local resources and contacts
8. Emergency information

Make it specific to {city} and practical for someone with KES {budget} budget.

Survival Guide:"""

# Budget analysis template
BUDGET_ANALYSIS_TEMPLATE = """
Analyze the budget requirements for living in {city}, Kenya.

Available data:
- Rental costs: {rentals}
- Food costs: {food}
- Transport costs: {transport}
- User budget: KES {budget}

Provide a detailed budget breakdown showing:
1. Essential monthly expenses (rent, food, transport)
2. Recommended allocations
3. Money-saving strategies specific to {city}
4. Whether the budget is realistic
5. Suggestions for budget adjustments

Budget Analysis:"""

# Local tips template
LOCAL_TIPS_TEMPLATE = """
Provide specific local tips and insider knowledge for {city}, Kenya.

Focus areas:
{focus_areas}

User context:
- Goal: {goal}
- Budget: KES {budget}

Provide practical, local insights that only someone familiar with {city} would know:
1. Hidden gems and local favorites
2. Cost-saving strategies locals use
3. Cultural do's and don'ts
4. Best times/places for various activities
5. Local language phrases that help
6. Safety tips specific to {city}
7. Seasonal considerations

Local Tips:"""

# Place recommendation template
PLACE_RECOMMENDATION_TEMPLATE = """
Recommend specific places in {city}, Kenya based on the user's needs.

User preferences:
- Type: {place_type}
- Budget range: KES {budget_range}
- Goal: {goal}
- Mood: {mood}

Available places data: {places_data}

Provide 5-7 specific recommendations with:
1. Name and location
2. Why it's good for their goal/mood
3. Approximate costs
4. Best times to visit
5. How to get there
6. Insider tips

Recommendations:"""

# Emergency help template
EMERGENCY_TEMPLATE = """
The user needs emergency assistance in {city}, Kenya.

Emergency type: {emergency_type}
User location context: {location_context}

Provide immediate, actionable help:
1. Emergency contacts specific to {city}
2. Nearest facilities (hospitals, police, etc.)
3. Step-by-step instructions
4. Important local context
5. Language phrases if helpful

This is urgent - be direct and practical.

Emergency Response:"""


def format_chat_prompt(user_input, personality, city, goal, budget, conversation_history=""):
    """Format a chat prompt for the HuggingFace model."""
    system_prompt = SYSTEM_PROMPT.format(
        personality=personality,
        city=city,
        goal=goal,
        budget=budget
    )
    
    return CHAT_TEMPLATE.format(
        system_prompt=system_prompt,
        conversation_history=conversation_history,
        user_input=user_input,
        budget=budget,
        city=city
    )


def format_itinerary_prompt(city, budget, goal, duration, preferences, data):
    """Format an itinerary generation prompt."""
    return ITINERARY_TEMPLATE.format(
        city=city,
        budget=budget,
        goal=goal,
        duration=duration,
        preferences=preferences,
        rentals=data.get('rentals', []),
        food=data.get('food', []),
        places=data.get('places', []),
        transport=data.get('transport', [])
    )


def format_survival_guide_prompt(city, budget, goal, duration, data):
    """Format a survival guide generation prompt."""
    return SURVIVAL_GUIDE_TEMPLATE.format(
        city=city,
        budget=budget,
        goal=goal,
        duration=duration,
        rentals=data.get('rentals', []),
        food=data.get('food', []),
        transport=data.get('transport', []),
        places=data.get('places', [])
    )


def format_budget_analysis_prompt(city, budget, data):
    """Format a budget analysis prompt."""
    return BUDGET_ANALYSIS_TEMPLATE.format(
        city=city,
        budget=budget,
        rentals=data.get('rentals', []),
        food=data.get('food', []),
        transport=data.get('transport', [])
    )


def format_local_tips_prompt(city, goal, budget, focus_areas):
    """Format a local tips prompt."""
    return LOCAL_TIPS_TEMPLATE.format(
        city=city,
        goal=goal,
        budget=budget,
        focus_areas=", ".join(focus_areas)
    )


def format_place_recommendation_prompt(city, place_type, budget_range, goal, mood, places_data):
    """Format a place recommendation prompt."""
    return PLACE_RECOMMENDATION_TEMPLATE.format(
        city=city,
        place_type=place_type,
        budget_range=budget_range,
        goal=goal,
        mood=mood,
        places_data=places_data
    )


def format_emergency_prompt(city, emergency_type, location_context):
    """Format an emergency assistance prompt."""
    return EMERGENCY_TEMPLATE.format(
        city=city,
        emergency_type=emergency_type,
        location_context=location_context
    )