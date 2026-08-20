from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.resume_routes import router as resume_router
from app.routes.retrieval_routes import router as retrieval_router
from app.routes.query_routes import router as query_router
from app.routes.voice_routes import router as voice_router
app = FastAPI(
    title="AI Resume Voice Agent",
    description="Voice-based AI Resume Information Retrieval Agent",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume_router)
app.include_router(retrieval_router)
app.include_router(query_router)
app.include_router(voice_router)

@app.get("/")
def home():
    return {
        "message": "AI Resume Voice Agent Backend is running"
    }