from typing import Literal, Optional, Dict
from pydantic import BaseModel, Field


class PlannerOutput(BaseModel):
    action_type: Literal["a2a", "tool", "respond"] = Field(
        ..., description="The type of action to take: 'tool', 'a2a', or 'respond'"
    )
    action_name: Optional[str] = Field(
        ...,
        description="The name of the tool or agent to call, or null if responding to the user",
    )
    action_args: Optional[Dict] = Field(
        default_factory=dict,
        description="The arguments to pass to the tool or agent, or empty if responding to the user",
    )
