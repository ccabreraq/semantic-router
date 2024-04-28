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
funcion1 = Route(
    name="funcion1|https://flowise-y3q2.onrender.com/api/v1/prediction/28e85d20-87ed-493d-8860-60241c9250e9",
    utterances=[
        "enviar un correo",
        "enviar un sms",
        "total de facturas",
        "cantidades de facturas o documentos",
        "calculadora",
		"sumar un numero con otro",
		"hacer operaciones matematicas",
    ],
)

# this could be used as an indicator to our chatbot to switch to a more
# conversational prompt
funcion2 = Route(
    name="funcion2|https://flowise-y3q2.onrender.com/api/v1/prediction/2229075d-471b-4a0d-a66a-b06ba1941ee2",
    utterances=[
        "verificar en ofac",
        "verificar una persona",
        "listas de lavados de activos",
        "listas restrictivas",
		"verifica a una persona",
		"lavado de activos",
    ],
)

no_permitido = Route(
    name="no_permitido|no_permitido",
    utterances=[
        "cuales son lo mejores politicos",
        "que opinas del presidente petro",
        "de que partido eres",
        "la politica es buena?",
        "quien salvra a este pais",
		"te gusta el sexo",
    ],
)

contrato = Route(
    name="contrato|https://flowise-y3q2.onrender.com/api/v1/prediction/dcdca554-2b89-4fb8-8443-3679784a369c",
    utterances=[
        "cuales son lo mejores politicos",
        "que opinas del presidente petro",
        "de que partido eres",
        "la politica es buena?",
        "quien salvra a este pais",
		"te gusta el sexo",
    ],
)

# we place both of our decisions together into single list
routes = [funcion1,funcion2,no_permitido,contrato]

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
	

