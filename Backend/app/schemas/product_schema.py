from pydantic import BaseModel, Field
from typing import Optional, List

class ProductCreate(BaseModel):
    title: str = Field(min_length=3)
    description: Optional[str] = None
    price: int = Field(gt=0)
    stock: int = Field(ge=0)
    images: Optional[List[str]] = None
    category: Optional[str] = None
    is_active: bool = True

class ProductUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3)
    description: Optional[str] = None
    price: Optional[int] = Field(default=None, gt=0)
    stock: Optional[int] = Field(default=None, ge=0)
    images: Optional[List[str]] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None

class StockUpdate(BaseModel):
    stock: int = Field(ge=0)
    
class ProductOut(BaseModel):
    id: int
    seller_id: int
    title: str
    description: Optional[str] = None
    price: int
    stock: int
    images: Optional[List] = None
    category: Optional[str] = None
    is_active: bool = True
    average_rating: float = 0.0
    
    class Config:
        from_attributes = True
