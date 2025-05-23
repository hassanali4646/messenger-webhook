from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import httpx

app = FastAPI()

VERIFY_TOKEN = "fb_verify_8f72b13d2c7d4f15960c13d6"
PAGE_ACCESS_TOKEN = "EAAPFk9CFXT0BOZBLUWqgpQWg47EOaD3gLUe7r0NLeXcMZBpgqEqZA1gGV2XVsPvoTZAfZB7TBRZBWJpVZCiLgBOqSYqnm3yqJ7pRSHZBfiTMPOKonH1mGFlNpHEF09HZBNZBfmrETfgZBajPOa22B4YojJ9Lmuep2EbGZCH7defftaX4wZAojSk2i5WQ22zIqm4oNghUssZBXmzP8sf6fU1prGImPLicuXLwZDZD"

@app.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(content=challenge)
    else:
        return PlainTextResponse(content="Verification failed", status_code=403)


from fastapi import Request

@app.post("/webhook")
@app.post("/webhook")
async def receive_webhook(request: Request):
    body = await request.json()
    print("📩 Full Payload:", body)

    try:
        entry = body["entry"][0]
        messaging_event = entry["messaging"][0]

        sender_id = messaging_event["sender"]["id"]
        message_text = messaging_event["message"]["text"]

        print(f"👤 Sender ID: {sender_id}")
        print(f"💬 Message Text: {message_text}")

        # Send reply
        reply_payload = {
            "recipient": {"id": sender_id},
            "message": {"text": f"You said: {message_text}"}
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}",
                json=reply_payload
            )
            print("📤 Reply Response:", response.status_code, response.text)

    except Exception as e:
        print(f"⚠️ Error parsing or responding: {e}")

    return {"status": "ok"}

