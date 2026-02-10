from typing import List
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool
from core.llm_client import llm
from runtime.action_registry import action_registry
from .planner_agent.agent import PlannerAgent
from .responder_agent.agent import ResponderAgent

# from .planner_agent.schema import PlannerOutput
from .state import AssistantState
from runtime.a2a_discover import AgentDiscover


async def discover_and_register_a2a_tools():
    a2a_agent_tools = AgentDiscover(base_url="http://localhost:7000")
    tools = await a2a_agent_tools.create_a2a_tools()

    for tool in tools:
        action_registry.register(
            name=tool.name, handler=tool, action_type="a2a_skill"
        )
    return tools

async def planner_node(state: AssistantState):
    a2a_agent_tools = await discover_and_register_a2a_tools()
    planner_agent = PlannerAgent(llm=llm, tools=a2a_agent_tools)
    response = await planner_agent.run(state)
    return {"messages": [response]}


async def tool_node(state: AssistantState):
    last_message = state.messages[-1]

    if not isinstance(last_message, AIMessage):
        return {}

    tool_calls = getattr(last_message, "tool_calls", None)

    if not tool_calls:
        return {}

    tools_messages: List[ToolMessage] = []

    for tool_call in tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        tool_call_id = tool_call["id"]

        try:
            tool_func = action_registry.get(tool_name)["handler"]

            if hasattr(tool_func, "ainvoke"):
                tool_result = await tool_func.ainvoke(tool_args)
            else:
                tool_result = tool_func(**tool_args)

        except Exception as ex:
            tool_result = f"Error executing tool '{tool_name}': {str(ex)}"

        tools_messages.append(
            ToolMessage(content=tool_result, tool_call_id=tool_call_id)
        )

    return {"messages": tools_messages}


async def responder_node(state: AssistantState):
    responder_agent = ResponderAgent(llm=llm)

    response = await responder_agent.run(state)

    return {"messages": [AIMessage(content=response.content)]}
