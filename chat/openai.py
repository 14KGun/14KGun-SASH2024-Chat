from dotenv import load_dotenv
from openai import OpenAI
import os


# load environment variables
load_dotenv()
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"] if "OPENAI_API_KEY" in os.environ else ""

client = OpenAI(api_key=OPENAI_API_KEY)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
        },
        {
            "role": "user",
            "content": "Compose a poem that explains the concept of recursion in programming.",
        },
    ],
)

print(completion.choices[0].message)
