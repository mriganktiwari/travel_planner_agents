"""Root travel agent: the single entry point for the multi-agent system.

Interprets the user's request, validates duration, and delegates destination
research and itinerary planning to specialist agents (wired in as AgentTools
so it stays in control and returns one combined answer, per the product
contract in docs/product-contract.md).
"""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .destinations_agent import destination_agent
from .itinerary_agent import itinerary_agent
from .prompts.root_agent_prompt import ROOT_AGENT_INSTRUCTION
from backend.tools.duration import validate_trip_duration

root_agent = Agent(
    name="root_travel_agent",
    model="gemini-2.5-flash",
    description="Main travel planning assistant that interprets requests and orchestrates specialist agents.",
    instruction=ROOT_AGENT_INSTRUCTION,
    tools=[AgentTool(agent=destination_agent), AgentTool(agent=itinerary_agent), validate_trip_duration],
)
