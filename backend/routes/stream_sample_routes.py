# backend/routes/stream_sample_routes.py
from typing import Optional
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from agents.stream_sample_agent import StreamSampleAgent
from pydantic import BaseModel


router = APIRouter(tags=["Agent API"])
# agent = StreamSample() # ⬅️ 전역 인스턴스 제거 (혹은 주석 처리)


class PostStreamSampleRequest(BaseModel):
    user_id: Optional[str] = 'guest'
    message: Optional[str]


@router.post("/stream")
async def post_stream_sample(data: PostStreamSampleRequest):
    # data = await request.json()
    user_input = data.message

    agent = StreamSampleAgent() 
    stream_response = agent.handle(user_input)
    
    return StreamingResponse(stream_response, media_type="text/event-stream")


@router.get("/stream")
async def get_stream_sample(request: Request):
    user_id = request.query_params.get("user_id", "guest") 
    message = request.query_params.get("message") 
    keywords_str = request.query_params.get("keywords") # ✅ 키워드 문자열

    keywords = keywords_str.split(',') if keywords_str else []
    
    print(f'Received GET request - User ID: {user_id}, Message: {message}, Keywords: {keywords}')
    
    agent = StreamSampleAgent() 
    stream_response = agent.handle(message)
    
    return StreamingResponse(stream_response, media_type="text/event-stream")
