from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth
from database import engine
import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Marketplace API",
    description="API for student marketplace platform",
    version="1.0.0"
)

# CORS Configuration - must be added before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],  # Allow both localhost variants
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicitly include OPTIONS
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,  # Cache preflight requests for 10 minutes
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

@app.get("/")
def read_root():
    return {"message": "Student Marketplace API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)