from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, func

from app.db.base import Base


class Banner(Base):
    __tablename__ = "banners"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    subtitle = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=False)
    cta_primary_label = Column(String(80), nullable=True)
    cta_primary_link = Column(String(500), nullable=True)
    cta_secondary_label = Column(String(80), nullable=True)
    cta_secondary_link = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    display_order = Column(Integer, default=0, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
