from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool
from .destinations_agent import destination_agent
from .itinerary_agent import itinerary_agent
from .prompts.root_agent_prompt import ROOT_AGENT_INSTRUCTION

root_agent = Agent(
    name="root_travel_agent",
    model="gemini-2.5-flash",
    description="Main travel planning assistant that interprets requests and orchestrates specialist agents.",
    instruction=ROOT_AGENT_INSTRUCTION,
    tools=[AgentTool(agent=destination_agent), AgentTool(agent=itinerary_agent)],
)
