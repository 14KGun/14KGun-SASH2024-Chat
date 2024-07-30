from dotenv import load_dotenv
import requests
import os

# load environment variables
load_dotenv()
CLOVASTUDIO_API_KEY = (
    os.environ["CLOVASTUDIO_API_KEY"] if "CLOVASTUDIO_API_KEY" in os.environ else ""
)
CLOVASTUDIO_GATEWAY_API_KEY = (
    os.environ["CLOVASTUDIO_GATEWAY_API_KEY"]
    if "CLOVASTUDIO_GATEWAY_API_KEY" in os.environ
    else ""
)


class CompletionExecutor:
    def __init__(self):
        self.host = "https://clovastudio.stream.ntruss.com"
        self.model_name = "HCX-003"

    def execute(self, completion_request):
        with requests.post(
            "{host}/testapp/v1/chat-completions/{model}".format(
                host=self.host, model=self.model_name
            ),
            headers={
                "X-NCP-CLOVASTUDIO-API-KEY": CLOVASTUDIO_API_KEY,
                "X-NCP-APIGW-API-KEY": CLOVASTUDIO_GATEWAY_API_KEY,
                "Content-Type": "application/json; charset=utf-8",
                "Accept": "text/event-stream",
            },
            json=completion_request,
            stream=True,
        ) as r:
            for line in r.iter_lines():
                if line:
                    print(line.decode("utf-8"))


systemContent = """
- 당신은 전 세계의 모든 책을 알고 있는 거대한 도서관입니다.
- 사용자가 입력하는 {인상깊게 읽었던 책}와 유사한 주제나 분위기의 책을 추천해줍니다.
- 사용자가 입력하는 {장르}에 해당하는 책을 추천해줍니다.
- 3가지 조건을 모두 만족하는 책만을 추천해줍니다.
"""

userContent = """
이기적 유전자, SF소설, 국내
"""

assistantContent = """
이기적 유전자와 유사한 주제를 가진 SF소설 중 국내 작가의 작품을 추천해드리겠습니다.

1. 우리가 빛의 속도로 갈 수 없다면 - 김초엽
인간의 삶과 가치에 대한 깊은 고민을 담은 SF소설로, 과학 기술의 발전과 인간의 삶의 관계를 다루고 있습니다.

2. 당신 인생의 이야기 - 테드 창
인간의 삶과 죽음, 그리고 인식의 문제를 다룬 SF소설로, 과학과 철학, 문학이 결합된 작품입니다.

3. 지구 끝의 온실 - 김초엽
지구의 멸망과 재건을 다룬 SF소설로, 인간의 삶과 자연의 관계를 다루고 있습니다.

위 작품들은 모두 국내 작가의 작품으로, 이기적 유전자와 유사한 주제를 가지고 있으며, SF소설의 장르적 특성을 잘 살린 작품들입니다.
"""

userContent2 = """
또 다른 책을 추천해 줘
"""


if __name__ == "__main__":
    completion_executor = CompletionExecutor()

    preset_text = [
        {
            "role": "system",
            "content": systemContent,
        },
        {"role": "user", "content": userContent},
        {"role": "assistant", "content": assistantContent},
        {"role": "user", "content": userContent2},
    ]

    request_data = {
        "messages": preset_text,
        "topP": 0.6,
        "topK": 0,
        "maxTokens": 512,
        "temperature": 0.5,
        "repeatPenalty": 1.2,
        "stopBefore": [],
        "includeAiFilters": True,
        "seed": 0,
    }

    print(preset_text)
    completion_executor.execute(request_data)
