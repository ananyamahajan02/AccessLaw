from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Request, Response
import os
import json

from utils.webhook_verify import verify_webhook
from logic.fetch_context import fetch_context_from_rag
from logic.gen_response import generate_response 
from logic.send_wp import send_whatsapp_message

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "WhatsApp bot is running with local Flan-T5!"}

@app.get("/webhook")
async def verify(request: Request):
    return await verify_webhook(request)

from fastapi import Request
import json

last_message_id = None

@app.post("/webhook")
async def receive_message(request: Request):
    global last_message_id

    body = await request.json()
    print("📥 Incoming message:", json.dumps(body, indent=2))

    try:
        change = body["entry"][0]["changes"][0]["value"]
        if "messages" not in change:
            return {"status": "ignored - not a message"}
        message = change["messages"][0]
        if message.get("from") == change.get("metadata", {}).get("phone_number_id"):
            print("⚠️ Echo message from bot itself. Skipping.")
            return {"status": "ignored - echo"}

        msg_id = message.get("id")
        if msg_id == last_message_id:
            print("⚠️ Duplicate message. Skipping.")
            return {"status": "ignored - duplicate"}
        last_message_id = msg_id

        sender_id = message["from"]
        if message.get("type") != "text":
            return {"status": "ignored - not a text message"}
        user_text = message.get("text", {}).get("body", "").strip()
        
        if not user_text or user_text.isspace():
            return {"status": "ignored - empty or blank message"}
        
        context = fetch_context_from_rag(user_text)
        reply = generate_response(user_text, context)
        send_whatsapp_message(sender_id, reply)

        return {"status": "message processed"}

    except Exception as e:
        print("❌ Unexpected Error:", str(e))
        return {"status": "error", "message": str(e)}
