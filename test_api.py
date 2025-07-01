from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-nano-2025-04-14",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)