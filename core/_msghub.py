from typing import Optional, Union
from ._agent import Agent
from ._model import ChatResponse


class MsgHub:
    def __init__(
        self, 
        participants: list[Agent],
        announcement: Optional[Union[ChatResponse, list[ChatResponse]]] = None
    ):
        self.participants = participants
        self.announcement = announcement
    
    def __enter__(self) -> "MsgHub":
        for agent in self.participants:
            agent._audience = [a for a in self.participants if a != agent]
        
        if self.announcement:
            self.broadcast(self.announcement)
        
        return self
    
    def __exit__(self, *args, **kwargs) -> None:
        for agent in self.participants:
            agent._audience = None
    
    def add(self, agent: Union[Agent, list[Agent]]) -> None:
        if isinstance(agent, list):
            for a in agent:
                if a not in self.participants:
                    self.participants.append(a)
        else:
            if agent not in self.participants:
                self.participants.append(agent)
        
        self._reset_audience()
    
    def remove(self, agent: Union[Agent, list[Agent]]) -> None:
        if isinstance(agent, list):
            for a in agent:
                if a in self.participants:
                    self.participants.remove(a)
                    a._audience = None
        else:
            if agent in self.participants:
                self.participants.remove(agent)
                agent._audience = None
        
        self._reset_audience()
    
    def broadcast(self, msg: Union[ChatResponse, list[ChatResponse]]) -> None:
        for agent in self.participants:
            agent.observe(msg)
    
    def _reset_audience(self) -> None:
        for agent in self.participants:
            agent._audience = [a for a in self.participants if a != agent]


def msghub(
    participants: list[Agent],
    announcement: Optional[Union[ChatResponse, list[ChatResponse]]] = None
) -> MsgHub:
    return MsgHub(participants, announcement)
