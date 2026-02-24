from pydantic import BaseModel, Field
from typing import Optional, List

class ProductCreate(BaseModel):
    title: str = Field(min_length=3)
    description: Optional[str]
    price: int = Field(gt=0)
    stock: int = Field(ge=0)
    images: Optional[List[str]]
    category: Optional[str]
    is_active: bool = True

class ProductUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[int]
    images: Optional[List[str]]
    category: Optional[str]
    is_active: Optional[bool]

class StockUpdate(BaseModel):
    stock: int = Field(ge=0)
    
class ProductOut(BaseModel):
    id: int
    seller_id: int
    title: str
    description: Optional[str]
    price: int
    stock: int
    images: Optional[List]
    category: Optional[str]
    id_active: bool
    average_rating: int
    
    class Config:
        from_attributes = True
