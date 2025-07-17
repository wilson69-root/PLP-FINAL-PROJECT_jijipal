import requests
from typing import Optional, Tuple
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class GeocodingClient:
    def __init__(self):
        self.session = requests.Session()
        # Configure retries
        retries = Retry(
            total=3,  # number of retries
            backoff_factor=1,  # wait 1, 2, 4 seconds between retries
            status_forcelist=[429, 500, 502, 503, 504]  # retry on these status codes
        )
        self.session.mount('https://', HTTPAdapter(max_retries=retries))
        self.last_request_time = 0
        self.min_delay = 1.0  # Minimum 1 second between requests

    def geocode_place(self, place: str) -> Optional[Tuple[float, float]]:
        """
        Convert a place name to latitude and longitude coordinates using Nominatim.
        
        Args:
            place (str): Name of the place to geocode
            
        Returns:
            Optional[Tuple[float, float]]: (latitude, longitude) if found, None if not found
        """
        # Ensure minimum delay between requests
        time_since_last = time.time() - self.last_request_time
        if time_since_last < self.min_delay:
            time.sleep(self.min_delay - time_since_last)
        
        try:
            url = "https://nominatim.openstreetmap.org/search"
            headers = {
                "User-Agent": "MtaaPlus/1.0"
            }
            params = {
                "q": place,
                "format": "json",
                "limit": 1
            }
            
            response = self.session.get(
                url, 
                headers=headers, 
                params=params,
                timeout=10  # Set timeout to 10 seconds
            )
            response.raise_for_status()
            
            self.last_request_time = time.time()
            
            results = response.json()
            if results:
                lat = float(results[0]["lat"])
                lon = float(results[0]["lon"])
                return (lat, lon)
            return None
            
        except requests.exceptions.Timeout:
            print(f"Timeout while geocoding {place}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Geocoding error for {place}: {e}")
            return None

# Create a single instance to be shared
_geocoder = GeocodingClient()

def geocode_place(place: str) -> Optional[Tuple[float, float]]:
    """
    Wrapper function to use the shared GeocodingClient instance.
    """
    return _geocoder.geocode_place(place)
