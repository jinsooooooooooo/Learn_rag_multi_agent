# backend/routes/chat_routes.py
from fastapi import APIRouter, Request
from pydantic import BaseModel
from agents.chat_agent import ChatAgent

router = APIRouter(tags=["Agent API"])
agent = ChatAgent()

# Pydantic 모델 정의 (요청 본문 Schema)
class ChatRequest(BaseModel):
    """
    llm Chat을 보내기이한 메세지 전송
    """
    user_id: str = 'guest'
    message: str # 사용자의 입력 메시지 (필수 문자열 필드)

@router.post("/chat")
async def chat(payload: ChatRequest):
    # data = await request.json()
    # user_input = data.get("message", "")
    user_input = payload.message # ✅ Pydantic 모델을 통해 안전하고 깔끔하게 데이터 접근
    response = agent.handle(user_input)
    return {"agent": agent.name, "reply": response}
