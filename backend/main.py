# backend/main.py
from fastapi import FastAPI, Form
from fastapi.responses import ORJSONResponse, PlainTextResponse
from pydantic import BaseModel
from xml.etree.ElementTree import Element, tostring

from backend.ai_agent import graph, SYSTEM_PROMPT, parse_response

app = FastAPI(title="MentMe – AI Mental Health Backend")

class Query(BaseModel):
    message: str


# api endpoints 
@app.post("/ask")
async def ask(query: Query):
    inputs = {
        "messages": [
            ("system", SYSTEM_PROMPT),
            ("user", query.message),
        ]
    }

    stream = graph.stream(inputs, stream_mode="updates")
    tool_called_name, final_response = parse_response(stream)

    return ORJSONResponse(
        content={
            "response": final_response,
            "tool_called": tool_called_name,
        }
    )
# twilio whatsapp
def _twiml_message(body: str) -> PlainTextResponse:
    """Create minimal TwiML <Response><Message>...</Message></Response>"""
    response_el = Element("Response")
    message_el = Element("Message")
    message_el.text = body
    response_el.append(message_el)
    xml_bytes = tostring(response_el, encoding="utf-8")

    return PlainTextResponse(
        content=xml_bytes,
        media_type="application/xml",
    )

# endpoints for whatsapp
@app.post("/whatsapp_ask")
async def whatsapp_ask(Body: str = Form(...)):
    user_text = Body.strip() if Body else ""

    inputs = {
        "messages": [
            ("system", SYSTEM_PROMPT),
            ("user", user_text),
        ]
    }
    stream = graph.stream(inputs, stream_mode="updates")
    tool_called_name, final_response = parse_response(stream)

    if not final_response:
        final_response = (
            "I'm here with you, but I couldn't generate a response just now."
        )
    return _twiml_message(final_response)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
