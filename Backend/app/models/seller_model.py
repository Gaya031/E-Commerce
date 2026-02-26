import enum
from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey, DateTime, Enum, func, Float)
from sqlalchemy.dialects.postgresql import JSONB
from app.db.base import Base

class SellerKYCStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class Seller(Base):
    __tablename__ = "sellers"
    
    id = Column(Integer, primary_key = True)
    
    #Link to User
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True
    )
    #Store Details
    store_name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    logo_url = Column(String(500), nullable=True)
    cover_image = Column(String(500), nullable=True)
    
    # Location fields for hyperlocal commerce
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    pincode = Column(String(20), nullable=True)
    latitude = Column(String(50), nullable=True)
    longitude = Column(String(50), nullable=True)
    delivery_radius_km = Column(Integer, default=5)
    
    # Rating and reviews
    total_reviews = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    
    #Approval & KYC
    approved = Column(Boolean, default=False)
    kyc_status = Column(
        Enum(SellerKYCStatus),
        default=SellerKYCStatus.pending,
        nullable=False
    )
    
    #KYC documents (URLs / Cloudinary IDs)
    kyc_docs = Column(
        JSONB,
        nullable=True,
        comment="aadhar, pan, gst, business_proof"
    )
    
    #Commercial terms
    commission_percent = Column(Integer, default=0)
    
    #subscription
    subscription_plan_id = Column(
        Integer,
        ForeignKey("subscriptions.id"),
        nullable=True
    )
    subscription_expiry = Column(DateTime, nullable=True)
    
    created_at = Column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    