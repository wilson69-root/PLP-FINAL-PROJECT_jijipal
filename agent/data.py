def get_static_tips(city: str) -> list[str]:
    """
    Returns static survival tips based on city.
    These are reliable common-sense or local insights.

    Args:
        city (str): City name

    Returns:
        List[str]: Tips for the city
    """
    tips = {
        "nairobi": [
            "Avoid walking with visible electronics in downtown Nairobi.",
            "Use BebaPay or Google Maps for public matatu routes.",
            "Water from taps may be unreliable — buy bottled water for safety.",
            "Local eateries in CBD like 'Highway Inn' offer meals under KES 150.",
            "Mpesa agents charge less near bus stations like Kencom and Railways.",
        ],
        "kisumu": [
            "Dunga Beach offers affordable fish meals for under KES 300.",
            "Use tuk-tuks or matatus; average fare within town is KES 30–50.",
            "Stay hydrated — lakeside humidity is high especially in the afternoon.",
            "Avoid walking near the lakefront after dark unless in a group.",
        ],
        "eldoret": [
            "Best affordable eateries are near Moi University campus.",
            "Matatus between estates cost about KES 40–60.",
            "Use local bodabodas only during daylight — wear a helmet if provided.",
            "Markets like Munyaka offer cheap fruits and daily items.",
        ],
        "mombasa": [
            "Tap water often needs boiling — bottled water is safer.",
            "Use matatus or tuk-tuks for inner city transport — KES 30–70 average.",
            "Swahili dishes like biryani and pilau can be found for KES 100–250 at local vibandas.",
            "Avoid carrying handbags or large backpacks near Likoni Ferry.",
        ],
    }

    return tips.get(city.lower(), ["No tips available for this city yet."])
