from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..models import models
from ..schemas import schemas

router = APIRouter()

# Product endpoints
@router.get("/products/", response_model=List[schemas.Product])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)
    if category:
        query = query.filter(models.Product.category == category)
    return query.offset(skip).limit(limit).all()

@router.get("/products/{product_id}", response_model=schemas.Product)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Order endpoints
@router.post("/orders/", response_model=schemas.Order)
async def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db)
):
    db_order = models.Order(
        total_amount=order.total_amount,
        status=order.status
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    
    for item in order.items:
        db_item = models.OrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order

# User endpoints
@router.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # In a real app, hash the password here
    db_user = models.User(
        email=user.email,
        hashed_password=user.password  # Don't do this in production!
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
