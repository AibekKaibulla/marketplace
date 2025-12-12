from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from routers import auth, listings, categories, messages, favorites, photos
from database import engine
from admin import setup_admin
import models
import os

# Create all tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Marketplace API",
    description="API for student marketplace platform",
    version="1.0.0"
)

app.add_middleware(
    SessionMiddleware, 
    secret_key="secret_key_12345", # Simple key
    session_cookie="marketplace_session", # Unique name
    https_only=False,
    max_age=3600
)

@app.on_event("startup")
async def startup_event():
    # log all routes
    for route in app.routes:
        print(f"DEBUG: Found route: {route.path}")


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200", 
        "http://127.0.0.1:4200", 
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

# Create uploads directory and mount static files
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

# Setup Admin Panel - access at /admin
setup_admin(app, engine)

# Register routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(listings.router, prefix="/api/listings", tags=["Listings"])
app.include_router(categories.router, prefix="/api/categories", tags=["Categories"])
app.include_router(messages.router, prefix="/api/messages", tags=["Messages"])
app.include_router(favorites.router, prefix="/api/favorites", tags=["Favorites"])
app.include_router(photos.router, prefix="/api/photos", tags=["Photos"])


@app.get("/")
def read_root(request: Request):
    return {
        "message": "Student Marketplace API",
        "admin_panel": "http://localhost:8000/admin",
        "session_test": request.session.get("test_key", "no_session")
    }

@app.get("/test-session")
def test_session(request: Request):
    request.session["test_key"] = "session_working"
    # DEBUG: Force login as admin
    request.session["admin_user"] = "admin"
    return {"status": "session_set", "admin_user": "set"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Seed default categories on startup
@app.on_event("startup")
def seed_categories():
    from database import SessionLocal
    db = SessionLocal()
    try:
        # Check if categories exist
        if db.query(models.Category).count() == 0:
            default_categories = [
                {"name": "Textbooks", "icon": "📚"},
                {"name": "Electronics", "icon": "💻"},
                {"name": "Furniture", "icon": "🪑"},
                {"name": "Clothing", "icon": "👕"},
                {"name": "Gaming", "icon": "🎮"},
                {"name": "Musical Instruments", "icon": "🎸"},
                {"name": "Sports", "icon": "⚽"},
                {"name": "Other", "icon": "📦"}
            ]
            for cat in default_categories:
                db.add(models.Category(name=cat["name"], icon=cat["icon"]))
            db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)