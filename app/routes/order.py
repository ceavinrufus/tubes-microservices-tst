from fastapi import APIRouter, Depends, HTTPException
from app.models.order import Order
from app.models.user import User
from app.config.database import orders_collection
from app.schema.order_schemas import list_serial, individual_serial
from app.middleware.auth import get_current_active_user, check_admin
from datetime import date

router = APIRouter()

# Get all orders
@router.get('')
async def get_all_orders(current_user: User = Depends(check_admin)):
    orders = list_serial(orders_collection.find().limit(100))
    return {"results":orders}

# Get users orders
@router.get('/me')
async def get_user_orders(current_user: User = Depends(get_current_active_user)):
    orders = list_serial(orders_collection.find({"username": current_user.username}).limit(100))
    return {"results":orders}

# Get a order by its ID
@router.get('/{order_id}')
async def get_order_by_id(order_id: int, current_user: User = Depends(get_current_active_user)):
    order = orders_collection.find_one({"id": order_id})
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"results":individual_serial(orders_collection.find_one({"id": order_id}))}

# Create a order
@router.post('')
async def create_order(order: Order, current_user: User = Depends(get_current_active_user)):
    existing_order = orders_collection.find_one({"id": order.id})
    if existing_order:
        raise HTTPException(status_code=400, detail="Order with this ID already exists")

    order.date = order.date.isoformat()
    orders_collection.insert_one(dict(order))
    order.date = date.fromisoformat(order.date)

    return {"data":order}

# Update an order
@router.put('/{id}')
async def put_order(id: int, order: Order, current_user: User = Depends(check_admin)):
    existing_order = orders_collection.find_one({"id": id})
    
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")

    if id != order.id:
        existing_order = orders_collection.find_one({"id": order.id})
        if existing_order:
            raise HTTPException(status_code=400, detail="Movie with this ID already exists")
        
    order.date = order.date.isoformat()
    orders_collection.find_one_and_update({"id": id}, {"$set": dict(order)})
    order.date = date.fromisoformat(order.date)
    return {"data":order}

# Delete an order
@router.delete('/{id}')
async def delete_order(id: int, current_user: User = Depends(check_admin)):
    existing_order = orders_collection.find_one({"id": id})
    
    if not existing_order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    orders_collection.find_one_and_delete({"id": id})

    return {"message": "Order deleted successfully"}
