"""Travel Planner Multi-Agent Swarm built with Google ADK.
Features Flight, Hotel, and Sightseeing subagents orchestrated by a Lead Concierge.
Supports both Free Google Gemini API (Cloud Run) and Local Ollama (RTX 4060).
"""
import os
from dotenv import load_dotenv

# Load local environment variables from .env
load_dotenv()

# Import specialized tools
try:
    from tools.weather import get_weather_forecast
    from tools.places import search_attractions
    from tools.flights import search_flights
    from tools.hotels import search_hotels
except ImportError:
    from .tools.weather import get_weather_forecast
    from .tools.places import search_attractions
    from .tools.flights import search_flights
    from .tools.hotels import search_hotels

from google.adk.agents import Agent

# Model Selection: Free Gemini API (if key present) or Local Ollama
google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
ollama_base = os.getenv("OLLAMA_API_BASE", "http://192.168.29.21:11434")

if google_api_key and not google_api_key.lower().startswith("your_"):
    # Ensure both environment variables are set for Google SDKs
    os.environ["GOOGLE_API_KEY"] = google_api_key
    os.environ["GEMINI_API_KEY"] = google_api_key
    print("Using Free Google Gemini API with automatic retry & fallback")
    from google.adk.models import Gemini, FallbackModel
    from google.genai import types
    
    # Configure auto-retry on 503/429
    retry = types.HttpRetryOptions(initial_delay=1, attempts=3)
    
    # Modern active models: gemini-2.5-flash (primary) and gemini-3.8-flash
    model_choice = FallbackModel(
        models=[
            Gemini(model="gemini-2.5-flash", retry_options=retry),
            Gemini(model="gemini-3.8-flash", use_interactions_api=True, retry_options=retry),
            Gemini(model="gemini-2.5-flash-lite", retry_options=retry),
        ]
    )
else:
    print(f"Using Local Ollama via LiteLLM at {ollama_base}")
    from google.adk.models.lite_llm import LiteLlm
    model_choice = LiteLlm(model="ollama_chat/qwen2.5:7b", api_base=ollama_base)
# ---------------------------------------------------------
# Subagent 1: Flight Specialist
# ---------------------------------------------------------
flight_agent = Agent(
    name="flight_specialist",
    model=model_choice,
    tools=[search_flights],
    instruction="""You are a Flight Specialist.
Search flight options for the given origin, destination, and dates.
Compare prices and recommend the best balanced option within budget.
Always state departure and arrival times."""
)

# ---------------------------------------------------------
# Subagent 2: Hotel Specialist
# ---------------------------------------------------------
hotel_agent = Agent(
    name="hotel_specialist",
    model=model_choice,
    tools=[search_hotels],
    instruction="""You are a Hotel & Accommodation Specialist.
Search hotels matching the travel dates and budget limits.
Recommend lodging based on price, rating, and location, and calculate total cost."""
)

# ---------------------------------------------------------
# Subagent 3: Sightseeing Specialist
# ---------------------------------------------------------
sightseeing_agent = Agent(
    name="sightseeing_specialist",
    model=model_choice,
    tools=[search_attractions, get_weather_forecast],
    instruction="""You are a Local City Guide Specialist.
Check the 5-day weather forecast for the destination city.
Search top tourist attractions and synthesize a practical day-by-day plan."""
)

# ---------------------------------------------------------
# Root Orchestrator: Lead Trip Concierge
# ---------------------------------------------------------
root_agent = Agent(
    name="trip_concierge",
    model=model_choice,
    sub_agents=[flight_agent, hotel_agent, sightseeing_agent],
    instruction="""You are the Lead Trip Concierge.
When planning a trip:
1. Ask 'flight_specialist' to find flights.
2. Ask 'hotel_specialist' to find accommodations.
3. Ask 'sightseeing_specialist' for weather and attractions.
4. Synthesize all findings into a master Day-by-Day Travel Itinerary with a total budget breakdown."""
)