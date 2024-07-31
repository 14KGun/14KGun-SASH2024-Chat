from dotenv import load_dotenv
from .test import testCompletion
from .common import ChatProvider
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


class ClovaChatProvider(ChatProvider):
    def __init__(self):
        self.completion_executor = CompletionExecutor()
        self.messages = [
            {
                "role": "system",
                "content": self.systemContent,
            },
        ]

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
    chat_provider = ClovaChatProvider()
    testCompletion(chat_provider)
