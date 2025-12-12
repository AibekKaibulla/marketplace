from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db
from auth_utils import get_current_user

router = APIRouter()


@router.get("", response_model=List[schemas.FavoriteResponse])
def get_favorites(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's favorites"""
    favorites = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.user_id
    ).order_by(models.Favorite.created_at.desc()).all()
    return favorites


@router.post("", response_model=schemas.FavoriteResponse, status_code=status.HTTP_201_CREATED)
def add_favorite(
    favorite: schemas.FavoriteCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Add a listing to favorites"""
    # Check if listing exists
    listing = db.query(models.Listing).filter(
        models.Listing.listing_id == favorite.listing_id
    ).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    # Check if already favorited
    existing = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.user_id,
        models.Favorite.listing_id == favorite.listing_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already in favorites")
    
    db_favorite = models.Favorite(
        user_id=current_user.user_id,
        listing_id=favorite.listing_id
    )
    
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    return db_favorite


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_favorite(
    listing_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Remove a listing from favorites"""
    favorite = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.user_id,
        models.Favorite.listing_id == listing_id
    ).first()
    
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    db.delete(favorite)
    db.commit()
    return None


@router.get("/check/{listing_id}")
def check_favorite(
    listing_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Check if a listing is in user's favorites"""
    favorite = db.query(models.Favorite).filter(
        models.Favorite.user_id == current_user.user_id,
        models.Favorite.listing_id == listing_id
    ).first()
    
    return {"is_favorite": favorite is not None}
