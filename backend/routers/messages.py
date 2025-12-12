from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List
import models
import schemas
from database import get_db
from auth_utils import get_current_user

router = APIRouter()


@router.get("/conversations", response_model=List[schemas.ConversationResponse])
def get_conversations(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all conversations for current user"""
    
    # Get the actual messages with their latest timestamps
    messages = db.query(models.Message).filter(
        or_(
            models.Message.sender_id == current_user.user_id,
            models.Message.receiver_id == current_user.user_id
        )
    ).order_by(models.Message.sent_at.desc()).all()  # Use sent_at
    
    # Build unique conversations
    seen_conversations = set()
    conversations = []
    
    for msg in messages:
        other_user_id = msg.receiver_id if msg.sender_id == current_user.user_id else msg.sender_id
        conv_key = (other_user_id, msg.listing_id)
        
        if conv_key not in seen_conversations:
            seen_conversations.add(conv_key)
            
            other_user = db.query(models.User).filter(models.User.user_id == other_user_id).first()
            listing = None
            if msg.listing_id:
                listing = db.query(models.Listing).filter(models.Listing.listing_id == msg.listing_id).first()
            
            # Count unread messages
            unread_count = db.query(models.Message).filter(
                models.Message.sender_id == other_user_id,
                models.Message.receiver_id == current_user.user_id,
                models.Message.is_read == False
            ).count()
            
            conversations.append(schemas.ConversationResponse(
                user=schemas.UserBrief(
                    user_id=other_user.user_id,
                    username=other_user.username,
                    display_name=other_user.display_name
                ),
                listing=schemas.ListingBrief(
                    listing_id=listing.listing_id,
                    title=listing.title,
                    price=listing.price
                ) if listing else None,
                last_message=schemas.MessageResponse(
                    message_id=msg.message_id,
                    sender_id=msg.sender_id,
                    receiver_id=msg.receiver_id,
                    listing_id=msg.listing_id,
                    body=msg.body,  # Use body
                    is_read=msg.is_read,
                    sent_at=msg.sent_at,  # Use sent_at
                    sender=schemas.UserBrief(
                        user_id=msg.sender.user_id,
                        username=msg.sender.username,
                        display_name=msg.sender.display_name
                    )
                ),
                unread_count=unread_count
            ))
    
    return conversations


@router.get("/conversation/{user_id}", response_model=List[schemas.MessageResponse])
def get_conversation_messages(
    user_id: int,
    listing_id: int = Query(None, description="Filter by listing"),
    limit: int = Query(50, ge=1, le=100),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get messages between current user and another user"""
    query = db.query(models.Message).filter(
        or_(
            and_(models.Message.sender_id == current_user.user_id, models.Message.receiver_id == user_id),
            and_(models.Message.sender_id == user_id, models.Message.receiver_id == current_user.user_id)
        )
    )
    
    if listing_id:
        query = query.filter(models.Message.listing_id == listing_id)
    
    messages = query.order_by(models.Message.sent_at.asc()).limit(limit).all()  # Use sent_at
    
    # Mark messages as read
    db.query(models.Message).filter(
        models.Message.sender_id == user_id,
        models.Message.receiver_id == current_user.user_id,
        models.Message.is_read == False
    ).update({"is_read": True})
    db.commit()
    
    return messages


@router.post("", response_model=schemas.MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    message: schemas.MessageCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Send a message to another user"""
    # Validate receiver exists
    receiver = db.query(models.User).filter(models.User.user_id == message.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")
    
    if message.receiver_id == current_user.user_id:
        raise HTTPException(status_code=400, detail="Cannot send message to yourself")
    
    # Validate listing if provided
    if message.listing_id:
        listing = db.query(models.Listing).filter(models.Listing.listing_id == message.listing_id).first()
        if not listing:
            raise HTTPException(status_code=404, detail="Listing not found")
    
    db_message = models.Message(
        sender_id=current_user.user_id,
        receiver_id=message.receiver_id,
        listing_id=message.listing_id,
        body=message.body  # Use body
    )
    
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message


@router.put("/{message_id}/read", response_model=schemas.MessageResponse)
def mark_message_read(
    message_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Mark a message as read"""
    message = db.query(models.Message).filter(
        models.Message.message_id == message_id,
        models.Message.receiver_id == current_user.user_id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    message.is_read = True
    db.commit()
    db.refresh(message)
    return message
