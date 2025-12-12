from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


# ============== User Schemas ==============

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    display_name: Optional[str] = Field(None, max_length=100)
    role: str = Field(default="buyer", pattern="^(buyer|seller|both|admin)$")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @field_validator('username')
    @classmethod
    def validate_username(cls, v):
        if not v.replace('_', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, and underscores')
        return v



class UserUpdate(BaseModel):
    display_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    role: Optional[str] = Field(None, pattern="^(buyer|seller|both|admin)$")


class PasswordChange(BaseModel):
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=6)



class UserResponse(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserBrief(BaseModel):
    """Minimal user info for embedding in other responses"""
    user_id: int
    username: str
    display_name: Optional[str] = None

    class Config:
        from_attributes = True


# ============== Auth Schemas ==============

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


# ============== Category Schemas ==============

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    icon: Optional[str] = Field(None, max_length=50)


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    category_id: int

    class Config:
        from_attributes = True


# ============== Photo Schemas ==============

class PhotoResponse(BaseModel):
    photo_id: int
    url: str
    alt_text: Optional[str] = None
    sort_order: int = 0

    class Config:
        from_attributes = True


# ============== Listing Schemas ==============

class ListingBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = None
    price: Decimal = Field(..., ge=0)
    condition: str = Field(default="good", pattern="^(brand-new|like-new|good|fair|poor)$")
    quantity: int = Field(default=1, ge=1)


class ListingCreate(ListingBase):
    category_id: Optional[int] = None
    status: str = Field(default="published", pattern="^(published|draft|sold)$")


class ListingUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=255)
    description: Optional[str] = None
    price: Optional[Decimal] = Field(None, ge=0)
    condition: Optional[str] = Field(None, pattern="^(brand-new|like-new|good|fair|poor)$")
    quantity: Optional[int] = Field(None, ge=1)
    category_id: Optional[int] = None
    status: Optional[str] = Field(None, pattern="^(published|draft|sold)$")


class ListingResponse(ListingBase):
    listing_id: int
    seller_id: int
    category_id: Optional[int] = None
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    view_count: int = 0
    seller: UserBrief
    category: Optional[CategoryResponse] = None
    photos: List[PhotoResponse] = []

    class Config:
        from_attributes = True


class ListingBrief(BaseModel):
    """Minimal listing info for embedding"""
    listing_id: int
    title: str
    price: Decimal

    class Config:
        from_attributes = True


# ============== Message Schemas ==============

class MessageCreate(BaseModel):
    receiver_id: int
    listing_id: Optional[int] = None
    body: str = Field(..., min_length=1)  # Match DB column name


class MessageResponse(BaseModel):
    message_id: int
    sender_id: int
    receiver_id: int
    listing_id: Optional[int] = None
    body: str  # Match DB column name
    is_read: bool
    sent_at: datetime  # Match DB column name
    sender: UserBrief

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    """Represents a conversation with another user"""
    user: UserBrief
    listing: Optional[ListingBrief] = None
    last_message: Optional[MessageResponse] = None
    unread_count: int = 0


# ============== Favorite Schemas ==============

class FavoriteCreate(BaseModel):
    listing_id: int


class FavoriteResponse(BaseModel):
    favorite_id: int
    user_id: int
    listing_id: int
    created_at: datetime
    listing: ListingResponse

    class Config:
        from_attributes = True


# ============== Stats Schemas ==============

class UserStats(BaseModel):
    active_listings: int = 0
    completed_sales: int = 0
    rating: float = 5.0