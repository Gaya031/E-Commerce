from sqlalchemy import (Column, Integer, ForeignKey, String, DateTime, func)
from app.db.base import Base

class WalletTransaction(Base):
    __tablename__ = "wallet_transactions"
    
    id = Column(Integer, primary_key = True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    amount = Column(Integer, nullable=False)
    type = Column(String, nullable= False)
    reference_id = Column(String, nullable= True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    