def individual_serial(order) -> dict:
    return {
        # "id": str(order.get("_id", "")),  # Provide a default value for missing keys
        "order_id": int(order.get("id", "")),  # Provide a default value for missing keys
        "date": order.get("date", ""),  # Provide a default value for missing keys
        "ticketPrice": float(order.get("ticketPrice", "")),  # Provide a default value for missing keys
        "total": int(order.get("total", "")),  # Provide a default value for missing keys
        "movieId": order.get("movieId", ""),  # Provide a default value for missing keys
        "seats": order.get("seats", ""),  # Provide a default value for missing keys
        "username": order.get("username", ""),  # Provide a default value for missing keys
    }

def list_serial(orders) -> list:
    return [individual_serial(order) for order in orders]