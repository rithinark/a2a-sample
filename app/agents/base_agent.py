from typing import Dict, Any, List
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, AnyMessage, BaseMessage
from langchain_core.runnables import RunnableSequence



class BaseAgent:
    def __init__(
        self, name: str, system_prompt: str, llm: BaseChatModel, tools: List = None
    ):
        self.name = name
        self.llm = llm
        if tools:
            self.llm = self.llm.bind_tools(tools)

        system_message = SystemMessage(content=system_prompt)
        conversation = MessagesPlaceholder("conversation", optional=True)
        prompt = ChatPromptTemplate.from_messages([system_message, conversation])
        self.chain = RunnableSequence(prompt | self.llm)

    async def run(self, messages: List[AnyMessage]) -> BaseMessage:
        response = await self.chain.ainvoke({"conversation": messages})
        return response
