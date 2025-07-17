import requests
from bs4 import BeautifulSoup
import json

def scrape_numbeo_specific(city_name):
    """
    Scrapes specific cost of living data from Numbeo.com for a given city.
    
    Args:
        city_name (str): The name of the city (e.g., "Nairobi").
    
    Returns:
        dict: A JSON-compatible dictionary with rent, food, water, and transport data.
        str: An error message if scraping fails.
    """
    # Define the items to extract, mapped to their respective categories
    target_items = {
        "rent": [
            "Apartment (1 bedroom) in City Centre",
            "Apartment (1 bedroom) Outside of Centre"
        ],
        "food": [
            "Meal, Inexpensive Restaurant",
            "Rice (white), (1kg)"
        ],
        "water": [
            "Water (1.5 liter bottle)"
        ],
        "transport": [
            "One-way Ticket (Local Transport)",
            "Monthly Pass (Regular Price)"
        ]
    }
    
    # Convert city name to URL format (replace spaces with hyphens)
    city_url = city_name.replace(" ", "-")
    url = f"https://www.numbeo.com/cost-of-living/in/{city_url}"
    
    # Send a GET request to the URL
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return f"Error: Could not fetch data for {city_name}. Check the city name or try again later."
    
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='data_wide_table')
    
    if not table:
        return "Error: Table not found. The website structure may have changed."
    
    # Initialize the output dictionary
    result = {
        "rent": [],
        "food": [],
        "water": [],
        "transport": []
    }
    
    # Extract data from table rows
    rows = table.find_all('tr')
    for row in rows[1:]:  # Skip header row
        cols = row.find_all('td')
        if len(cols) >= 2:
            item_name = cols[0].text.strip()
            price = cols[1].text.strip().replace("\xa0", " ")  # Handle non-breaking space
            
            # Check each category and item
            for category, items in target_items.items():
                for item in items:
                    if item in item_name:
                        # Format price as ~KES {value}
                        formatted_price = f"{item_name}: ~{price}"
                        result[category].append(formatted_price)
    
    # Validate that all items were found
    for category, items in target_items.items():
        if len(result[category]) != len(items):
            return f"Error: Could not find all items for {category}. Found {len(result[category])} of {len(items)}."
    
    return result

# Example usage
if __name__ == "__main__":
    city = "Nairobi"
    result = scrape_numbeo_specific(city)
    if isinstance(result, dict):
        # Print JSON with indentation
        print(json.dumps(result, indent=2))
        # Optionally save to a file
        with open(f"{city}_cost_of_living.json", "w") as f:
            json.dump(result, f, indent=2)
    else:
        print(result)