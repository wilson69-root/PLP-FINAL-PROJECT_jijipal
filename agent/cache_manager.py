import streamlit as st
from agent.core import get_city_guide
from agent.locations import fetch_places_osm
from time import time

def get_cached_city_guide(city: str, budget: int, goal: str) -> list:
    """
    Get city guide data with caching support.
    
    Args:
        city (str): City name
        budget (int): Budget amount
        goal (str): User's goal
        
    Returns:
        list: List of guide tips
    """
    cache_key = f"city_guide_{city}_{budget}_{goal}"
    
    if cache_key not in st.session_state:
        st.session_state[cache_key] = get_city_guide(city, budget, goal)
    
    return st.session_state[cache_key]

def cache_places(city: str, tag: str, ttl: int = 3600) -> list:
    """
    Cache and retrieve places data with TTL support.
    
    Args:
        city (str): City name
        tag (str): Place type tag
        ttl (int): Time to live in seconds (default: 1 hour)
        
    Returns:
        list: List of places
    """
    cache_key = f"places_{city}_{tag}"
    timestamp_key = f"places_timestamp_{city}_{tag}"
    
    current_time = time()
    
    # Check if cache exists and is still valid
    if (
        cache_key in st.session_state 
        and timestamp_key in st.session_state 
        and current_time - st.session_state[timestamp_key] < ttl
    ):
        return st.session_state[cache_key]
    
    # Fetch fresh data
    places = fetch_places_osm(city, tag)
    
    # Update cache
    st.session_state[cache_key] = places
    st.session_state[timestamp_key] = current_time
    
    return places
