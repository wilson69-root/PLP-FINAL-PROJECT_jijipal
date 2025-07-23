"""
Itinerary generation logic for the Mtaa Agent Project.
Creates personalized itineraries based on user goals, budget, and scraped data.
"""

from models.hf_model import ask_model
from agent.prompt_templates import format_itinerary_prompt
from agent.cache import cache_data, get_cached_data
import random
import logging

logger = logging.getLogger(__name__)


def generate_itinerary(city, budget, goal="Survive", duration=7, preferences=None, data=None):
    """
    Generate a comprehensive itinerary based on user parameters and available data.
    
    Args:
        city: Target city
        budget: Total budget in KES
        goal: User goal (Survive, Explore, Relocate)
        duration: Number of days for the itinerary
        preferences: User preferences (optional)
        data: Dictionary containing scraped data
    
    Returns:
        Generated itinerary as string or dictionary
    """
    logger.info(f"Generating {duration}-day itinerary for {city}, budget: KES {budget}")
    
    # Check cache first
    cache_key = f"itinerary_{city.lower()}_{budget}_{goal}_{duration}"
    cached_itinerary = get_cached_data(cache_key)
    
    if cached_itinerary:
        logger.info("Returning cached itinerary")
        return cached_itinerary
    
    # Prepare data
    if data is None:
        data = {}
    
    if preferences is None:
        preferences = _get_default_preferences(goal)
    
    try:
        # Generate using AI model
        itinerary = _generate_ai_itinerary(city, budget, goal, duration, preferences, data)
        
        # Cache the result
        cache_data(cache_key, itinerary, ttl=3600*12)  # Cache for 12 hours
        
        logger.info("Successfully generated and cached itinerary")
        return itinerary
        
    except Exception as e:
        logger.error(f"Error generating AI itinerary: {e}")
        # Fallback to template-based generation
        return _generate_template_itinerary(city, budget, goal, duration, data)


def _generate_ai_itinerary(city, budget, goal, duration, preferences, data):
    """Generate itinerary using HuggingFace model."""
    prompt = format_itinerary_prompt(
        city=city,
        budget=budget,
        goal=goal,
        duration=duration,
        preferences=preferences,
        data=data
    )
    
    response = ask_model(prompt)
    return response


def _generate_template_itinerary(city, budget, goal, duration, data):
    """Fallback template-based itinerary generation."""
    logger.info("Using template-based itinerary generation")
    
    daily_budget = budget / duration
    
    itinerary = {
        "city": city,
        "total_budget": budget,
        "daily_budget": daily_budget,
        "goal": goal,
        "duration": duration,
        "days": []
    }
    
    for day in range(1, duration + 1):
        day_plan = _generate_day_plan(day, city, daily_budget, goal, data)
        itinerary["days"].append(day_plan)
    
    return itinerary


def _generate_day_plan(day_number, city, daily_budget, goal, data):
    """Generate a plan for a specific day."""
    
    # Base structure for a day
    day_plan = {
        "day": day_number,
        "budget": daily_budget,
        "activities": [],
        "estimated_cost": 0,
        "notes": []
    }
    
    if goal == "Survive":
        day_plan = _add_survival_activities(day_plan, city, data)
    elif goal == "Explore":
        day_plan = _add_exploration_activities(day_plan, city, data)
    elif goal == "Relocate":
        day_plan = _add_relocation_activities(day_plan, city, data, day_number)
    
    return day_plan


def _add_survival_activities(day_plan, city, data):
    """Add survival-focused activities to a day."""
    
    if day_plan["day"] == 1:
        # First day - essentials
        day_plan["activities"].extend([
            {
                "time": "Morning (8-10 AM)",
                "activity": "Find temporary accommodation",
                "location": "Central area of " + city,
                "cost": 1000,
                "description": "Secure a place to stay while you look for permanent housing"
            },
            {
                "time": "Mid-morning (10-12 PM)",
                "activity": "Register phone number and get local SIM",
                "location": "Mobile provider shop",
                "cost": 200,
                "description": "Essential for communication and mobile money"
            },
            {
                "time": "Afternoon (2-4 PM)",
                "activity": "Find nearest supermarket and market",
                "location": "Local markets",
                "cost": 500,
                "description": "Buy essential supplies and groceries"
            }
        ])
    else:
        # Regular survival activities
        day_plan["activities"].extend([
            {
                "time": "Morning",
                "activity": "Job hunting or networking",
                "location": city + " business district",
                "cost": 200,
                "description": "Look for employment opportunities"
            },
            {
                "time": "Afternoon",
                "activity": "Explore local resources",
                "location": "Community centers",
                "cost": 100,
                "description": "Find local support networks and resources"
            }
        ])
    
    _add_food_recommendations(day_plan, data.get('food', []))
    _add_transport_info(day_plan, data.get('transport', []))
    
    return day_plan


def _add_exploration_activities(day_plan, city, data):
    """Add exploration-focused activities to a day."""
    
    places = data.get('chill_spots', [])
    
    if places:
        selected_places = random.sample(places, min(2, len(places)))
        for i, place in enumerate(selected_places):
            day_plan["activities"].append({
                "time": "Morning" if i == 0 else "Afternoon",
                "activity": f"Visit {place}",
                "location": place,
                "cost": random.randint(300, 800),
                "description": f"Explore and enjoy {place}"
            })
    
    _add_food_recommendations(day_plan, data.get('food', []))
    return day_plan


