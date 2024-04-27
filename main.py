import os
import uvicorn
import asyncio

from fastapi import FastAPI, Request
from fastapi import File, UploadFile, Form

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse

from semantic_router import Route
from semantic_router.encoders import  OpenAIEncoder



# or for OpenAI
encoder = OpenAIEncoder()
from semantic_router.layer import RouteLayer



app = FastAPI()

##----------------- pandasai ---------------------
app.uid = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT","OPTIONS"],
    allow_headers=["*"],
)


# we could use this as a guide for our chatbot to avoid political conversations
politics = Route(
    name="politics - ggggggggggggggggggggggggggggggg",
    utterances=[
        "cuales son lo mejores politicos",
        "que opinas del presidente petro",
        "de que partido eres",
        "la politica es buena?",
        "quien salvra a este pais",
    ],
)

# this could be used as an indicator to our chatbot to switch to a more
# conversational prompt
chitchat = Route(
    name="chitchat",
    utterances=[
        "how's the weather today?",
        "how are things going?",
        "lovely weather today",
        "the weather is horrendous",
        "let's go to the chippy",
    ],
)

# we place both of our decisions together into single list
routes = [politics, chitchat]

rl = RouteLayer(encoder=encoder, routes=routes)

@app.post("/semantic-router")
async def chat_agent(info : Request):
	"""Returns an AI-generated response to a user conversation, based on limited prior context."""
	req_info = await info.json()	
	mensajes =req_info["messages"]
	uid = req_info["uid"]
	ultimo = len(req_info["messages"])-1
	content = mensajes[ultimo]["content"]

	resp1 = rl(content).name
	print(resp1)
	
	return resp1
	

