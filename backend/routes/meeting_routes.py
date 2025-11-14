# backend/routes/meeting_routes.py
from fastapi import APIRouter, Request
from agents.meeting_agent import MeetingAgent
from pydantic import BaseModel

router = APIRouter(tags=["Agent API"])
agent = MeetingAgent()

class MeetingRequest(BaseModel):
    user_id: str = 'guest'
    message: str

@router.post("/meeting")
async def meeting(request: MeetingRequest):
    user_input = request.message
    response = agent.handle(user_input)
    return {"agent": agent.name, "reply": response}
