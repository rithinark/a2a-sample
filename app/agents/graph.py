from langgraph.graph import StateGraph, END, START
from langgraph.graph.state import CompiledStateGraph
from langgraph.checkpoint.memory import MemorySaver

from langchain_core.messages import AIMessage, BaseMessage
from .state import AssistantState
from .nodes import planner_node, tool_node, responder_node


class Graph:
    def __init__(self):
        self.compiled_graph: CompiledStateGraph

    def build_graph(self):
        graph = StateGraph(AssistantState)
        graph.add_node("planner", planner_node)
        graph.add_node("executor", tool_node)
        graph.add_node("responder", responder_node)

        graph.add_edge(START, "planner")
        graph.add_conditional_edges("planner", self.planner_router)

        graph.add_edge("executor", "planner")
        graph.add_edge("responder", END)
        memory = MemorySaver()
        self.compiled_graph = graph.compile(checkpointer=memory)
        return self.compiled_graph

    def planner_router(self, state: AssistantState):
        last_message: BaseMessage = state.messages[-1]
        if isinstance(last_message, AIMessage) and getattr(
            last_message, "tool_calls", None
        ):

            return "executor"
        return "responder"

    def save_graph_plan(self):
        png_bytes = self.compiled_graph.get_graph().draw_mermaid_png()
        with open("assistant_graph.png", "wb") as f:
            f.write(png_bytes)


graph = Graph()
