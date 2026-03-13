from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BannerBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    subtitle: Optional[str] = None
    image_url: str = Field(min_length=1, max_length=500)
    cta_primary_label: Optional[str] = Field(default=None, max_length=80)
    cta_primary_link: Optional[str] = Field(default=None, max_length=500)
    cta_secondary_label: Optional[str] = Field(default=None, max_length=80)
    cta_secondary_link: Optional[str] = Field(default=None, max_length=500)
    is_active: bool = True
    display_order: int = 0


class BannerCreate(BannerBase):
    pass


class BannerUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    subtitle: Optional[str] = None
    image_url: Optional[str] = Field(default=None, min_length=1, max_length=500)
    cta_primary_label: Optional[str] = Field(default=None, max_length=80)
    cta_primary_link: Optional[str] = Field(default=None, max_length=500)
    cta_secondary_label: Optional[str] = Field(default=None, max_length=80)
    cta_secondary_link: Optional[str] = Field(default=None, max_length=500)
    is_active: Optional[bool] = None
    display_order: Optional[int] = None


class BannerOut(BannerBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
