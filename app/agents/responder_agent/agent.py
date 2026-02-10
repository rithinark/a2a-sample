from typing import List
from langchain_core.messages import AnyMessage, BaseMessage
from ..state import AssistantState
from ..base_agent import BaseAgent

RESPONDER_SYSTEM_PROMPT = """
You are a helpful AI assistant responsible for generating the final response to the user.

Respond naturally and conversationally to the user’s latest message using the full conversation history, including any information already provided earlier in the conversation.

All required information has already been gathered before you respond. You must not plan, make decisions, or call tools.

Guidelines:

- Answer the user directly and naturally.
- Use relevant information from earlier messages when it helps produce a better response.
- If previous messages contain results or answers, use that information instead of asking again.
- Do not mention tools, agents, system processes, or internal reasoning.
- Do not explain how the system works internally.
- Maintain continuity with the conversation.

If the user is greeting or making small talk, respond naturally.

If the user asks for information that is not available in the conversation, respond honestly and offer a helpful alternative when possible.

Be clear, concise, and helpful. Your response should be written directly to the user.
"""


class ResponderAgent(BaseAgent):
    def __init__(self, llm, tools=None):

        super().__init__(
            name="planner", system_prompt=RESPONDER_SYSTEM_PROMPT, llm=llm, tools=tools
        )

    async def run(self, state: AssistantState) -> BaseMessage:
        # print(state.messages)
        response = await super().run(state.messages)
        return response
