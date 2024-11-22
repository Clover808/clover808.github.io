from fastapi import FastAPI, Request, Query, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import uvicorn
import os

# Get the absolute path to the project root
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(title="Clover Clothes")

# Mount static files with absolute path
app.mount("/static", StaticFiles(directory=os.path.join(ROOT_DIR, "static")), name="static")

# Configure templates with absolute path
templates = Jinja2Templates(directory=os.path.join(ROOT_DIR, "templates"))

# Sample product data (to be replaced with database later)
PRODUCTS = [
    {
        "id": 1,
        "name": "Premium Cotton Fabric",
        "category": "fabrics",
        "price": 29.99,
        "description": "High-quality cotton fabric perfect for summer wear."
    },
    {
        "id": 2,
        "name": "Custom Design Service",
        "category": "design",
        "price": 149.99,
        "description": "Professional fashion design consultation and sketching."
    },
    {
        "id": 3,
        "name": "Expert Tailoring Service",
        "category": "tailoring",
        "price": 49.99,
        "description": "Professional clothing alterations and custom fitting."
    },
    {
        "id": 4,
        "name": "Silk Fabric Collection",
        "category": "fabrics",
        "price": 89.99,
        "description": "Luxurious silk fabrics in various patterns."
    },
    {
        "id": 5,
        "name": "Character Design Package",
        "category": "cartooning",
        "price": 199.99,
        "description": "Custom character design and illustration service."
    },
    {
        "id": 6,
        "name": "Ready-to-Wear Collection",
        "category": "clothes",
        "price": 299.99,
        "description": "Premium ready-to-wear clothing collection."
    }
]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page with featured products"""
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "products": PRODUCTS[:6],
            "cart_count": 0
        }
    )

@app.get("/products", response_class=HTMLResponse)
async def products(
    request: Request,
    category: Optional[str] = Query(None, description="Filter products by category"),
    q: Optional[str] = Query(None, description="Search products by name")
):
    """Get all products with optional category filter and search"""
    filtered_products = PRODUCTS

    # Apply category filter if provided
    if category:
        filtered_products = [p for p in filtered_products if p["category"] == category]
    
    # Apply search filter if provided
    if q:
        filtered_products = [
            p for p in filtered_products 
            if q.lower() in p["name"].lower() or q.lower() in p["description"].lower()
        ]

    return templates.TemplateResponse(
        "products.html",
        {
            "request": request,
            "products": filtered_products,
            "category": category,
            "search_query": q,
            "cart_count": 0
        }
    )

@app.get("/search", response_class=HTMLResponse)
async def search(
    request: Request,
    q: str = Query(..., description="Search query")
):
    """Search products by name and description"""
    return await products(request, q=q)

@app.post("/add-to-cart/{product_id}")
async def add_to_cart(product_id: int):
    """Add a product to the cart (to be implemented with session management)"""
    return {"message": f"Added product {product_id} to cart"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
