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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
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
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=os.getenv("DEBUG", "false").lower() == "true")