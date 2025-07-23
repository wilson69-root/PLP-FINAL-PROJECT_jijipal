"""
Caching module for the Mtaa Agent Project.
Handles caching of scraped results using diskcache for persistence.
"""

import diskcache as dc
import json
import time
import os
from typing import Any, Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Create cache directory if it doesn't exist
CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

# Initialize the cache
cache = dc.Cache(CACHE_DIR, size_limit=100 * 1024 * 1024)  # 100MB limit


def cache_data(key: str, data: Any, ttl: int = 3600) -> bool:
    """
    Cache data with a time-to-live (TTL) in seconds.
    
    Args:
        key: Cache key
        data: Data to cache
        ttl: Time to live in seconds (default: 1 hour)
    
    Returns:
        bool: True if successfully cached, False otherwise
    """
    try:
        cache_entry = {
            'data': data,
            'timestamp': time.time(),
            'ttl': ttl
        }
        
        cache[key] = cache_entry
        logger.debug(f"Cached data with key: {key}, TTL: {ttl}s")
        return True
        
    except Exception as e:
        logger.error(f"Error caching data with key {key}: {e}")
        return False


def get_cached_data(key: str) -> Optional[Any]:
    """
    Retrieve cached data if it exists and hasn't expired.
    
    Args:
        key: Cache key
    
    Returns:
        Cached data if valid, None if not found or expired
    """
    try:
        if key not in cache:
            logger.debug(f"Cache miss for key: {key}")
            return None
        
        cache_entry = cache[key]
        current_time = time.time()
        cached_time = cache_entry['timestamp']
        ttl = cache_entry['ttl']
        
        # Check if cache has expired
        if current_time - cached_time > ttl:
            logger.debug(f"Cache expired for key: {key}")
            del cache[key]  # Remove expired entry
            return None
        
        logger.debug(f"Cache hit for key: {key}")
        return cache_entry['data']
        
    except Exception as e:
        logger.error(f"Error retrieving cached data for key {key}: {e}")
        return None


def cache_exists(key: str) -> bool:
    """
    Check if a cache entry exists and is valid.
    
    Args:
        key: Cache key
    
    Returns:
        bool: True if cache exists and is valid
    """
    return get_cached_data(key) is not None


def invalidate_cache(key: str) -> bool:
    """
    Remove a specific cache entry.
    
    Args:
        key: Cache key to remove
    
    Returns:
        bool: True if successfully removed, False if not found
    """
    try:
        if key in cache:
            del cache[key]
            logger.debug(f"Invalidated cache for key: {key}")
            return True
        else:
            logger.debug(f"Cache key not found for invalidation: {key}")
            return False
            
    except Exception as e:
        logger.error(f"Error invalidating cache for key {key}: {e}")
        return False


def clear_cache() -> bool:
    """
    Clear all cache entries.
    
    Returns:
        bool: True if successfully cleared
    """
    try:
        cache.clear()
        logger.info("Cleared all cache entries")
        return True
        
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        return False


def get_cache_stats() -> dict:
    """
    Get cache statistics and information.
    
    Returns:
        dict: Cache statistics
    """
    try:
        stats = {
            'total_entries': len(cache),
            'cache_size_bytes': cache.volume(),
            'cache_directory': CACHE_DIR,
            'size_limit_bytes': cache.size_limit
        }
        
        # Get entry details
        entries = []
        current_time = time.time()
        
        for key in cache:
            try:
                entry = cache[key]
                age = current_time - entry['timestamp']
                remaining_ttl = entry['ttl'] - age
                
                entries.append({
                    'key': key,
                    'age_seconds': age,
                    'remaining_ttl': remaining_ttl,
                    'is_expired': remaining_ttl <= 0
                })
            except:
                continue
        
        stats['entries'] = entries
        return stats
        
    except Exception as e:
        logger.error(f"Error getting cache stats: {e}")
        return {'error': str(e)}


def cleanup_expired_entries() -> int:
    """
    Remove all expired cache entries.
    
    Returns:
        int: Number of entries removed
    """
    removed_count = 0
    current_time = time.time()
    
    try:
        keys_to_remove = []
        
        for key in cache:
            try:
                entry = cache[key]
                age = current_time - entry['timestamp']
                
                if age > entry['ttl']:
                    keys_to_remove.append(key)
            except:
                # If we can't read the entry, consider it corrupted and remove it
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            try:
                del cache[key]
                removed_count += 1
            except:
                continue
        
        logger.info(f"Cleaned up {removed_count} expired cache entries")
        return removed_count
        
    except Exception as e:
        logger.error(f"Error during cache cleanup: {e}")
        return 0


def cache_city_data(city: str, data_type: str, data: Any, ttl: int = 3600) -> bool:
    """
    Cache city-specific data with a standardized key format.
    
    Args:
        city: City name
        data_type: Type of data (rentals, food, transport, etc.)
        data: Data to cache
        ttl: Time to live in seconds
    
    Returns:
        bool: True if successfully cached
    """
    key = f"{data_type}_{city.lower().replace(' ', '_')}"
    return cache_data(key, data, ttl)


def get_city_data(city: str, data_type: str) -> Optional[Any]:
    """
    Retrieve cached city-specific data.
    
    Args:
        city: City name
        data_type: Type of data to retrieve
    
    Returns:
        Cached data if available and valid
    """
    key = f"{data_type}_{city.lower().replace(' ', '_')}"
    return get_cached_data(key)


def cache_user_session(session_id: str, data: dict, ttl: int = 3600*24) -> bool:
    """
    Cache user session data.
    
    Args:
        session_id: Unique session identifier
        data: Session data to cache
        ttl: Time to live in seconds (default: 24 hours)
    
    Returns:
        bool: True if successfully cached
    """
    key = f"session_{session_id}"
    return cache_data(key, data, ttl)


def get_user_session(session_id: str) -> Optional[dict]:
    """
    Retrieve cached user session data.
    
    Args:
        session_id: Session identifier
    
    Returns:
        Session data if available and valid
    """
    key = f"session_{session_id}"
    return get_cached_data(key)


# Automatic cleanup function that can be called periodically
def periodic_cleanup():
    """Run periodic maintenance on the cache."""
    removed = cleanup_expired_entries()
    stats = get_cache_stats()
    
    logger.info(f"Periodic cleanup completed: {removed} entries removed, "
                f"{stats.get('total_entries', 0)} entries remaining")


# Initialize cache stats logging
if __name__ == "__main__":
    stats = get_cache_stats()
    print(f"Cache initialized with {stats['total_entries']} entries")
    print(f"Cache directory: {stats['cache_directory']}")
    print(f"Cache size: {stats['cache_size_bytes']} bytes")