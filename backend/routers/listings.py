from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
import models
import schemas
from database import get_db
from auth_utils import get_current_user

router = APIRouter()


@router.get("", response_model=List[schemas.ListingResponse])
def get_listings(
    search: Optional[str] = Query(None, description="Search in title and description"),
    category_id: Optional[int] = Query(None, description="Filter by category"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price"),
    condition: Optional[str] = Query(None, description="Filter by condition"),
    status: str = Query("published", description="Filter by status"),
    sort_by: str = Query("newest", description="Sort by: newest, oldest, price_low, price_high"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get all listings with optional filters and sorting"""
    query = db.query(models.Listing).filter(models.Listing.status == status)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                models.Listing.title.ilike(search_term),
                models.Listing.description.ilike(search_term)
            )
        )
    
    if category_id:
        query = query.filter(models.Listing.category_id == category_id)
    
    if min_price is not None:
        query = query.filter(models.Listing.price >= min_price)
    
    if max_price is not None:
        query = query.filter(models.Listing.price <= max_price)
    
    if condition:
        query = query.filter(models.Listing.condition == condition)
    
    # Apply sorting
    if sort_by == "oldest":
        query = query.order_by(models.Listing.created_at.asc())
    elif sort_by == "price_low":
        query = query.order_by(models.Listing.price.asc())
    elif sort_by == "price_high":
        query = query.order_by(models.Listing.price.desc())
    else:  # newest (default)
        query = query.order_by(models.Listing.created_at.desc())
    
    listings = query.offset(offset).limit(limit).all()
    return listings


@router.get("/{listing_id}", response_model=schemas.ListingResponse)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    """Get a single listing by ID and increment view count"""
    listing = db.query(models.Listing).filter(models.Listing.listing_id == listing_id).first()
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    # Increment view count
    listing.view_count = (listing.view_count or 0) + 1
    db.commit()
    db.refresh(listing)
    
    return listing


@router.post("", response_model=schemas.ListingResponse, status_code=status.HTTP_201_CREATED)
def create_listing(
    listing: schemas.ListingCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new listing"""
    # Validate category if provided
    if listing.category_id:
        category = db.query(models.Category).filter(
            models.Category.category_id == listing.category_id
        ).first()
        if not category:
            raise HTTPException(status_code=400, detail="Invalid category")
    
    db_listing = models.Listing(
        seller_id=current_user.user_id,
        category_id=listing.category_id,
        title=listing.title,
        description=listing.description,
        price=listing.price,
        condition=listing.condition,
        quantity=listing.quantity,
        status=listing.status
    )
    
    db.add(db_listing)
    db.commit()
    db.refresh(db_listing)
    return db_listing


@router.put("/{listing_id}", response_model=schemas.ListingResponse)
def update_listing(
    listing_id: int,
    listing_update: schemas.ListingUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a listing (owner only)"""
    db_listing = db.query(models.Listing).filter(models.Listing.listing_id == listing_id).first()
    
    if not db_listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    if db_listing.seller_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this listing")
    
    # Update only provided fields
    update_data = listing_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_listing, field, value)
    
    db.commit()
    db.refresh(db_listing)
    return db_listing


@router.delete("/{listing_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_listing(
    listing_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a listing (owner only)"""
    db_listing = db.query(models.Listing).filter(models.Listing.listing_id == listing_id).first()
    
    if not db_listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    
    if db_listing.seller_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this listing")
    
    db.delete(db_listing)
    db.commit()
    return None


@router.get("/user/{user_id}", response_model=List[schemas.ListingResponse])
def get_user_listings(
    user_id: int,
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get all listings by a specific user"""
    query = db.query(models.Listing).filter(models.Listing.seller_id == user_id)
    
    if status:
        query = query.filter(models.Listing.status == status)
    
    listings = query.order_by(models.Listing.created_at.desc()).all()
    return listings


@router.get("/me/listings", response_model=List[schemas.ListingResponse])
def get_my_listings(
    status: Optional[str] = Query(None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's listings"""
    query = db.query(models.Listing).filter(models.Listing.seller_id == current_user.user_id)
    
    if status:
        query = query.filter(models.Listing.status == status)
    
    listings = query.order_by(models.Listing.created_at.desc()).all()
    return listings
