import numpy as np
from scipy.spatial.distance import cosine
from app.database import cluster, COUCHBASE_BUCKET
from app.embeddings import get_embedding

def fetch_relevant_docs(query, top_k=3):
    query_embedding = get_embedding(query)
    #WHERE META().id LIKE 'faq:%' OR META().id LIKE 'footwear:%'
    query_text = f"SELECT text, embedding FROM `{COUCHBASE_BUCKET}`"
    results = cluster.query(query_text)

    documents = []
    for row in results:
        #print("DEBUG - Couchbase row:", row)  # Debugging line
        documents.append(row)

    if not documents:
        print("DEBUG - No matching documents found in Couchbase.")
        return ["No relevant information found."]

    similarities = [(doc.get("text", "UNKNOWN"), 1 - cosine(query_embedding, doc.get("embedding", [])))
                    for doc in documents if "embedding" in doc]

    sorted_docs = sorted(similarities, key=lambda x: x[1], reverse=True)

    return [doc[0] for doc in sorted_docs[:top_k]]
