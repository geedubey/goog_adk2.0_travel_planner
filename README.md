# Caps Travel Planner: Multi-Agent Swarm (Google ADK)

A production-grade, multi-agent travel planning system built with the Google Agent Development Kit (ADK).

## 1. Multi-Agent Architecture
* **`trip_concierge` (Lead Agent / Root Orchestrator):** Coordinates user goals, budget constraints, and produces an integrated master itinerary.
* **`flight_specialist` (Subagent):** Discovers flight options, routes, and departure/arrival times.
* **`hotel_specialist` (Subagent):** Matches accommodations to flight dates and budget tiers.
* **`sightseeing_specialist` (Subagent):** Analyzes local weather and schedules cultural attractions.

## 2. Directory Structure
```text
caps-travel-planner/
├── __init__.py           # Package entrypoint (from . import agent)
├── agent.py              # Root agent and subagent swarm definitions
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── test_tools.py         # Standalone test runner for all tools
└── tools/
    ├── __init__.py
    ├── flights.py        # Flight search (Amadeus API + fallback engine)
    ├── hotels.py         # Hotel search (curated & dynamic budget engine)
    ├── places.py         # Attractions tool (Wikipedia/curated engine)
    └── weather.py        # 5-day forecast tool (Open-Meteo free API)
```

## 3. Quick Start (Manual Setup in WSL2)

```bash
# 1. Navigate to the project directory
cd /home/ganga/googanti/agydesktop/caps-travel-planner

# 2. Create and activate a Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify all tools independently
python3 test_tools.py
```
