# backend/routes/langchain_chat_routes.py
from fastapi import APIRouter, Request
from agents.langchain_chat_agent import LangchainChatAgent
from pydantic import BaseModel

router = APIRouter(tags=["LangChain Chat"])

class LangchaChatRequest(BaseModel):
    user_id: str = 'guest'
    message: str

@router.post("/langchain/chat")
async def chat_with_memory(data: LangchaChatRequest):
    """
    LangChain 기반 대화 API:
    - user_id 별로 Redis에 대화 이력 저장
    - 이전 대화를 자동으로 참고
    """
    # data = await request.json()
    user_id = data.user_id
    message = data.message

    agent = LangchainChatAgent(user_id=user_id)
    response = agent.handle(message)

    return {"user_id": user_id, "reply": response}
