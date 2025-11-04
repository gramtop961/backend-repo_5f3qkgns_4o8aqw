"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (you can keep using these if needed)
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# App-specific schemas
class OrderItem(BaseModel):
    name: str
    price: float
    quantity: int = Field(..., ge=1)
    category: Optional[str] = None

class Order(BaseModel):
    customer_name: str = Field(..., min_length=2)
    phone: str = Field(..., min_length=8, max_length=15)
    payment_method: str = Field(..., description="cod or upi")
    items: List[OrderItem]
    subtotal: float
    discount: float = 0.0
    total: float
    notes: Optional[str] = None
