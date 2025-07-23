"""
HuggingFace transformer interface for the Mtaa Agent Project.
Handles all AI model interactions and text generation.
"""

from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import logging
import os
from typing import Optional

# Set up logging
logger = logging.getLogger(__name__)

# Model configuration
DEFAULT_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
FALLBACK_MODEL = "microsoft/DialoGPT-medium"

# Global model instance
model = None
tokenizer = None


def initialize_model(model_name: str = DEFAULT_MODEL, use_fallback: bool = False):
    """
    Initialize the HuggingFace model and tokenizer.
    
    Args:
        model_name: Name of the HuggingFace model to use
        use_fallback: Whether to use a smaller fallback model
    
    Returns:
        bool: True if successfully initialized
    """
    global model, tokenizer
    
    try:
        if use_fallback:
            model_name = FALLBACK_MODEL
            logger.info(f"Using fallback model: {model_name}")
        
        logger.info(f"Initializing model: {model_name}")
        
        # Initialize with pipeline for easier use
        model = pipeline(
            "text-generation",
            model=model_name,
            tokenizer=model_name,
            device_map="auto" if os.getenv("CUDA_VISIBLE_DEVICES") else "cpu",
            torch_dtype="auto"
        )
        
        logger.info(f"Successfully initialized model: {model_name}")
        return True
        
    except Exception as e:
        logger.error(f"Error initializing model {model_name}: {e}")
        
        if not use_fallback and model_name != FALLBACK_MODEL:
            logger.info("Attempting to initialize with fallback model...")
            return initialize_model(use_fallback=True)
        
        return False


def ask_model(prompt: str, max_new_tokens: int = 300, temperature: float = 0.7, 
              do_sample: bool = True, top_p: float = 0.9) -> str:
    """
    Generate text using the HuggingFace model.
    
    Args:
        prompt: Input prompt for the model
        max_new_tokens: Maximum number of new tokens to generate
        temperature: Sampling temperature (higher = more random)
        do_sample: Whether to use sampling
        top_p: Top-p (nucleus) sampling parameter
    
    Returns:
        Generated text response
    """
    global model
    
    if model is None:
        logger.warning("Model not initialized, attempting to initialize...")
        if not initialize_model():
            return _fallback_response(prompt)
    
    try:
        logger.debug(f"Generating response for prompt: {prompt[:100]}...")
        
        # Generate response
        result = model(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=do_sample,
            top_p=top_p,
            pad_token_id=model.tokenizer.eos_token_id,
            return_full_text=False  # Only return the generated part
        )
        
        response = result[0]['generated_text']
        logger.debug(f"Generated response: {response[:100]}...")
        
        return response.strip()
        
    except Exception as e:
        logger.error(f"Error generating response: {e}")
        return _fallback_response(prompt)


def ask_model_chat(messages: list, max_new_tokens: int = 300) -> str:
    """
    Generate chat response using conversation format.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content'
        max_new_tokens: Maximum number of new tokens to generate
    
    Returns:
        Generated chat response
    """
    # Convert messages to a prompt format
    prompt = _format_chat_prompt(messages)
    return ask_model(prompt, max_new_tokens=max_new_tokens)


def generate_summary(text: str, max_length: int = 150) -> str:
    """
    Generate a summary of the given text.
    
    Args:
        text: Text to summarize
        max_length: Maximum length of summary
    
    Returns:
        Generated summary
    """
    prompt = f"""
    Please provide a concise summary of the following text in {max_length} words or less:

    {text}

    Summary:"""
    
    return ask_model(prompt, max_new_tokens=max_length)


def generate_recommendations(context: str, user_preferences: str) -> str:
    """
    Generate recommendations based on context and user preferences.
    
    Args:
        context: Context information
        user_preferences: User preferences and requirements
    
    Returns:
        Generated recommendations
    """
    prompt = f"""
    Based on the following context and user preferences, provide specific recommendations:

    Context: {context}
    User Preferences: {user_preferences}

    Recommendations:"""
    
    return ask_model(prompt, max_new_tokens=400)


def _format_chat_prompt(messages: list) -> str:
    """Format a list of messages into a prompt string."""
    prompt_parts = []
    
    for message in messages:
        role = message.get('role', 'user')
        content = message.get('content', '')
        
        if role == 'system':
            prompt_parts.append(f"System: {content}")
        elif role == 'user':
            prompt_parts.append(f"User: {content}")
        elif role == 'assistant':
            prompt_parts.append(f"Assistant: {content}")
    
    prompt_parts.append("Assistant:")
    return "\n".join(prompt_parts)


def _fallback_response(prompt: str) -> str:
    """Generate a fallback response when the model fails."""
    logger.warning("Using fallback response generation")
    
    # Simple keyword-based responses
    prompt_lower = prompt.lower()
    
    if any(word in prompt_lower for word in ['budget', 'money', 'cost', 'price']):
        return "Here are some budget-friendly suggestions for your situation. Consider looking for shared accommodation, eating at local restaurants, and using public transport to save money."
    
    elif any(word in prompt_lower for word in ['accommodation', 'housing', 'rent', 'room']):
        return "For housing in Kenyan cities, consider shared apartments, bedsitters, or hostels. Always visit the property first and negotiate the rent. Areas closer to the city center tend to be more expensive."
    
    elif any(word in prompt_lower for word in ['transport', 'matatu', 'bus', 'travel']):
        return "For transport, matatus are the most affordable option. Learn the routes and always confirm the fare before boarding. Boda bodas are convenient for short distances but more expensive."
    
    elif any(word in prompt_lower for word in ['food', 'restaurant', 'eating', 'meal']):
        return "Local kibandas offer affordable meals. Supermarkets like Tuskys and Naivas are good for groceries. Markets have fresh produce at better prices than supermarkets."
    
    elif any(word in prompt_lower for word in ['safety', 'security', 'safe']):
        return "Stay aware of your surroundings, especially at night. Avoid displaying expensive items. Use registered taxis or ride-hailing apps instead of walking alone in unfamiliar areas."
    
    else:
        return "I'd recommend starting with basic necessities: secure accommodation, reliable transport routes, affordable food options, and local community connections. Focus on one step at a time."


def check_model_status() -> dict:
    """
    Check the status of the model.
    
    Returns:
        Dictionary with model status information
    """
    global model
    
    status = {
        "model_loaded": model is not None,
        "model_name": DEFAULT_MODEL if model else None,
        "ready": False
    }
    
    if model is not None:
        try:
            # Test with a simple prompt
            test_response = ask_model("Hello", max_new_tokens=10)
            status["ready"] = len(test_response) > 0
            status["test_response"] = test_response
        except Exception as e:
            status["error"] = str(e)
    
    return status


def reload_model(model_name: str = DEFAULT_MODEL) -> bool:
    """
    Reload the model with a different configuration.
    
    Args:
        model_name: Name of the model to load
    
    Returns:
        bool: True if successfully reloaded
    """
    global model
    
    # Clear existing model
    model = None
    
    # Initialize new model
    return initialize_model(model_name)


# Auto-initialize model when module is imported
try:
    initialize_model()
except Exception as e:
    logger.warning(f"Could not auto-initialize model: {e}")
    logger.info("Model will be initialized on first use")