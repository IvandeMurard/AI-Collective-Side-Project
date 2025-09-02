# Configuration file for Hackathon Idea Matcher
# Add your API keys and settings here

# Mistral API Configuration
MISTRAL_API_KEY = "AvBkwvKojakoCNEWlKoNeWhN4dvrUqNx"  # Add your Mistral API key here
MISTRAL_MODEL = "mistral-medium"  # Options: mistral-small, mistral-medium, mistral-large

# App Configuration
DEBUG_MODE = True
PORT = 5000
HOST = "127.0.0.1"

# Fallback Configuration
USE_RANDOM_FALLBACK = True  # Use random percentages if API fails
RANDOM_SEED = 42  # For consistent random results during testing
