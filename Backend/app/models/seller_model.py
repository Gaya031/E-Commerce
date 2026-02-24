import enum
from sqlalchemy import (Column, Integer, String, Boolean, ForeignKey, DateTime, Enum, func)
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
    