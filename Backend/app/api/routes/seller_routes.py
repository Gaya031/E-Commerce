from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.postgres import get_db
from app.schemas.seller_schema import (SellerCreate, SellerKYCUpdate, SellerOut)
from app.services.seller_service import (create_seller_profile, upload_kyc, approve_seller)
from app.api.deps.auth_deps import get_current_user, require_roles
from app.models.user_model import User

router = APIRouter(tags=["sellers"])

@router.post("/", response_model=SellerOut, status_code=status.HTTP_201_CREATED)
async def create_seller(data: SellerCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_roles("seller"))):
    return await create_seller_profile(
        db=db,
        user_id=current_user.id,
        store_name=data.store_name
    )
    
@router.put("/{seller_id}/kyc", response_model=SellerOut)
async def update_kyc(seller_id: int, data: SellerKYCUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(require_roles("seller"))):
    return await upload_kyc(
        db=db,
        seller_id=seller_id,
        kyc_data=data.model_dump(exclude_none = True),
        user_id=current_user.id
    )
    
@router.post("/{seller_id}/approve", response_model=SellerOut)
async def approve(seller_id: int, commission_percent: int, db: AsyncSession = Depends(get_db), admin: User = Depends(require_roles("admin"))):
    return await approve_seller(
        db=db,
        seller_id=seller_id,
        commission_percent=commission_percent
    )
    
