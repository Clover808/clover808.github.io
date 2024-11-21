from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI(title="CloverClothes Store")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Load product data
def load_products(category=None):
    with open("static/data/products.json", "r") as f:
        data = json.load(f)
        if category and category != "all":
            data["products"] = [p for p in data["products"] if p["category"] == category]
        return data["products"]

@app.get("/")
async def home(request: Request):
    products = load_products()
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "products": products, "active_category": "all"}
    )

@app.get("/category/{category}")
async def category(request: Request, category: str):
    products = load_products(category)
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "products": products, "active_category": category}
    )

@app.get("/product/{product_id}")
async def product_detail(product_id: int, request: Request):
    # Load products from JSON file
    with open("static/data/products.json", "r") as f:
        products = json.load(f)
    
    # Find the product with matching ID
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return templates.TemplateResponse(
        "product.html",
        {"request": request, "product": product}
    )

@app.get("/contact")
async def contact_page(request: Request, product_id: int = None):
    product = None
    if product_id is not None:
        # Load products from JSON file
        with open("static/data/products.json", "r") as f:
            products = json.load(f)
        
        # Find the product with matching ID
        product = next((p for p in products if p["id"] == product_id), None)
    
    return templates.TemplateResponse(
        "contact.html",
        {"request": request, "product": product}
    )

@app.post("/contact")
async def contact_submit(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...),
    product_id: int = Form(None),
    product_name: str = Form(None),
    product_price: float = Form(None)
):
    # Here you would typically send an email or store the contact request
    # For now, we'll just redirect back to the home page
    return RedirectResponse(url="/", status_code=303)

@app.post("/contact")
async def contact(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    # In a real application, you would handle the contact form data here
    # For now, we'll just redirect back to home
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
