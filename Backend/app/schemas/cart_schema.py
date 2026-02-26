from pydantic import BaseModel, Field


class CartItemIn(BaseModel):
    product_id: int
    title: str
    price: int
    image: str | None = None
    quantity: int = Field(default=1, ge=1)


class CartSyncIn(BaseModel):
    store_id: int | None = None
    items: list[CartItemIn] = Field(default_factory=list)


class CartItemOut(BaseModel):
    product_id: int
    title: str
    price: int
    image: str | None = None
    quantity: int


class CartOut(BaseModel):
    store_id: int | None = None
    items: list[CartItemOut]
