from dotenv import load_dotenv
import requests
import json
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


def constant(func):
    def func_set(self, value):
        raise TypeError

    def func_get(self):
        return func()

    return property(func_get, func_set)


class CompletionExecutor:
    def __init__(self):
        self.host = "https://clovastudio.stream.ntruss.com"
        self.model_name = "HCX-003"

    def execute(self, messages) -> str:
        responses = []
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
            json={
                "messages": messages,
                "topP": 0.6,
                "topK": 0,
                "maxTokens": 512,
                "temperature": 0.5,
                "repeatPenalty": 1.2,
                "stopBefore": [],
                "includeAiFilters": True,
                "seed": 0,
            },
            stream=True,
        ) as r:
            for line in r.iter_lines():
                if line:
                    text = line.decode("utf-8")
                    if text.startswith("data:"):
                        try:
                            response = json.loads(text[5:])
                            content = response["message"]["content"]
                            assert type(content) == str
                            responses.append(content)
                        except Exception as e:
                            pass
        return "".join(responses)


class ChatProvider:
    def __init__(self) -> str:
        self.completion_executor = CompletionExecutor()
        self.messages = [
            {
                "role": "system",
                "content": self.systemContent,
            },
        ]

    @constant
    def systemContent():
        return """
            - 당신은 전 세계의 모든 책을 알고 있는 거대한 도서관입니다.
            - 사용자가 입력하는 {인상깊게 읽었던 책}와 유사한 주제나 분위기의 책을 추천해줍니다.
            - 사용자가 입력하는 {장르}에 해당하는 책을 추천해줍니다.
            - 3가지 조건을 모두 만족하는 책만을 추천해줍니다.
        """

    def add_message(self, message) -> str:
        assert (
            self.messages[-1]["role"] == "assistant"
            or self.messages[-1]["role"] == "system"
        )
        self.messages.append({"role": "user", "content": message})
        response = self.completion_executor.execute(self.messages)
        self.messages.append({"role": "assistant", "content": response})
        return response
