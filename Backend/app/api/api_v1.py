from fastapi import APIRouter
from app.api.routes.auth_routes import router as auth_router
# from app.api.routes.user_routes import router as user_router
from app.api.routes.seller_routes import router as seller_router
from app.api.routes.product_routes import router as product_router
from app.api.routes.order_routes import router as order_router
# from app.api.routes.payment_routes import router as payment_router
# from app.api.routes.delivery_routes import router as delivery_router
# from app.api.routes.subscription_routes import router as subscription_router
# from app.api.routes.admin_routes import router as admin_router


api_router = APIRouter()


api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
# api_router.include_router(user_router, prefix="/users", tags=["Users"])
api_router.include_router(seller_router, prefix="/sellers", tags=["Sellers"])
api_router.include_router(product_router, prefix="/products", tags=["Products"])
api_router.include_router(order_router, prefix="/orders", tags=["Orders"])
# api_router.include_router(payment_router, prefix="/payments", tags=["Payments"])
# api_router.include_router(delivery_router, prefix="/delivery", tags=["Delivery"])
# api_router.include_router(subscription_router, prefix="/subscriptions", tags=["Subscriptions"])
# api_router.include_router(admin_router, prefix="/admin", tags=["Admin"])
