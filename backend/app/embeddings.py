import openai
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def get_embedding(text, model="text-embedding-ada-002"):
    response = openai.Embedding.create(
        model=model,
        input=text
    )
    return response.data[0].embedding