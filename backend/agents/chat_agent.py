# backend/agnet/chat_agent.py
from backend.agents.base_agent import BaseAgent
from sqlalchemy.orm import Session
import uuid

class ChatAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ChatAgent",
            role_prompt=(
                "당신은 사용자의 일상 업무를 도와주는 AI 어시스턴트입니다. "
                "짧고 명확하게 대답하세요."
            ),
        )

    def handle(self, db: Session, session_id:str , user_id: str, model:str , message: str) -> tuple[str, str] :
        """일반 대화 처리"""
        
        # 1. seesion_id 가 없으면 (= 첫 대화)
        #   databse에서 "chat_seesion" 테이블에 세션 데이터를 insert 하여 pk로 session_id(=uuid) 반환 받아 사용 한다. 
        if session_id is None or session_id.strip() == "":
            print(f'[chat_agent.py] create new seesion_id!!! -> {session_id}')
            # generate seesuib_id from db, databse에 "chat_seesion" 에 세션 데이터를 insert 하면 pk로 uuid를 회신 
            # new_session = create_chat_session_in_db(db, user_id, ...)
            # session_id = new_session.id
            # db.commit()
            session_id = str(uuid.uuid4()) # (임시조치)
            

        # 2. 이 세션에서 이뤄진 대화 시트로리르저장 한다.
        chat_history = []  
        # fetch_chat_history(seesion_id) from databse
        # print(f"[Agent] DB에서 세션 {session_id}의 이력 조회 (예정)")

        # 3. model + agent 조합으로 prompt 조합
        # get_prompt(model, self.name) from databse

        # 4. LLM 질의 gkrl + 메세지 히스토리 저장
        # save_message_to_db(db, session_id, "user", message)
        # save_message_to_db(db, session_id, "assistant", llm_reply)
        # db.commit()
        llm_reply = self._llm_reply( model, message, chat_history)

        # 5. LLM 답변 메세지 히스토리 저장 
        # save_message_to_db(db, session_id, "user", message)
        # save_message_to_db(db, session_id, "assistant", llm_reply)
        # db.commit()

        return llm_reply, session_id
