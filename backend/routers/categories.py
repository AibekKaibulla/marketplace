from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from database import get_db

router = APIRouter()


@router.get("", response_model=List[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Get all categories"""
    categories = db.query(models.Category).order_by(models.Category.name).all()
    return categories


@router.post("", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db)
):
    """Create a new category (admin only in production)"""
    # Check if category already exists
    existing = db.query(models.Category).filter(models.Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    
    db_category = models.Category(
        name=category.name,
        icon=category.icon
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


@router.get("/{category_id}", response_model=schemas.CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Get a single category"""
    category = db.query(models.Category).filter(models.Category.category_id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
