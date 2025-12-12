from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import os
import uuid
import shutil
from database import get_db
from auth_utils import get_current_user

router = APIRouter()

# Create uploads directory
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_photo(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload a photo file and return the URL"""
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} not allowed. Use: {allowed_types}"
        )
    
    # Generate unique filename
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    unique_filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Return URL path
    url = f"/uploads/{unique_filename}"
    
    return {"url": url, "filename": unique_filename}


@router.post("/listing/{listing_id}", status_code=status.HTTP_201_CREATED)
async def add_photo_to_listing(
    listing_id: int,
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload and attach a photo to a listing"""
    # Verify listing exists and user owns it
    listing = db.query(models.Listing).filter(models.Listing.listing_id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    if listing.seller_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Generate unique filename
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    unique_filename = f"{uuid.uuid4()}.{ext}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Get current photo count for sort order
    photo_count = db.query(models.Photo).filter(models.Photo.listing_id == listing_id).count()
    
    # Create photo record
    photo = models.Photo(
        listing_id=listing_id,
        url=f"/uploads/{unique_filename}",
        alt_text=file.filename,
        sort_order=photo_count
    )
    db.add(photo)
    db.commit()
    db.refresh(photo)
    
    return {
        "photo_id": photo.photo_id,
        "url": photo.url,
        "alt_text": photo.alt_text
    }


@router.get("/listing/{listing_id}")
def get_listing_photos(listing_id: int, db: Session = Depends(get_db)):
    """Get all photos for a listing"""
    photos = db.query(models.Photo).filter(
        models.Photo.listing_id == listing_id
    ).order_by(models.Photo.sort_order).all()
    
    return [
        {"photo_id": p.photo_id, "url": p.url, "alt_text": p.alt_text}
        for p in photos
    ]


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_photo(
    photo_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a photo"""
    photo = db.query(models.Photo).filter(models.Photo.photo_id == photo_id).first()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    
    # Verify ownership
    listing = db.query(models.Listing).filter(models.Listing.listing_id == photo.listing_id).first()
    if listing.seller_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Delete file from disk
    file_path = os.path.join(UPLOAD_DIR, os.path.basename(photo.url))
    if os.path.exists(file_path):
        os.remove(file_path)
    
    db.delete(photo)
    db.commit()
    return None
