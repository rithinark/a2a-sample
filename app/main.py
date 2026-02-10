import chainlit as cl

from langchain_core.runnables.config import RunnableConfig
from langchain_core.messages import HumanMessage, BaseMessageChunk

from agents.graph import graph


@cl.on_chat_start
def on_chat_start():
    graph.build_graph()


@cl.on_message
async def on_message(user_query: cl.Message):
    config = {"configurable": {"thread_id": cl.context.session.id}}
    # cb = cl.LangchainCallbackHandler()
    final_answer = cl.Message(content="")

    async for message, metadata in graph.compiled_graph.astream(
        {"messages": [HumanMessage(content=user_query.content)]},
        stream_mode="messages",
        config=RunnableConfig(**config, recursion_limit=10),
    ):
        if (
            message.content
            and isinstance(message, BaseMessageChunk)
            and not isinstance(message, HumanMessage)
            and metadata["langgraph_node"] == "responder"
        ):
            await final_answer.stream_token(message.content)

    await final_answer.update()
