"""Streamlit Web UI for ADK Multi-Agent Travel Planner."""
import asyncio
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import root_agent

# Page config
st.set_page_config(
    page_title="AI Travel Concierge",
    page_icon="✈️",
    layout="wide"
)

st.title("✈️ AI Travel Concierge")
st.caption("Powered by Google ADK Multi-Agent Swarm (Flight, Hotel & Sightseeing Specialists)")

# Sidebar: Trip Parameters
with st.sidebar:
    st.header("🗺️ Trip Details")
    origin = st.text_input("Departure City / Airport", value="London")
    destination = st.text_input("Destination City / Airport", value="Paris")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Departure Date")
    with col2:
        end_date = st.date_input("Return Date")
    budget = st.number_input("Total Budget ($ USD)", min_value=100, max_value=20000, value=800, step=50)
    travel_style = st.selectbox("Travel Style", ["Budget", "Balanced", "Luxury", "Family-friendly"])
    
    st.divider()
    active_model = "Gemini 3.8 Flash (Cloud)" if os.getenv("GOOGLE_API_KEY") else "Ollama Qwen 2.5 7B (Local)"
    st.info(f"**Active Engine:** {active_model}")

# Helper to run async ADK runner
async def run_swarm(prompt_text, status_placeholder, log_container):
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="caps_travel_planner",
        agent=root_agent,
        session_service=session_service,
    )
    user_id = "web_user"
    session = await session_service.create_session(app_name="caps_travel_planner", user_id=user_id)
    
    message = types.Content(role="user", parts=[types.Part(text=prompt_text)])
    
    response_text = ""
    async for event in runner.run_async(user_id=user_id, session_id=session.id, new_message=message):
        author = getattr(event, "author", None) or "Agent"
        if event.content and event.content.parts:
            for part in event.content.parts:
                if getattr(part, "text", None):
                    response_text += part.text
                elif getattr(part, "function_call", None):
                    fn = part.function_call
                    status_placeholder.write(f"⚙️ **{author}** calling `{fn.name}`...")
                    log_container.write(f"👉 `{author}` invoked `{fn.name}({fn.args})`")
                elif getattr(part, "function_response", None):
                    resp = part.function_response
                    log_container.write(f"✅ Received data for `{resp.name}`")
                    
    return response_text

# Main Action
if st.button("🚀 Plan My Vacation", type="primary", use_container_width=True):
    prompt = (
        f"Plan a {travel_style.lower()} trip from {origin} to {destination} "
        f"from {start_date} to {end_date} with a total budget of ${budget}. "
        f"Search flights, find a hotel, check weather forecast, and suggest key sightseeing spots."
    )
    
    status_box = st.empty()
    with st.expander("🔍 Live Agent Swarm Activity", expanded=True):
        log_box = st.container()
        
    status_box.info("🤖 Trip Concierge is coordinating with subagents...")
    
    with st.spinner("Generating your personalized itinerary..."):
        try:
            itinerary = asyncio.run(run_swarm(prompt, status_box, log_box))
            status_box.success("🎉 Trip plan generated successfully!")
            st.markdown("### 📋 Your Comprehensive Travel Plan")
            st.markdown(itinerary)
        except Exception as e:
            status_box.error(f"Execution Error: {e}")