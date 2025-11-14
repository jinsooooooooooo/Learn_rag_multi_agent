from typing import Optional
from fastapi import APIRouter, Request
from agents.naver_news_agent import NaverNewsAgent
from pydantic import BaseModel

router = APIRouter(tags=["Agent API"])
agent = NaverNewsAgent()

class NaverNewsRequest(BaseModel):
    message: Optional[str]
    keywords: list[str]
    user_id: str

@router.post("/naver_news")
async def naver_news(data: NaverNewsRequest):
    # data = await request.json()
    # user_input = data.get("message", "")
    response = agent.handle(data)
    return {"agent": agent.name, "articles": response}
