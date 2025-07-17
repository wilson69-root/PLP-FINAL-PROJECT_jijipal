from agent.scrapers import scrape_numbeo_specific

def get_dynamic_tips(city: str, budget: int, goal: str) -> list[str]:
    """
    Returns additional survival tips based on budget and intention.

    Args:
        city (str): City name
        budget (int): Daily survival budget
        goal (str): 'Survive and save' or 'Explore and enjoy'

    Returns:
        List[str]: Budget-based or goal-based tips
    """
    tips = []

    # Get real price data
    price_data = scrape_numbeo_specific(city)
    if isinstance(price_data, dict):
        for category, items in price_data.items():
            tips.extend(items)
    
    # Budget-based logic
    if budget <= 500:
        tips.append("💸 You're on a tight budget. Stick to local eateries (vibandas) for meals under KES 150.")
        tips.append("📱 Consider using *444# bundles (Safaricom daily plans) to save on airtime/data.")
        tips.append("🚶 Walk where possible or use short-distance matatus instead of bodabodas.")
    elif budget <= 1000:
        tips.append("🧺 Mix affordable eateries and street vendors to stay under budget.")
        tips.append("🚗 Use shared taxis or city ride apps like Wasili or Little where available.")
    else:
        tips.append("🎉 You can explore mid-range restaurants, co-working cafes, and malls comfortably.")
        tips.append("🛵 Use bodabodas for faster movement — negotiate fare before boarding.")

    # Intention-based logic
    if goal == "Survive and save":
        tips.append("💡 Track your daily spend using free apps like M-PESA Tracker or Expensure.")
        tips.append("🔒 Avoid late-night movement unless you're in a group.")
        tips.append("🧺 Shop from open markets in the mornings for better deals.")
    else:
        tips.append("📷 Check out tourist-friendly zones like museums or street food hubs.")
        tips.append("🕹️ Explore gaming cafés, art galleries, or co-working spaces for experiences.")
        tips.append("🌅 Always ask locals about hidden gems that aren't on Google.")

    return tips
