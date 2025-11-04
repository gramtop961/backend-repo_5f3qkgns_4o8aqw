import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List

from database import create_document, get_documents
from schemas import Order

app = FastAPI(title="Bits&Bites API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bits&Bites backend is running"}

@app.get("/test")
def test_database():
    from database import db
    status = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set" if not os.getenv("DATABASE_URL") else "✅ Set",
        "database_name": "❌ Not Set" if not os.getenv("DATABASE_NAME") else "✅ Set",
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            status["database"] = "✅ Available"
            try:
                status["collections"] = db.list_collection_names()
                status["connection_status"] = "Connected"
                status["database"] = "✅ Connected & Working"
            except Exception as e:
                status["database"] = f"⚠️ Connected but error: {str(e)[:80]}"
        else:
            status["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        status["database"] = f"❌ Error: {str(e)[:80]}"
    return status

# Static menu data grouped by categories
MENU: Dict[str, List[Dict]] = {
    "Starters": [
        {"name": "Veg Manchuria", "price": 90},
        {"name": "Gobi Manchuria", "price": 100},
        {"name": "Crispy Corn", "price": 90},
        {"name": "Baby Corn Manchuria", "price": 110},
        {"name": "Paneer Manchuria", "price": 130},
        {"name": "Chilli Panner", "price": 130},
        {"name": "Gobi 65", "price": 130},
        {"name": "Chicken Manchuria", "price": 130},
        {"name": "Chilli Chicken", "price": 130},
        {"name": "Kaju Chicken", "price": 150},
        {"name": "Ginger Chicken", "price": 130},
        {"name": "Chicken 65", "price": 130},
        {"name": "Chilli Paneer", "price": 130},
        {"name": "Egg 65", "price": 110},
        {"name": "Egg Manchuria", "price": 110},
        {"name": "Egg Chilli", "price": 110},
        {"name": "Mushroom Manchuria", "price": 129},
        {"name": "Chicken Drum Sticks", "price": 180},
        {"name": "Chicken Wings", "price": 200},
        {"name": "Garlic Chicken", "price": 130},
        {"name": "Butter Garlic Chicken", "price": 140},
        {"name": "Schezwan Prawns", "price": 210},
        {"name": "Chilly Prawns", "price": 180},
        {"name": "Crispy Prawns", "price": 200},
        {"name": "Maggi Pakora", "price": 120},
    ],
    "Rolls": [
        {"name": "Veg Roll", "price": 90},
        {"name": "Veg Cheese Roll", "price": 120},
        {"name": "Egg Roll", "price": 100},
        {"name": "Paneer Roll", "price": 120},
        {"name": "Paneer Cheese Roll", "price": 140},
        {"name": "Chicken Roll", "price": 130},
        {"name": "Chicken Cheese Roll", "price": 150},
        {"name": "Egg Chicken Roll", "price": 150},
        {"name": "Mutton Keema Roll", "price": 160},
        {"name": "Double Chicken Cheese Roll", "price": 160},
    ],
    "Breads & Puffs": [
        {"name": "Garlic Bread", "price": 70},
        {"name": "Aloo Samosa (2 pieces)", "price": 30},
        {"name": "Veg Puff", "price": 35},
        {"name": "Egg Puff", "price": 50},
        {"name": "Chicken Puff", "price": 50},
        {"name": "Paneer Puff", "price": 50},
        {"name": "Potato Wedges", "price": 80},
        {"name": "French Fries", "price": 80},
    ],
    "Dosa": [
        {"name": "Rava Dosa", "price": 55},
        {"name": "Onion Rava Dosa", "price": 65},
        {"name": "Plain Dosa", "price": 35},
        {"name": "Masala Dosa", "price": 50},
        {"name": "Onion Dosa", "price": 50},
        {"name": "Onion Rava Masala Dosa", "price": 65},
        {"name": "Pizza Dosa", "price": 130},
        {"name": "Upma Dosa", "price": 80},
        {"name": "Jeera Dosa", "price": 75},
        {"name": "Butter Dosa", "price": 60},
        {"name": "Butter Masala Dosa", "price": 75},
        {"name": "Butter Cheese Dosa", "price": 100},
        {"name": "Butter Corn Dosa", "price": 85},
        {"name": "Butter Karam Dosa", "price": 85},
        {"name": "Double Butter Dosa", "price": 70},
        {"name": "Paneer Dosa", "price": 95},
        {"name": "Paneer Masala Dosa", "price": 110},
        {"name": "Chilli Paneer Dosa", "price": 100},
        {"name": "Paneer Schezwan Dosa", "price": 110},
        {"name": "Paneer Corn Dosa", "price": 110},
        {"name": "Masala Uttapam", "price": 110},
        {"name": "Onion Uttapam", "price": 80},
        {"name": "Kaju Dosa", "price": 135},
        {"name": "Butter Babycorn Dosa", "price": 90},
        {"name": "Spicy Babycorn Dosa", "price": 90},
        {"name": "Paneer Babycorn Dosa", "price": 110},
        {"name": "Cheese Babycorn Dosa", "price": 100},
        {"name": "Cheese Dosa", "price": 100},
        {"name": "Cheese Masala Dosa", "price": 100},
        {"name": "Double Cheese Dosa", "price": 120},
        {"name": "Cheese Schezwan Dosa", "price": 130},
        {"name": "Chilli Cheese Dosa", "price": 90},
        {"name": "Cheese Corn Dosa", "price": 105},
        {"name": "Spl Ghee Masala Dosa", "price": 80},
        {"name": "Ghee Karam Dosa", "price": 75},
        {"name": "Plain Ghee Dosa", "price": 65},
        {"name": "Plain Uttapam", "price": 65},
        {"name": "Butter Uttapam", "price": 85},
        {"name": "Cheese Uttapam", "price": 110},
        {"name": "Kaju Cheese Uttapam", "price": 140},
        {"name": "Panner Uttapam", "price": 110},
        {"name": "Paneer Cheese Uttapam", "price": 130},
    ],
    "Idli": [
        {"name": "Plain Idli (4 pieces)", "price": 40},
        {"name": "Butter Idli", "price": 50},
        {"name": "Plain Ghee Idli", "price": 55},
        {"name": "Karam Podi Idli", "price": 55},
        {"name": "Guntur Ghee Idli", "price": 65},
        {"name": "Sambhar Idli", "price": 60},
        {"name": "Paneer Schezwan Idli", "price": 85},
        {"name": "Cheese Schezwan Idli", "price": 100},
        {"name": "Idli 65", "price": 80},
    ],
    "Fried Rice": [
        {"name": "Veg Fried Rice", "price": 90},
        {"name": "Veg Manchurian Fried Rice", "price": 110},
        {"name": "Gobi Fried Rice", "price": 110},
        {"name": "Egg Fried Rice", "price": 110},
        {"name": "Double Egg Fried Rice", "price": 120},
        {"name": "Double Egg Dble Chicken Fried Rice", "price": 150},
        {"name": "Paneer Fried Rice", "price": 120},
        {"name": "Mixed Non Veg Fried Rice", "price": 180},
        {"name": "Babycorn Fried Rice", "price": 120},
        {"name": "Mushroom Fried Rice", "price": 120},
        {"name": "Chicken Fried Rice", "price": 130},
        {"name": "Double chicken fried rice", "price": 140},
        {"name": "Chicken Schezwan Fried Rice", "price": 140},
    ],
    "Noodles": [
        {"name": "Veg Noodles", "price": 90},
        {"name": "Veg Manchurian Noodles", "price": 100},
        {"name": "Gobi Noodles", "price": 110},
        {"name": "Egg Noodles", "price": 110},
        {"name": "Double Egg Noodles", "price": 120},
        {"name": "Chicken Noodles", "price": 120},
        {"name": "Double Chicken Noodles", "price": 140},
        {"name": "Paneer Noodles", "price": 120},
        {"name": "Mushroom Noodles", "price": 120},
        {"name": "Babycorn Noodles", "price": 110},
        {"name": "Double Egg Dble Chicken Noodles", "price": 150},
        {"name": "Veg Schezwan Noodles", "price": 110},
        {"name": "Chicken Schezwan Noodles", "price": 130},
    ],
    "Tea & Coffee": [
        {"name": "Tea", "price": 20},
        {"name": "Filter Coffee", "price": 25},
        {"name": "Milk", "price": 20},
        {"name": "Black Coffee", "price": 25},
    ],
}

@app.get("/api/menu")
def get_menu():
    # Remove duplicate entries like duplicate Paneer Manchuria or Butter Uttapam implicitly by set
    cleaned: Dict[str, List[Dict]] = {}
    for cat, items in MENU.items():
        seen = set()
        cleaned_items = []
        for it in items:
            key = (it["name"], it["price"])  # consider same name+price duplicate
            if key not in seen:
                seen.add(key)
                cleaned_items.append(it)
        cleaned[cat] = cleaned_items
    return {"categories": cleaned}

@app.post("/api/orders")
def create_order(order: Order):
    # Basic validation for payment method and items
    if order.payment_method.lower() not in {"cod", "upi"}:
        raise HTTPException(status_code=400, detail="Invalid payment method. Use 'cod' or 'upi'.")
    if not order.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    # Recalculate totals server-side to prevent tampering
    subtotal = sum(item.price * item.quantity for item in order.items)
    discount = max(0.0, float(order.discount))
    total = max(0.0, float(subtotal - discount))

    data = order.model_dump()
    data.update({"subtotal": float(subtotal), "discount": float(discount), "total": float(total)})

    try:
        inserted_id = create_document("order", data)
        return {"status": "ok", "order_id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/orders")
def list_orders(limit: int = 50):
    try:
        docs = get_documents("order", {}, limit=limit)
        # Convert ObjectId and datetime to strings
        def serialize(doc):
            doc = dict(doc)
            if "_id" in doc:
                doc["_id"] = str(doc["_id"])
            for k in ["created_at", "updated_at"]:
                if k in doc:
                    doc[k] = str(doc[k])
            return doc
        return [serialize(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
