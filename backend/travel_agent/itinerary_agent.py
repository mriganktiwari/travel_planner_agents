from google.adk.agents import Agent
from .prompts.itinerary_agent_prompt import ITINERARY_AGENT_INSTRUCTION

itinerary_agent = Agent(
    name="itinerary_agent",
    model="gemini-2.5-flash",
    description="Builds a day-by-day itinerary with estimated costs from travel requirements and a destination brief.",
    instruction=ITINERARY_AGENT_INSTRUCTION,
)
