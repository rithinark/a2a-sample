import httpx
from uuid import uuid4
from langchain_core.tools import StructuredTool

from a2a.client import A2AClient
from a2a.client import A2ACardResolver
from a2a.types import (
    AgentSkill,
    AgentCard,
    MessageSendParams,
    SendMessageRequest,
    SendMessageResponse
)


class AgentDiscover:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.httpx_client: httpx.AsyncClient | None = None
        self.a2a_client: A2AClient | None = None

    async def connect(self) -> AgentCard:
        self.httpx_client = httpx.AsyncClient()

        resolver = A2ACardResolver(
            httpx_client=self.httpx_client,
            base_url=self.base_url,
        )

        agent_card: AgentCard = await resolver.get_agent_card()

        self.a2a_client = A2AClient(
            httpx_client=self.httpx_client,
            agent_card=agent_card,
        )

        return agent_card

    async def create_a2a_tools(self) -> list[StructuredTool]:

        if self.a2a_client is None:
            agent_card = await self.connect()
        else:
            agent_card = self.a2a_client.get_card()

        tools = []
        for skill in agent_card.skills:
            tool = self._create_tool_for_skill(skill)
            tools.append(tool)

        return tools

    def _extract_text_from_response(self, response: SendMessageResponse) -> str:
        artifacts = response.model_dump()['result']['artifacts']

        texts = []

        for artifact in artifacts:
            for part in artifact['parts'][1:]:
                texts.append(part['text'])

        full_text = "\n".join(texts)
        return full_text

    def _create_tool_for_skill(self, skill: AgentSkill):

        skill_name = skill.name  # safe capture

        async def _tool_func(query: str) -> str:

            request = SendMessageRequest(
                id=str(uuid4()),
                params=MessageSendParams(
                    message={
                        "role": "user",
                        "parts": [
                            {
                                "kind": "text",
                                "text": query,
                            }
                        ],
                        "message_id": uuid4().hex,
                    }
                ),
            )

            response = await self.a2a_client.send_message(request)

            return self._extract_text_from_response(response)
            # return response
        return StructuredTool.from_function(
            coroutine=_tool_func,
            name=skill.id,
            description=skill.description or f"A2A skill: {skill_name}",
        )


    async def close(self):
        if self.httpx_client:
            await self.httpx_client.aclose()
