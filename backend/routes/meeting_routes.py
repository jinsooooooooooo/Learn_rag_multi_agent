# backend/routes/meeting_routes.py
from typing import Optional
from fastapi import APIRouter, Request
from agents.meeting_agent import MeetingAgent
from pydantic import BaseModel

router = APIRouter(tags=["Agent API"])
agent = MeetingAgent()

class MeetingRequest(BaseModel):
    """
    회의실 관련 AI 메세지 전송
    """
    session_id: Optional[str] = None
    user_id: str = 'guest'
    model: str = 'gpt-4o-mini'
    message: str # 사용자의 입력 메시지 (필수 문자열 필드)



@router.post("/meeting")
async def meeting(payload: MeetingRequest):
    # user_input = payload.message
    # response = agent.handle(user_input)
    response_text, session_id = agent.handle(  payload.session_id, payload.user_id , payload.model, payload.message )

    return {
        "agent": agent.name, 
        "reply": response_text,
        "session_id": session_id
        }
