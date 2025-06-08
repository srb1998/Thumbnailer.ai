from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from routes.api import router
import os

app = FastAPI(
    title="ThumbnailGuru - Secret of Viral Videos",
    description="AI-powered YouTube thumbnail generator",
    version="1.0.0"
)

# CORS middleware
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "https://thumbnailer-ai.vercel.app",
]

if os.getenv("ENVIRONMENT") == "development":
    allowed_origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Static files
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routes
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "YouTube Thumbnail AI is running!"}

@app.get("/test")
async def answer():
    return {"message": "Successfully working"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=port, 
        reload=os.getenv("DEBUG", "false").lower() == "true"
    )