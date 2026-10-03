"""Travel Planner Multi-Agent Swarm built with Google ADK.
Features Flight, Hotel, and Sightseeing subagents orchestrated by a Lead Concierge.
"""
import os
from dotenv import load_dotenv
from google.adk.models.lite_llm import LiteLlm

# Load local environment variables from .env
load_dotenv()

# Import specialized tools
from .tools.weather import get_weather_forecast
from .tools.places import search_attractions
from .tools.flights import search_flights
from .tools.hotels import search_hotels

local_llm = LiteLlm(model="ollama_chat/qwen2.5:7b")


try:
    from google.adk.agents import Agent
except ImportError:
    # Fallback placeholder if google-adk is not yet installed in current python environment
    class Agent:
        def __init__(self, name, model=local_llm, tools=None, sub_agents=None, instruction=""):
            self.name = name
            self.model = model
            self.tools = tools or []
            self.sub_agents = sub_agents or []
            self.instruction = instruction


# ---------------------------------------------------------
# Subagent 1: Flight Specialist
# ---------------------------------------------------------

# Pass local_llm to each agent:
flight_agent = Agent(
    name="flight_specialist",
    model=local_llm,
    tools=[search_flights],
    instruction="""You are a meticulous Flight Booking Specialist.
Your responsibilities:
1. Search for flight options matching user origin, destination, and dates.
2. Compare prices, flight durations, and departure/arrival times.
3. Recommend the best balanced flight option within the user's flight budget.
4. Always note departure and arrival times so other agents can plan accordingly."""
)

# ---------------------------------------------------------
# Subagent 2: Hotel Specialist
# ---------------------------------------------------------
hotel_agent = Agent(
    name="hotel_specialist",
    model=local_llm,
    tools=[search_hotels],
    instruction="""You are an Accommodation & Hospitality Specialist.
Your responsibilities:
1. Search for hotels matching check-in and check-out dates and budget limits.
2. Evaluate hotel ratings, amenities (WiFi, transit access, breakfast), and neighborhood safety/proximity.
3. Recommend lodging that minimizes commute time to central landmarks.
4. Calculate total lodging cost (nightly rate * number of nights)."""
)

# ---------------------------------------------------------
# Subagent 3: Sightseeing & Activities Specialist
# ---------------------------------------------------------
sightseeing_agent = Agent(
    name="sightseeing_specialist",
    model=local_llm,
    tools=[search_attractions, get_weather_forecast],
    instruction="""You are an expert Local City Guide and Itinerary Specialist.
Your responsibilities:
1. Check the 5-day weather forecast for the destination city to plan indoor vs outdoor activities.
2. Retrieve top cultural sights, historical landmarks, and attractions.
3. Group attractions logically by geographic neighborhood to prevent travel fatigue.
4. Create an engaging, realistic day-by-day activity schedule."""
)

# ---------------------------------------------------------
# Root Orchestrator: Lead Trip Concierge
# ---------------------------------------------------------
root_agent = Agent(
    name="trip_concierge",
    model=local_llm,
    sub_agents=[flight_agent, hotel_agent, sightseeing_agent],
    instruction="""You are the Lead Trip Concierge orchestrating a dream vacation.
When a user asks for a trip plan:
1. Identify key constraints: Origin, Destination, Dates, Total Budget, and Travel Style.
2. Delegate to 'flight_specialist' to find realistic travel options and lock in arrival/departure times.
3. Delegate to 'hotel_specialist' to find accommodations matching the exact flight dates and budget allocation.
4. Delegate to 'sightseeing_specialist' to inspect weather and craft a daily itinerary.
5. Synthesize all findings into a master Day-by-Day Travel Itinerary including:
   - Trip Summary & Total Budget Breakdown (Flights + Hotel + Sightseeing estimates)
   - Flight Details (Airlines, Times, Outbound & Inbound)
   - Hotel Recommendation (Neighborhood, Nightly & Total cost, Amenities)
   - Day-by-Day Schedule (Morning, Afternoon, Evening) with weather notes
   - Essential Packing & Local Tips."""
)
