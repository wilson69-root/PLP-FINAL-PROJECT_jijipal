import requests

def fetch_places_osm(city: str, tag: str = "restaurant") -> list[str]:
    """
    Fetches places from OpenStreetMap using Overpass API by city and tag.
    Tag examples: restaurant, fast_food, supermarket, pharmacy, hospital
    """
    query = f"""
    [out:json][timeout:25];
    area[name="{city}"]->.searchArea;
    (
      node["amenity"="{tag}"](area.searchArea);
    );
    out body;
    """
    try:
        res = requests.get("https://overpass-api.de/api/interpreter", params={"data": query}, timeout=15)
        res.raise_for_status()
        data = res.json()
        names = []
        for el in data.get("elements", []):
            tags = el.get("tags", {})
            name = tags.get("name")
            if name:
                names.append(name)
        return names[:10] if names else ["⚠️ No named locations found."]
    except Exception as e:
        return [f"❌ Failed to fetch OSM places: {e}"]
