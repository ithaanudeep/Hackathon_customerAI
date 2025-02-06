import openai
from app.retrieval import fetch_relevant_docs
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_answer(query):
    context = fetch_relevant_docs(query)
    context_text = "\n\n".join(context)

    prompt = f"""
    You are an AI assistant answering user queries. Use the provided context to answer.
    
    Context:
    {context_text}
    
    Question: {query}
    
    Answer:
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content
