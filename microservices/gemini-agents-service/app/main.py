from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import gemini_agents

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


@app.get("/")
def status():
    return {"status": "OK"}
