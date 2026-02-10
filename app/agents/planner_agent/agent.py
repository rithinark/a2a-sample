from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import AnyMessage, ToolMessage, ToolCall, BaseMessage, SystemMessage
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool
from .schema import PlannerOutput
from ..state import AssistantState
from ..base_agent import BaseAgent


PLANNER_SYSTEM_PROMPT = """
You are the PLANNER of an AI assistant system.

Your job is to decide whether a tool needs to be called
based on the conversation history.

You do NOT respond to the user.
You do NOT generate conversational replies.

Look at the full conversation history:

- If the user's request requires a tool and the tool has
  not yet been used, call the appropriate tool.
- If the required tool has already been called and the
  result is available in the history, do NOT call the tool again.
- If no tool is required, produce a normal message without
  tool calls so the responder can generate the final reply.
- Once the necessary tools have been called, stop and provide summary letting the responder agent take over.

Rules:

- Call tools only when necessary.
- Do not call tools for greetings or normal conversation.
- Do not repeat the same tool call if the result already exists.
- Do not answer the user directly.

Output behavior:

- AIMessage with tool_calls → continue tool execution.
- AIMessage without tool_calls → hand over to responder.

"""


class PlannerAgent(BaseAgent):
    def __init__(self, llm: BaseChatModel, tools: Optional[List[BaseTool]] = None):
        super().__init__(
            name="planner", system_prompt=PLANNER_SYSTEM_PROMPT, llm=llm, tools=tools
        )

    async def run(self, state: AssistantState) -> BaseMessage:
        response = await super().run(state.messages)
        return response
