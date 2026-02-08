from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.search import router as search_router
from app.recommendation import router as rec_router
from app.onboarding import router as onboarding_router
from app.artist import router as artist_router
from app.player import router as player_router
from app.library import router as library_router

app = FastAPI(title="Scalable Music App API", version="1.0.0")

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(search_router.router, prefix="/api/search", tags=["Search"])
app.include_router(rec_router.router, prefix="/api/recommend", tags=["Recommendation"])
app.include_router(onboarding_router.router, prefix="/api/onboarding", tags=["Onboarding"])
app.include_router(artist_router.router, prefix="/api/artist", tags=["Artist"])
app.include_router(player_router.router, prefix="/api/player", tags=["Player"])
app.include_router(library_router.router, prefix="/api/library", tags=["Library"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Scalable Music App API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
