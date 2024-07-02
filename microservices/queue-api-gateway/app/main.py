from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import gemini_agents, user_chat

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    gemini_agents.router, prefix="/gemini-agents", tags=["gemini-agents"]
)
app.include_router(user_chat.router, prefix="/user-chat", tags=["user-chat"])


@app.get("/")
def status():
    return {"status": "OK"}
