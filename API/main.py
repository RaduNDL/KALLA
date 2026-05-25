from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt
import jwt
from datetime import datetime, timedelta
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PARAMS = {
    "dbname": "coffeeshop",
    "user": "postgres",
    "password": "parola",
    "host": "localhost",
    "port": "5432"
}

SECRET_KEY = "professional_coffee_shop_secret"
ALGORITHM = "HS256"

class UserAuth(BaseModel):
    email: str
    password: str

class RegisterSchema(BaseModel):
    name: str
    email: str
    password: str

class OrderItemSchema(BaseModel):
    product_id: int
    price: float
    quantity: int

class CheckoutSchema(BaseModel):
    full_name: str
    address: str
    city: str
    total_amount: float
    items: list[OrderItemSchema]

class SettingsUpdateSchema(BaseModel):
    new_name: str
    new_email: str
    new_password: str = None

class ProductSchema(BaseModel):
    name: str
    description: str
    details: str
    price: float
    category: str
    image_url: str
    stock: int

class OrderStatusUpdate(BaseModel):
    status: str

def get_db_connection():
    return psycopg2.connect(**DB_PARAMS)

def verify_employee(authorization: str):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("role") != "employee":
            raise HTTPException(status_code=403, detail="Not authorized")
        return payload
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/register")
def register(user: RegisterSchema):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = %s", (user.email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    cursor.execute("INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, 'customer')",
                   (user.name, user.email, hashed_password))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User created successfully"}

@app.post("/api/login")
def login(user: UserAuth):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, name, password_hash, role FROM users WHERE email = %s", (user.email,))
    db_user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not db_user or not bcrypt.checkpw(user.password.encode('utf-8'), db_user['password_hash'].encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token_expires = datetime.utcnow() + timedelta(hours=24)
    token = jwt.encode({"sub": user.email, "name": db_user['name'], "role": db_user['role'], "exp": token_expires},
                       SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/api/products")
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, name, description, details, price, category, image_url, stock FROM products ORDER BY id ASC;")
    products = cursor.fetchall()
    cursor.close()
    conn.close()
    return products

@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, name, description, details, price, category, image_url, stock FROM products WHERE id = %s;", (product_id,))
    product = cursor.fetchone()
    cursor.close()
    conn.close()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/admin/products")
def create_product(product: ProductSchema, authorization: str = Header(None)):
    verify_employee(authorization)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """INSERT INTO products (name, description, details, price, category, image_url, stock)
               VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;""",
            (product.name, product.description, product.details, product.price, product.category, product.image_url, product.stock)
        )
        new_id = cursor.fetchone()[0]
        conn.commit()
        return {"message": "Product created", "id": new_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.put("/api/admin/products/{product_id}")
def update_product(product_id: int, product: ProductSchema, authorization: str = Header(None)):
    verify_employee(authorization)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            """UPDATE products SET name=%s, description=%s, details=%s, price=%s, category=%s, image_url=%s, stock=%s
               WHERE id=%s;""",
            (product.name, product.description, product.details, product.price, product.category, product.image_url, product.stock, product_id)
        )
        conn.commit()
        return {"message": "Product updated"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.delete("/api/admin/products/{product_id}")
def delete_product(product_id: int, authorization: str = Header(None)):
    verify_employee(authorization)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM products WHERE id=%s;", (product_id,))
        conn.commit()
        return {"message": "Product deleted"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.post("/api/orders")
def create_order(order_data: CheckoutSchema):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO orders (full_name, address, city, total_amount, status) VALUES (%s, %s, %s, %s, 'Pending') RETURNING id;",
            (order_data.full_name, order_data.address, order_data.city, order_data.total_amount)
        )
        order_id = cursor.fetchone()[0]
        for item in order_data.items:
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, price_at_purchase, quantity) VALUES (%s, %s, %s, %s);",
                (order_id, item.product_id, item.price, item.quantity)
            )
        conn.commit()
        return {"message": "Order created successfully", "order_id": order_id}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/api/orders/history")
def get_order_history():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, full_name, total_amount, status, created_at FROM orders ORDER BY created_at DESC;")
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return orders

@app.put("/api/admin/orders/{order_id}/status")
def update_order_status(order_id: int, data: OrderStatusUpdate, authorization: str = Header(None)):
    verify_employee(authorization)
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE orders SET status = %s WHERE id = %s", (data.status, order_id))
        conn.commit()
        return {"message": "Order status updated"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.put("/api/user/settings")
def update_settings(data: SettingsUpdateSchema, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        current_email = payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, role FROM users WHERE email = %s", (current_email,))
    db_user = cursor.fetchone()
    if not db_user:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=444, detail="User not found")

    if data.new_email != current_email:
        cursor.execute("SELECT id FROM users WHERE email = %s", (data.new_email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            raise HTTPException(status_code=400, detail="Email already registered")

    if data.new_password:
        hashed_password = bcrypt.hashpw(data.new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("UPDATE users SET name = %s, email = %s, password_hash = %s WHERE id = %s",
                       (data.new_name, data.new_email, hashed_password, db_user['id']))
    else:
        cursor.execute("UPDATE users SET name = %s, email = %s WHERE id = %s",
                       (data.new_name, data.new_email, db_user['id']))

    conn.commit()
    cursor.close()
    conn.close()

    token_expires = datetime.utcnow() + timedelta(hours=24)
    new_token = jwt.encode(
        {"sub": data.new_email, "name": data.new_name, "role": db_user['role'], "exp": token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"message": "Settings updated successfully", "access_token": new_token}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)