def _add_relocation_activities(day_plan, city, data, day_number):
    """Add relocation-focused activities to a day."""
    
    if day_number <= 3:
        # First few days - house hunting
        day_plan["activities"].extend([
            {
                "time": "Morning",
                "activity": "House hunting",
                "location": f"Various neighborhoods in {city}",
                "cost": 500,
                "description": "Visit potential rental properties"
            },
            {
                "time": "Afternoon",
                "activity": "Neighborhood exploration",
                "location": "Target neighborhoods",
                "cost": 300,
                "description": "Assess safety, amenities, and transport links"
            }
        ])
    else:
        # Later days - settling in
        day_plan["activities"].extend([
            {
                "time": "Morning",
                "activity": "Set up utilities and services",
                "location": "Service provider offices",
                "cost": 200,
                "description": "Internet, electricity, water connections"
            },
            {
                "time": "Afternoon",
                "activity": "Explore local amenities",
                "location": "Near your new home",
                "cost": 400,
                "description": "Find nearby shops, healthcare, and services"
            }
        ])
    
    return day_plan


def _add_food_recommendations(day_plan, food_data):
    """Add food recommendations to a day plan."""
    if food_data:
        selected_food = random.choice(food_data)
        day_plan["activities"].append({
            "time": "Lunch",
            "activity": "Meal",
            "location": selected_food,
            "cost": random.randint(150, 500),
            "description": f"Enjoy local cuisine at {selected_food}"
        })


def _add_transport_info(day_plan, transport_data):
    """Add transport information to day plan notes."""
    if transport_data:
        transport_tip = random.choice(transport_data)
        day_plan["notes"].append(f"💡 Transport tip: {transport_tip}")


def _get_default_preferences(goal):
    """Get default preferences based on user goal."""
    preferences_map = {
        "Survive": "budget-friendly, essential services, safe areas, practical",
        "Explore": "cultural sites, entertainment, local experiences, variety",
        "Relocate": "residential areas, long-term amenities, practical setup, community"
    }
    
    return preferences_map.get(goal, "balanced, practical, local")


def generate_quick_itinerary(city, budget, duration=3):
    """Generate a quick 3-day itinerary for immediate use."""
    return {
        "type": "quick_itinerary",
        "city": city,
        "budget": budget,
        "duration": duration,
        "recommendations": [
            f"Day 1: Secure accommodation and essential services in {city}",
            f"Day 2: Explore local markets and transport routes",
            f"Day 3: Network and find local communities",
            f"Budget allocation: KES {budget//3} per day",
            f"Priority: Safety, basic needs, orientation"
        ]
    }


def generate_budget_optimized_itinerary(city, budget, data):
    """Generate an itinerary optimized for the given budget."""
    
    # Calculate budget allocation
    accommodation_budget = budget * 0.4  # 40% for accommodation
    food_budget = budget * 0.3  # 30% for food
    transport_budget = budget * 0.15  # 15% for transport
    activities_budget = budget * 0.15  # 15% for activities
    
    recommendations = [
        f"🏠 Accommodation budget: KES {accommodation_budget:,.0f}",
        f"🍽️ Food budget: KES {food_budget:,.0f}",
        f"🚌 Transport budget: KES {transport_budget:,.0f}",
        f"🎯 Activities budget: KES {activities_budget:,.0f}"
    ]
    
    # Add specific recommendations based on available data
    rentals = data.get('rentals', [])
    if rentals:
        affordable_rentals = [r for r in rentals if 'Within budget' in r or not 'Above' in r]
        if affordable_rentals:
            recommendations.append(f"🏡 Recommended: {affordable_rentals[0]}")
    
    food_options = data.get('food', [])
    if food_options:
        budget_food = random.choice(food_options)
        recommendations.append(f"🍽️ Try: {budget_food}")
    
    return {
        "type": "budget_optimized",
        "city": city,
        "total_budget": budget,
        "allocations": {
            "accommodation": accommodation_budget,
            "food": food_budget,
            "transport": transport_budget,
            "activities": activities_budget
        },
        "recommendations": recommendations
    }


def generate_emergency_itinerary(city, budget):
    """Generate an emergency survival itinerary for immediate needs."""
    return {
        "type": "emergency",
        "city": city,
        "budget": budget,
        "immediate_actions": [
            "🆘 Find immediate shelter (hostels, budget hotels, friends)",
            "📱 Get local SIM card and mobile money setup",
            "🏥 Locate nearest hospital and police station",
            "🍞 Find 24-hour shops and emergency food sources",
            "🚌 Learn basic transport routes to essential services",
            "💰 Find ATMs and banking services",
            "📍 Download offline maps of the area"
        ],
        "emergency_contacts": [
            "Emergency: 999 or 112",
            "Police: 999",
            "Medical emergency: 999",
            f"Local {city} emergency services: Contact local authorities"
        ],
        "budget_priority": "Focus on shelter, food, communication, and safety first"
    }