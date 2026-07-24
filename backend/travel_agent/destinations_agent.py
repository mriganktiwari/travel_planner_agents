"""Destination Research specialist agent.

Recommends or validates a single destination and produces a concise
destination brief for itinerary_agent to build on. Does not create a
day-by-day itinerary — that responsibility belongs to itinerary_agent.
"""

from google.adk.agents import Agent
from .prompts.destination_agent_prompt import DESTINATION_AGENT_INSTRUCTION

destination_agent = Agent(
    name='destination_agent',
    model='gemini-2.5-flash',
    description='Recommends or validates a travel destination and produces a concise destination brief.',
    instruction=DESTINATION_AGENT_INSTRUCTION
)
