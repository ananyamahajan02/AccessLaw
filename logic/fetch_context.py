import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

def fetch_context_from_rag(question):
    try:
        payload = {
            "query": question,
            "top_k": 3,
            "rerank": False,
            "include_scores": False,
            "filters": {}
        }
        res = requests.post(API_KEY, json=payload)
        res.raise_for_status()
        results = res.json().get("results", [])
        if results:
            chunks = [r.get("content", "") for r in results]
            return "\n".join([f"{i+1}. {c.strip()}" for i, c in enumerate(chunks)])
        return "No relevant context found."
    except Exception as e:
        print("❌ Error fetching context:", e)
        return "Error retrieving context."
