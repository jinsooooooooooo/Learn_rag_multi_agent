import uuid
from backend.agents.base_agent import BaseAgent
from backend.core.naver_news_api import search_naver_news

class NaverNewsAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="NaverNewsAgent",
            role_prompt=(
                "당신은 뉴스 큐레이션을 담당하는 AI 에이전트입니다. \n"
                "뉴스 기사나 정보를 선별·분류·정리하여 사용자에게 맞게 제공해주세요 \n\n"
                " - 사용자로 부터 뉴스 키워드는 1~3개 까지 입력 받을 수 있습니다. \n"
                " - 입력된 키워드 별로 Naver API를 통해 뉴스 기사(제목,링크)를 가져와 제공 해줄 것 입니다. \n"
                " - 제공된 키워드 링크에 찾아가 기사 내용을 확인(=학습) 한 뒤 키워드별 뉴스의 요약 및 사용자 요청에 답변 해주세요 \n"
            ),
        )

    def handle(self, payload) -> tuple[list[dict], str] :
        """
        네이버 API를 통해 검색 결과 회신

        Args:
            payload (naver_news_routes.NaverNewsRequest): 
                FastAPI 라우트에서 전달하는 Pydantic 모델 객체.
                .message (str), .keywords (List[str]), .user_id (str) 등의 속성을 가짐.
        
        Returns:
            str: 네이버 뉴스 검색 결과 또는 에러 메시지
        """

        print(
            f'[naver_news_agent.py]\n'
            f'  - session_id:   {payload.session_id}\n'
            f'  - user_id   :   {payload.user_id}\n'
            f'  - model     :   {payload.model}\n'
            f'  - keywords  :   {payload.keywords}\n'
            f'  - message   :   {payload.message}\n'
        )

        session_id = payload.session_id
        keywords = payload.keywords
        model = payload.model
        message = payload.message

        # 1. session_id 생성
        
        if session_id is None or session_id.strim()=="":
            session_id = uuid.uuid4()

        # 2. load seesion history
        chat_history = []

        # 3. 시스템 프롬프트 조합

        # 3.1 먼저 입력된 keywords를 순회하여 Naver 뉴스를 조회
        # fetch_news = search_naver_news(user_keywords,3) if user_keywords else "입력한 키워드가 없습니다."
        total_articles = []
        if keywords:
            for idx, keyword in enumerate(keywords, start=1):
                # print(f'키워드{idx}: {keyword}')
                self.role_prompt=f"{self.role_prompt}\n\n\n키워드{idx}: {keyword}"
                fetch_articles = search_naver_news(keyword,3)
                if fetch_articles:
                    # total_articles에 단일 리스트로 합치기
                    total_articles.extend(fetch_articles)

                    # role_prompt 업데이트
                    for i_dx, article in enumerate(fetch_articles, start=1):
                        # print(
                        #     f"  - 제목: {article['title']}\n"
                        #     f"  - 링크: {article['link']}\n"
                        #     f"  - 날짜: {article['pubDate']}\n"
                        #     f"  - 설명: {article['description']}\n"
                        # )
                        self.role_prompt=f"{self.role_prompt}\n  - 제목{i_dx}: {article['title']}"
                        self.role_prompt=f"{self.role_prompt}\n  - 링크{i_dx}: {article['link']}"


             

        # 3.2 키워드 검색 결과가 포함된 프롬프트로 llm query 질의 
        print(f'{self.role_prompt}')   
        llm_reply = self._llm_reply(model, message, chat_history)
        
        
        return total_articles, llm_reply, session_id
