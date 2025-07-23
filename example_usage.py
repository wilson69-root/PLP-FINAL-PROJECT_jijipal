#!/usr/bin/env python3
"""
Example usage of the Mtaa Agent Project scaffolded structure.
Demonstrates how to use the AgentTaskRunner and related components.
"""

from agent.agent_runner import AgentTaskRunner
from models.hf_model import ask_model, check_model_status
from agent.cache import get_cache_stats, clear_cache
import json

def main():
    """Main example function demonstrating the agent usage."""
    
    print("🧭 Mtaa Agent Project - Example Usage")
    print("=" * 50)
    
    # Configuration
    city = "Nairobi"
    budget = 50000  # KES
    goal = "Survive"
    
    print(f"\n📍 City: {city}")
    print(f"💰 Budget: KES {budget:,}")
    print(f"🎯 Goal: {goal}")
    
    # Check model status
    print("\n🤖 Checking AI Model Status...")
    model_status = check_model_status()
    print(f"Model loaded: {model_status.get('model_loaded', False)}")
    print(f"Model ready: {model_status.get('ready', False)}")
    
    # Initialize agent runner
    print("\n🚀 Initializing Agent Runner...")
    runner = AgentTaskRunner(city, budget, goal)
    
    # Example 1: Get individual data types
    print("\n📊 Example 1: Getting Individual Data")
    print("-" * 30)
    
    print("🏠 Getting rental information...")
    rentals = runner.get_rentals()
    print(f"Found {len(rentals)} rental options:")
    for i, rental in enumerate(rentals[:3], 1):
        print(f"  {i}. {rental}")
    
    print("\n🍽️ Getting food options...")
    food_options = runner.get_food()
    print(f"Found {len(food_options)} food options:")
    for i, food in enumerate(food_options[:3], 1):
        print(f"  {i}. {food}")
    
    # Example 2: Run all tasks
    print("\n📋 Example 2: Running All Tasks")
    print("-" * 30)
    
    print("⏳ Running comprehensive analysis...")
    results = runner.run_all_tasks()
    
    if "error" not in results:
        metadata = results.get('metadata', {})
        print(f"✅ Analysis completed in {metadata.get('execution_time', 0):.2f} seconds")
        
        print(f"\n📊 Results Summary:")
        print(f"  • Rentals: {len(results.get('rentals', []))}")
        print(f"  • Food options: {len(results.get('food', []))}")
        print(f"  • Chill spots: {len(results.get('chill_spots', []))}")
        print(f"  • Transport info: {len(results.get('transport', []))}")
        
        print(f"\n📅 Itinerary preview:")
        itinerary = results.get('itinerary', 'No itinerary generated')
        if isinstance(itinerary, dict) and 'days' in itinerary:
            print(f"  Generated {len(itinerary['days'])} day(s) itinerary")
            print(f"  Daily budget: KES {itinerary.get('daily_budget', 0):,.0f}")
        else:
            print(f"  {str(itinerary)[:100]}...")
    else:
        print(f"❌ Error: {results['error']}")
    
    # Example 3: Budget breakdown
    print("\n💰 Example 3: Budget Analysis")
    print("-" * 30)
    
    budget_breakdown = runner.get_budget_breakdown()
    print(f"Budget feasibility: {budget_breakdown.get('budget_feasibility')}")
    
    expenses = budget_breakdown.get('estimated_expenses', {})
    print("Estimated monthly expenses:")
    for category, amount in expenses.items():
        percentage = (amount / budget * 100) if budget > 0 else 0
        print(f"  • {category.title()}: KES {amount:,} ({percentage:.1f}%)")
    
    # Example 4: Survival tips
    print("\n🛡️ Example 4: Survival Tips")
    print("-" * 30)
    
    survival_tips = runner.get_survival_tips()
    print("Top survival tips:")
    for i, tip in enumerate(survival_tips[:5], 1):
        print(f"  {i}. {tip}")
    
    # Example 5: AI interaction
    print("\n🤖 Example 5: AI Model Interaction")
    print("-" * 30)
    
    try:
        prompt = f"Give me 3 quick tips for surviving in {city} with KES {budget}"
        print(f"Prompt: {prompt}")
        
        ai_response = ask_model(prompt, max_new_tokens=150)
        print(f"AI Response: {ai_response}")
        
    except Exception as e:
        print(f"AI interaction failed: {e}")
        print("Note: Make sure transformers library is installed and model is available")
    
    # Example 6: Cache information
    print("\n💾 Example 6: Cache Statistics")
    print("-" * 30)
    
    cache_stats = get_cache_stats()
    print(f"Cache entries: {cache_stats.get('total_entries', 0)}")
    print(f"Cache size: {cache_stats.get('cache_size_bytes', 0)} bytes")
    print(f"Cache directory: {cache_stats.get('cache_directory', 'Unknown')}")
    
    # Example 7: Summary report
    print("\n📋 Example 7: Summary Report")
    print("-" * 30)
    
    summary = runner.get_summary_report()
    print(f"City: {summary['city']}")
    print(f"Budget: KES {summary['budget']:,}")
    print(f"Goal: {summary['goal']}")
    
    data_summary = summary.get('data_summary', {})
    print("Data found:")
    for key, value in data_summary.items():
        print(f"  • {key.replace('_', ' ').title()}: {value}")
    
    print("\n✨ Example completed successfully!")
    print("\n💡 Next steps:")
    print("  1. Run the Streamlit app: streamlit run main.py")
    print("  2. Customize scrapers in agent/scraper.py for real data sources")
    print("  3. Configure the HuggingFace model in models/hf_model.py")
    print("  4. Add more UI components in ui/components.py")


def demo_individual_components():
    """Demonstrate individual component usage."""
    
    print("\n🔧 Individual Component Demo")
    print("=" * 40)
    
    # Cache demo
    from agent.cache import cache_data, get_cached_data, cache_exists
    
    print("💾 Cache Demo:")
    cache_data("test_key", {"demo": "data"}, ttl=60)
    cached = get_cached_data("test_key")
    print(f"  Cached and retrieved: {cached}")
    print(f"  Cache exists: {cache_exists('test_key')}")
    
    # Scraper demo
    from agent.scraper import scrape_rentals, scrape_food
    
    print("\n🕷️ Scraper Demo:")
    demo_rentals = scrape_rentals("Nairobi")
    print(f"  Sample rentals: {demo_rentals[:2]}")
    
    # Prompt template demo
    from agent.prompt_templates import format_chat_prompt
    
    print("\n💬 Prompt Template Demo:")
    prompt = format_chat_prompt(
        user_input="Where should I live?",
        personality="Practical",
        city="Nairobi",
        goal="Survive", 
        budget=30000
    )
    print(f"  Generated prompt length: {len(prompt)} characters")
    
    # Itinerary demo
    from agent.itinerary import generate_quick_itinerary
    
    print("\n📅 Itinerary Demo:")
    quick_itinerary = generate_quick_itinerary("Nairobi", 30000)
    print(f"  Quick itinerary type: {quick_itinerary['type']}")
    print(f"  Recommendations: {len(quick_itinerary['recommendations'])}")


if __name__ == "__main__":
    try:
        main()
        demo_individual_components()
        
    except KeyboardInterrupt:
        print("\n\n👋 Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running example: {e}")
        print("\n💡 Make sure all dependencies are installed:")
        print("  pip install -r requirements.txt")