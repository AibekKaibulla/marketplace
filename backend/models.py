from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Numeric, Boolean, SmallInteger, func
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    display_name = Column(String(100))
    role = Column(String(20), nullable=False, default="buyer")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    listings = relationship("Listing", back_populates="seller", cascade="all, delete-orphan")
    sent_messages = relationship("Message", foreign_keys="Message.sender_id", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="Message.receiver_id", back_populates="receiver")
    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "display_name": self.display_name,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)  # Your DB has this column
    icon = Column(String(50))

    # Relationships
    listings = relationship("Listing", back_populates="category")


class Listing(Base):
    __tablename__ = "listings"

    listing_id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id"), nullable=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    price = Column(Numeric(10, 2), nullable=False)
    condition = Column(String(20), default="good")
    quantity = Column(Integer, default=1)
    status = Column(String(20), default="published")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    view_count = Column(Integer, default=0)

    # Relationships
    seller = relationship("User", back_populates="listings")
    category = relationship("Category", back_populates="listings")
    favorites = relationship("Favorite", back_populates="listing", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="listing")
    photos = relationship("Photo", back_populates="listing", cascade="all, delete-orphan")


class Photo(Base):
    __tablename__ = "photos"
    
    photo_id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("listings.listing_id", ondelete="CASCADE"), nullable=False)
    url = Column(Text, nullable=False)
    alt_text = Column(String(255))
    sort_order = Column(Integer, default=0)
    
    # Relationships
    listing = relationship("Listing", back_populates="photos")


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    listing_id = Column(Integer, ForeignKey("listings.listing_id", ondelete="SET NULL"), nullable=True)
    body = Column(Text, nullable=False)  # Your DB uses 'body' not 'content'
    sent_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Your DB uses 'sent_at'
    read_at = Column(DateTime(timezone=True))  # Your DB has this
    is_read = Column(Boolean, default=False)

    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")
    listing = relationship("Listing", back_populates="messages")


class Favorite(Base):
    __tablename__ = "favorites"

    favorite_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    listing_id = Column(Integer, ForeignKey("listings.listing_id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="favorites")
    listing = relationship("Listing", back_populates="favorites")


class Order(Base):
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True, index=True)
    buyer_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    total_amount = Column(Numeric(12, 2), nullable=False)
    status = Column(String(30), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    paid_at = Column(DateTime(timezone=True))


class Review(Base):
    __tablename__ = "reviews"
    
    review_id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    listing_id = Column(Integer, ForeignKey("listings.listing_id"), nullable=False)
    rating = Column(SmallInteger, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())