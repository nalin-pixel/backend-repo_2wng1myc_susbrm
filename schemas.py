"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
Each Pydantic model represents a collection in your database.

Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogpost" collection
"""

from pydantic import BaseModel, Field, HttpUrl, EmailStr
from typing import Optional, List
from datetime import datetime

# -----------------------------
# Tattoo Artist App Schemas
# -----------------------------

class TattooProduct(BaseModel):
    """
    Products the artist sells (prints, merch, vouchers)
    Collection name: "tattooproduct"
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in EUR")
    image_url: Optional[HttpUrl] = Field(None, description="Primary product image URL")
    category: str = Field(..., description="Category such as prints, merch, voucher")
    in_stock: bool = Field(True, description="Whether product is in stock")

class Review(BaseModel):
    """
    Client reviews for the artist
    Collection name: "review"
    """
    name: str = Field(..., description="Reviewer name")
    rating: int = Field(..., ge=1, le=5, description="Star rating 1-5")
    comment: str = Field(..., description="Review text")
    avatar_url: Optional[HttpUrl] = Field(None, description="Avatar image URL")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")

class GalleryItem(BaseModel):
    """
    Portfolio gallery items (healed tattoos, flashes, sketches)
    Collection name: "galleryitem"
    """
    image_url: HttpUrl = Field(..., description="Image URL")
    title: Optional[str] = Field(None, description="Title or short caption")
    tags: List[str] = Field(default_factory=list, description="Tags like blackwork, neo-trad")

class ContactMessage(BaseModel):
    """
    Contact/inquiry messages from the website
    Collection name: "contactmessage"
    """
    name: str = Field(..., description="Sender name")
    email: EmailStr = Field(..., description="Contact email")
    phone: Optional[str] = Field(None, description="Phone or WhatsApp")
    subject: Optional[str] = Field(None, description="Subject line")
    message: str = Field(..., description="Message body")
    consent: bool = Field(True, description="Consent to be contacted")

# Note: The Flames database viewer can read these via GET /schema
