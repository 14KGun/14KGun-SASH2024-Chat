from chat import OpenaiChatProvider, testCompletion

if __name__ == "__main__":
    chat_provider = OpenaiChatProvider()
    testCompletion(chat_provider)
