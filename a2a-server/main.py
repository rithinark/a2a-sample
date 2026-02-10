from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore, TaskUpdater
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.utils import new_agent_text_message, new_task
from a2a.server.events import EventQueue
from a2a.types import Part, TextPart
from a2a.utils.errors import ServerError
from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from langchain.agents import create_agent
import uvicorn
from dotenv import load_dotenv

load_dotenv()


@tool
def weather_agent_tool(location: str) -> str:
    """A simple tool that simulates fetching weather information for a given location."""
    return f"The current weather in {location} is sunny with a temperature of 25°C."


weather_agent = create_agent(
    model=ChatGroq(model="qwen/qwen3-32b").bind_tools([weather_agent_tool]),
    tools=[weather_agent_tool],
    system_prompt="You are a helpful assistant that provides weather information.",
)


class WeatherAgentExecutor(AgentExecutor):
    def __init__(self):
        self.agent = weather_agent

    async def execute(self, context: RequestContext, event_queue: EventQueue) -> None:
        result = await self.agent.ainvoke(
            {"messages": [HumanMessage(content=context.get_user_input())]}
        )
        query =  context.get_user_input()
        task = context.current_task
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue, task.id, task.context_id)
        try:
            response = await self.agent.ainvoke({"messages": [HumanMessage(content=query)]})
            parts = [Part(root=TextPart(text=message.content)) for message in response["messages"] if message.content]
            await updater.add_artifact(parts, name="agent_response")
            await updater.complete()
        except Exception as ex:
            raise ServerError(f"Error executing agent: {str(ex)}")

        # await event_queue.enqueue_event(new_agent_text_message(result))

    async def cancel(self, context: RequestContext, event_queue: EventQueue):
        raise Exception("Cancellation not supported for WeatherAgentExecutor")


skill = AgentSkill(
    name="Weather Info",
    description="Provides weather information for a given location.",
    id="weather_info",
    tags=["weather"]
)

agent_card = AgentCard(
    name="Weather Agent",
    description="An agent that provides weather information based on user queries.",
    url="http://localhost:7000",
    capabilities=AgentCapabilities(streaming=True),
    skills=[skill],
    default_input_modes=["text"],
    default_output_modes=["text"],
    version="1.0.0"
)

request_hander = DefaultRequestHandler(
    agent_executor=WeatherAgentExecutor(), task_store=InMemoryTaskStore()
)

server = A2AStarletteApplication(agent_card=agent_card, http_handler=request_hander)

uvicorn.run(server.build(), host="0.0.0.0", port=7000)
