from chat_clova import ChatProvider
from test import testText


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
