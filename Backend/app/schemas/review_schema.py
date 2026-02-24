from pydantic import BaseModel, Field
from typing import Optional

class ReviewCreate(BaseModel):
    product_id: int
    rating: int = Field(ge=1, le=5)
    comment: Optional[str]
    
class ReviewOut(BaseModel):
    id: int
    product_id: int
    buyer_id: int
    rating: int
    comment: Optional[str]
    
    class Config:
        from_attributes = True
        

