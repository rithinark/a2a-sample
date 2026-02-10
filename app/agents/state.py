from typing import Optional, Annotated, Sequence, Literal
from dataclasses import dataclass, field
from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages


@dataclass
class AssistantState:
    messages: Annotated[Sequence[AnyMessage], add_messages] = field(
        default_factory=list
    )
    planner_summary: Optional[str] = None


# @dataclass
# class AssistantState(BaseState):

#     action_type: Optional[Literal["tool", "a2a", "respond"]] = None
#     action_name: Optional[str] = None
#     action_args: Optional[str] = None

#     tool_result: Optional[str] = None
#     agent_result: Optional[str] = None
