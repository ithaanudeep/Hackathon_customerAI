from fastapi import FastAPI
import openai
from pydantic import BaseModel
from app.generate import generate_answer
from app.retrieval import fetch_relevant_docs
from app.database import collection
from app.embeddings import get_embedding
import logging
from textblob import TextBlob 
from app.database import cluster  # Import the cluster object

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Define JSON models
class QueryRequest(BaseModel):
    id: str
    query: str
    category: str

# class KnowledgeEntry(BaseModel):
#     id: str
#     text: str

class Feedback(BaseModel):
    id: str
    query: str
    answer: str
    feedback_score: int
    category: str

def analyze_sentiment(text):
    """Performs sentiment analysis using TextBlob (returns Positive, Neutral, or Negative)."""
    sentiment_score = TextBlob(text).sentiment.polarity  # Score between -1 and 1
    if sentiment_score > 0.1:
        return "Positive"
    elif sentiment_score < -0.1:
        return "Negative"
    else:
        return "Neutral"

def classify_intent(text):
    """Uses OpenAI's GPT-3.5 to classify user intent."""
    prompt = f"Classify the following customer query into one of the intents: returns, complaint, general inquiry, pricing, technical support.\nQuery: {text}\nIntent:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"].strip()


# Query endpoint to generate AI response
@app.post("/query")
def query_model(request: QueryRequest):
    answer = generate_answer(request.query)
    text = request.query + " " + answer
    embedding = get_embedding(text)
    sentiment = analyze_sentiment(request.query)
    intent = classify_intent(request.query)
    doc = {"id": request.id, "text": text, "embedding": embedding, "category": request.category,"sentiment":sentiment, "intent":intent}
    collection.insert(request.id, doc)
    return {"answer": answer, "sentiment":sentiment, "intent":intent}

# Store knowledge base entries
# @app.post("/store_knowledge")
# def store_knowledge(entry: KnowledgeEntry):
#     embedding = get_embedding(entry.text)
#     doc = {"id": entry.id, "text": entry.text, "embedding": embedding}
#     collection.insert(entry.id, doc)
#     return {"message": "Knowledge stored successfully"}

# Store user feedback for AI improvements
@app.post("/feedback")
def store_feedback(feedback: Feedback):
    feedback_entry = feedback.dict()
    doc_key = "feedback:" + feedback.query

    if feedback.feedback_score <= 2:
        logging.warning("⚠️ Low feedback detected! Generating an improved response.")

        # Step 1: Generate a better response using GPT-3.5
        improved_answer = generate_answer(feedback.query)

        # Step 2: Store both the old and improved response
        low_feedback_doc = {
            "id": feedback.id,
            "query": feedback.query,
            "old_answer": feedback.answer,
            "improved_answer": improved_answer,
            "category": feedback.category,
            "feedback_score": feedback.feedback_score
        }
        collection.upsert(feedback.id, low_feedback_doc)

        # Step 3: Update the knowledge base with the improved response
        """knowledge_entry = {
            "id": "faq:improved:" + feedback.query,
            "text": improved_answer
        }
        collection.upsert("faq:improved:" + feedback.query, knowledge_entry)"""

        # Step 4: Return improved response with additional message (not stored in DB)
        return {
            "improved_answer": improved_answer,
            "message": "If you are not satisfied with the response given, please contact our customer team."
        }

    # Store feedback normally if score >2
    collection.upsert(feedback.id, feedback_entry)
    return {"message": "Feedback stored successfully"}

@app.get("/dashboard")
def get_dashboard_stats():
    try:
        total_queries_result = cluster.query("SELECT COUNT(*) as count FROM `hackathon` WHERE category LIKE 'HOW_TO_RETURN%';")
        total_queries = list(total_queries_result)[0]['count'] if total_queries_result else 0

        low_feedback_result = cluster.query("SELECT COUNT(*) as count FROM `hackathon` WHERE META().id LIKE 'low_feedback:%'")
        print(low_feedback_result)
        low_feedback_count = list(low_feedback_result)[0]['count'] if low_feedback_result else 0

        return {
            "total_queries": total_queries,
            "low_feedback_entries": low_feedback_count,
            "message": "Dashboard showing real-time AI performance insights."
        }
    except Exception as e:
        return {"error": str(e)}

