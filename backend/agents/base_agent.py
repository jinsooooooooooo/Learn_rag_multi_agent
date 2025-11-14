# backend\agent\base_agent.py
from abc import ABC, abstractmethod
from core.llm_core import call_llm

class BaseAgent(ABC):
    """모든 에이전트의 공통 기반 클래스"""
    
    def __init__(self, name: str, role_prompt: str):
        self.name = name
        self.role_prompt = role_prompt

    @abstractmethod
    def handle(self, data) -> str:
        """각 에이전트별 요청 처리 로직"""
        pass

    def _llm_reply(self, content: str) -> str:
        """LLM 호출 공통 함수"""
        full_prompt = f"{self.role_prompt}\n\n사용자 요청:\n{content}"
        return call_llm(full_prompt)






