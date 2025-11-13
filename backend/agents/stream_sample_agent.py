# backend/agnet/stream_sample_agent.py
import asyncio
from typing import AsyncIterator, Iterator
from agents.base_agent import BaseAgent

class StreamSampleAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="StreamSampleAgent",
            role_prompt=(
                "fastAPI에서 Stream Respnose 샘플 테스트를 하기 위함입니다."
                "짧고 명확하게 대답하세요."
            ),
        )

    # handle 메서드를 async def로 변경하여 비동기 제너레이터로 만듭니다.
    async def handle(self, user_input: str) -> AsyncIterator[str]: # 반환 타입을 Iterator[str로 명시
        """일반 대화 처리"""
        sample_response = ["1장","2장","3장","4장"]
        for item in sample_response:
            yield f"data: {item}\n\n"
            await asyncio.sleep(3)
           
        # 스트림의 마지막에 명시적으로 [DONE] 메시지를 전송합니다.
        yield "data: [DONE]\n\n"     
        