from dataclasses import dataclass
from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langgraph.managed import IsLastStep


@dataclass
class InputState(TypedDict):
    """
    Defines the input state for the agent, representing a narrower interface to the outside world.
    This class is used to define the initial state and structure of incoming data.
    """

    messages: Annotated[Sequence[AnyMessage], add_messages]


@dataclass
class State(InputState):
    """
    Represents the complete state of the agent, extending InputState with additional attributes.
    This class can be used to store any information needed throughout the agent's lifecycle.
    """

    is_last_step: IsLastStep
