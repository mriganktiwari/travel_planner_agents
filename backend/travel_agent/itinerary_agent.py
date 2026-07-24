"""Itinerary Planning specialist agent.

Consumes traveller requirements plus a destination brief (from
destination_agent) and produces a day-by-day plan with estimated costs.
Delegates arithmetic to the allocate_budget tool instead of guessing numbers.
"""

from google.adk.agents import Agent
from .prompts.itinerary_agent_prompt import ITINERARY_AGENT_INSTRUCTION
from backend.tools.budget import allocate_budget

itinerary_agent = Agent(
    name="itinerary_agent",
    model="gemini-2.5-flash",
    description="Builds a day-by-day itinerary with estimated costs from travel requirements and a destination brief.",
    instruction=ITINERARY_AGENT_INSTRUCTION,
    tools=[allocate_budget],
)
