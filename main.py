from chat import ChatProvider

if __name__ == "__main__":
    chat_provider = ChatProvider()
    print(chat_provider.add_message("이기적 유전자, SF소설, 국내"))
    print(chat_provider.add_message("1번 책에 대해서 더 자세히 설명해 줘"))
    print(chat_provider.add_message("또 다른 책을 추천해 줘"))
