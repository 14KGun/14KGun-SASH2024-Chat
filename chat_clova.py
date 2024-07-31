from dotenv import load_dotenv
from test import testText
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
            - 당신은 '마이리틀닥터'라는 서비스의 약사입니다.
            - 당신은 거의 모든 약의 정보를 알고 있고 각 약의 부작용과 주의 사항을 아는 약사입니다.
            - 사용자에게 복용하려는 약들의 이름과 특징, 부작용, 주의사항이 담긴 JSON을 입력받습니다. 그럼 당신은 약에 대한 정보를 받았다고 짧게만 응답해주세요.
            - 사용자의 답변으로 JSON 형태를 입력 받을 수 있다는 것을 알려주지 않아도 됩니다.
            - 당신은 약에 대한 정보 외에 사용자들의 질문을 받습니다.
            - 약 복용 시 함께 먹어도 되는 음식에 대해서 사용자에게 질문 받을 수 있습니다.
            - 약 복용 시 나타나는 부작용 및 증상에 대해서 사용자에게 질문 받을 수 있습니다.
            - 다른 약물과 복용 시 주의사항에 대해서 사용자에게 질문 받을 수 있습니다.
            - '사용자님'이라는 말을 사용하여 사용자에게 응답하지 않아도 됩니다.
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


if __name__ == "__main__":
    chat_provider = ChatProvider()
    chat_provider.add_message(testText["info1"])
    chat_provider.add_message(testText["info2"])

    print("Q1. {}".format(testText["question1"]))
    print(chat_provider.add_message(testText["question1"]))

    print("")
    print("Q2. {}".format(testText["question2"]))
    print(chat_provider.add_message(testText["question2"]))

    print("")
    print("Q3. {}".format(testText["question3"]))
    print(chat_provider.add_message(testText["question3"]))
