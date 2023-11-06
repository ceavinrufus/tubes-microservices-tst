from fastapi import APIRouter, Depends, HTTPException, Query
from app.models.order import Order
from app.config.database import orders_collection
from app.schema.order_schemas import list_serial, individual_serial
from app.routes.auth import get_current_active_user
from datetime import date

router = APIRouter()

# Get all orders
@router.get('/orders')
async def get_all_orders():
    orders = list_serial(orders_collection.find().limit(100))
    return {"results":orders}

# Get a order by its ID
@router.get('/orders/{order_id}')
async def get_order_by_id(order_id: int):
    return {"results":individual_serial(orders_collection.find_one({"id": order_id}))}

# Create a order
@router.post('/orders')
async def create_order(order: Order):
    existing_order = orders_collection.find_one({"id": order.id})
    if existing_order:
        raise HTTPException(status_code=400, detail="Order with this ID already exists")

    order.date = order.date.isoformat()
    orders_collection.insert_one(dict(order))
    order.date = date.fromisoformat(order.date)

    return {"data":order}

# Update an order
@router.put('/orders/{id}')
async def put_order(id: int, order: Order):
    order.date = order.date.isoformat()
    orders_collection.find_one_and_update({"id": id}, {"$set": dict(order)})
    order.date = date.fromisoformat(order.date)
    return {"data":order}

# Delete an order
@router.delete('/orders/{id}')
async def delete_order(id: int):
    orders_collection.find_one_and_delete({"id": id})

# async def recommendation(order_id: int, amount: int, current_user: User = Depends(get_current_active_user)):