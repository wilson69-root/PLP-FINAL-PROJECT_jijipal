import concurrent.futures
from openai import OpenAI, AuthenticationError, RateLimitError, APIError
import time
import random

def check_openai_api_key(api_key):
    """
    Check if an OpenAI API key is valid with robust error handling
    Returns tuple (api_key, validity, error_message)
    """
    try:
        client = OpenAI(api_key=api_key)
        
        # Use a lightweight method to validate key
        client.models.list(limit=1)
        
        return (api_key, True, "Valid key")
    
    except AuthenticationError:
        return (api_key, False, "Invalid authentication")
    except RateLimitError:
        return (api_key, False, "Rate limit exceeded - may be valid")
    except APIError as e:
        return (api_key, False, f"API error: {e.message}")
    except Exception as e:
        return (api_key, False, f"Unexpected error: {str(e)}")

# List of API keys to validate
api_keys = [
    "sk-abcdef1234567890abcdef1234567890abcdef12",
    "sk-1234567890abcdef1234567890abcdef12345678",
    "sk-abcdefabcdefabcdefabcdefabcdefabcdef12",
    "sk-7890abcdef7890abcdef7890abcdef7890abcd",
    "sk-1234abcd1234abcd1234abcd1234abcd1234abcd",
    "sk-abcd1234abcd1234abcd1234abcd1234abcd1234",
    "sk-5678efgh5678efgh5678efgh5678efgh5678efgh",
    "sk-efgh5678efgh5678efgh5678efgh5678efgh5678",
    "sk-ijkl1234ijkl1234ijkl1234ijkl1234ijkl1234",
    "sk-mnop5678mnop5678mnop5678mnop5678mnop5678",
    "sk-qrst1234qrst1234qrst1234qrst1234qrst1234",
    "sk-uvwx5678uvwx5678uvwx5678uvwx5678uvwx5678",
    "sk-1234ijkl1234ijkl1234ijkl1234ijkl1234ijkl",
    "sk-5678mnop5678mnop5678mnop5678mnop5678mnop",
    "sk-qrst5678qrst5678qrst5678qrst5678qrst5678",
    "sk-uvwx1234uvwx1234uvwx1234uvwx1234uvwx1234",
    "sk-1234abcd5678efgh1234abcd5678efgh1234abcd",
    "sk-5678ijkl1234mnop5678ijkl1234mnop5678ijkl",
    "sk-abcdqrstefghuvwxabcdqrstefghuvwxabcdqrst",
    "sk-ijklmnop1234qrstijklmnop1234qrstijklmnop",
    "sk-1234uvwx5678abcd1234uvwx5678abcd1234uvwx",
    "sk-efghijkl5678mnopabcd1234efghijkl5678mnop",
    "sk-mnopqrstuvwxabcdmnopqrstuvwxabcdmnopqrst",
    "sk-ijklmnopqrstuvwxijklmnopqrstuvwxijklmnop",
    "sk-abcd1234efgh5678abcd1234efgh5678abcd1234",
    "sk-1234ijklmnop5678ijklmnop1234ijklmnop5678",
    "sk-qrstefghuvwxabcdqrstefghuvwxabcdqrstefgh",
    "sk-uvwxijklmnop1234uvwxijklmnop1234uvwxijkl",
    "sk-abcd5678efgh1234abcd5678efgh1234abcd5678",
    "sk-ijklmnopqrstuvwxijklmnopqrstuvwxijklmnop",
    "sk-1234qrstuvwxabcd1234qrstuvwxabcd1234qrst",
    "sk-efghijklmnop5678efghijklmnop5678efghijkl",
    "sk-mnopabcd1234efghmnopabcd1234efghmnopabcd",
    "sk-ijklqrst5678uvwxijklqrst5678uvwxijklqrst",
    "sk-1234ijkl5678mnop1234ijkl5678mnop1234ijkl",
    "sk-abcdqrstefgh5678abcdqrstefgh5678abcdqrst",
    "sk-ijklmnopuvwx1234ijklmnopuvwx1234ijklmnop",
    "sk-efgh5678abcd1234efgh5678abcd1234efgh5678",
    "sk-mnopqrstijkl5678mnopqrstijkl5678mnopqrst",
    "sk-1234uvwxabcd5678uvwxabcd1234uvwxabcd5678",
    "sk-ijklmnop5678efghijklmnop5678efghijklmnop",
    "sk-abcd1234qrstuvwxabcd1234qrstuvwxabcd1234",
    "sk-1234efgh5678ijkl1234efgh5678ijkl1234efgh",
    "sk-5678mnopqrstuvwx5678mnopqrstuvwx5678mnop",
    "sk-abcdijkl1234uvwxabcdijkl1234uvwxabcdijkl",
    "sk-ijklmnopabcd5678ijklmnopabcd5678ijklmnop",
    "sk-1234efghqrstuvwx1234efghqrstuvwx1234efgh",
    "sk-5678ijklmnopabcd5678ijklmnopabcd5678ijkl",
    "sk-abcd1234efgh5678abcd1234efgh5678abcd1234"
]

def validate_keys(keys, max_workers=5, retry_delay=2):
    """
    Validate API keys with parallel processing and automatic retries
    """
    valid_keys = []
    invalid_keys = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # First pass: Initial validation
        future_to_key = {executor.submit(check_openai_api_key, key): key for key in keys}
        for future in concurrent.futures.as_completed(future_to_key):
            key, valid, msg = future.result()
            if valid:
                valid_keys.append(key)
            else:
                invalid_keys.append((key, msg))
    
    # Second pass: Retry keys with rate limit errors
    retry_keys = [key for key, msg in invalid_keys if "Rate limit" in msg]
    if retry_keys:
        print(f"Retrying {len(retry_keys)} keys after delay...")
        time.sleep(retry_delay)
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_to_key = {executor.submit(check_openai_api_key, key): key for key in retry_keys}
            for future in concurrent.futures.as_completed(future_to_key):
                key, valid, msg = future.result()
                if valid:
                    valid_keys.append(key)
                    # Remove from invalid list
                    invalid_keys = [item for item in invalid_keys if item[0] != key]
    
    return valid_keys, invalid_keys

# Validate all keys with intelligent retry system
start_time = time.time()
valid_keys, invalid_keys = validate_keys(api_keys)
elapsed = time.time() - start_time

# Print results
print(f"\nValidation completed in {elapsed:.2f} seconds")
print(f"Valid keys: {len(valid_keys)}")
print(f"Invalid keys: {len(invalid_keys)}")

# Save results to files
with open("valid_keys.txt", "w") as f:
    f.write("\n".join(valid_keys))

with open("invalid_keys.txt", "w") as f:
    for key, error in invalid_keys:
        f.write(f"{key} | {error}\n")

print("Results saved to valid_keys.txt and invalid_keys.txt")