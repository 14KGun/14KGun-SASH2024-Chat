from dotenv import load_dotenv
from openai import OpenAI
from .common import ChatProvider
import os


# load environment variables
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"] if "OPENAI_API_KEY" in os.environ else ""


class OpenaiChatProvider(ChatProvider):
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.model_name = "gpt-4o-mini"
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

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages,
        )
        response = completion.choices[0].message.content
        self.messages.append({"role": "assistant", "content": response})
        return response
