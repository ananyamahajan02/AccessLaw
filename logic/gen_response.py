# logic/response_generator.py

import os
from openai import OpenAI
from dotenv import load_dotenv
import re
load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

def generate_response(question, context):
    prompt = f"""Answer the following legal query in a detailed and structured manner. *Do not exceed 1600 words and do not give incomplete output*. Include relevant examples and explanations if possible.Format key points in *bold* and examples in _italics_ using WhatsApp-compatible formatting.


Question: {question}

Context:
{context}

Answer:"""

    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": os.getenv("REFERER_URL"),
                "X-Title": "Local WhatsApp Bot"
            },
            model=os.getenv("OPENROUTER_MODEL"),
            messages=[
                {"role": "system", "content": "You are a legal AI assistant specializing in Indian law. Provide accurate, detailed responses based on the legal documents provided. If the query is not based on the legal context provided, handle it ***without using the context and DONOT mention the same in answers***. Always cite specific sections and sources in your responses. Be professional and precise in your language.Do not add anything like the context provided is wrong in your answers"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024, 
            temperature=0.2,
        )
        raw_response = completion.choices[0].message.content.strip()
        return format_response(raw_response)

    except Exception as e:
        print("❌ Error from OpenRouter:", e)
        return "Sorry, I couldn't generate a response at the moment."

def format_response(text: str) -> str:
    text = re.sub(r'^- ', '• ', text, flags=re.MULTILINE)                  
    text = re.sub(r'\n{3,}', '\n\n', text)                                 
    text = re.sub(r' +', ' ', text)                                        
    return text.strip()

