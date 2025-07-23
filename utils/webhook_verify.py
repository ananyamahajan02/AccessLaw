import os 
from fastapi import Request, Response
from fastapi.responses import PlainTextResponse , JSONResponse
from dotenv import load_dotenv
load_dotenv()
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

async def verify_webhook(request: Request):
    params = dict(request.query_params)
    print("DEBUG webhook params:", params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")
    
    print(f"Mode: {mode}, Token from request: {token}, Expected token: {VERIFY_TOKEN}")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Verification succeeded")
        return PlainTextResponse(content=challenge, status_code=200)
    else:
        print("❌ Verification failed")
        return JSONResponse(content={"status": "Invalid verify token"}, status_code=403)
