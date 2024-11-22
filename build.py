import os
import shutil
import json
from jinja2 import Environment, FileSystemLoader

# Configuration
DOCS_DIR = "docs"
STATIC_DIR = "static"
TEMPLATES_DIR = "templates"
BASE_URL = "/Bespoke-attire"

# Sample product data
products = [
    {
        "id": 1,
        "name": "Premium Cotton Fabric",
        "description": "High-quality cotton fabric perfect for summer wear",
        "category": "fabrics",
        "price": 15.99,
        "image": f"{BASE_URL}/static/images/cotton.jpg"
    },
    {
        "id": 2,
        "name": "Custom Dress Design",
        "description": "Professional dress design consultation",
        "category": "design",
        "price": 99.99,
        "image": f"{BASE_URL}/static/images/dress-design.jpg"
    },
    {
        "id": 3,
        "name": "Character Illustration",
        "description": "Custom character design and illustration",
        "category": "cartooning",
        "price": 49.99,
        "image": f"{BASE_URL}/static/images/character.jpg"
    },
    {
        "id": 4,
        "name": "Suit Tailoring",
        "description": "Professional suit alteration service",
        "category": "tailoring",
        "price": 149.99,
        "image": f"{BASE_URL}/static/images/suit.jpg"
    }
]

def ensure_dir(directory):
    """Ensure directory exists, create if it doesn't"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def copy_static_files():
    """Copy static files to docs directory"""
    docs_static = os.path.join(DOCS_DIR, "static")
    if os.path.exists(docs_static):
        shutil.rmtree(docs_static)
    shutil.copytree(STATIC_DIR, docs_static)

def generate_products_json():
    """Generate products.json file"""
    with open(os.path.join(DOCS_DIR, "products.json"), "w") as f:
        json.dump(products, f, indent=2)

def url_for(endpoint, **kwargs):
    """Simulate FastAPI's url_for function for static site generation"""
    if endpoint == 'static':
        return f"{BASE_URL}/static/{kwargs['path']}"
    return f"{BASE_URL}/"

def render_template(template_name, context, output_path):
    """Render a template with given context to output path"""
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template(template_name)
    
    # Add BASE_URL and url_for to context
    context["BASE_URL"] = BASE_URL
    context["url_for"] = url_for
    
    html = template.render(**context)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

def build_site():
    """Build the static site"""
    # Ensure docs directory exists
    ensure_dir(DOCS_DIR)
    ensure_dir(os.path.join(DOCS_DIR, "products"))
    
    # Copy static files
    copy_static_files()
    
    # Generate products.json
    generate_products_json()
    
    # Render index page
    render_template(
        "index.html",
        {"products": products},
        os.path.join(DOCS_DIR, "index.html")
    )
    
    # Render products page
    render_template(
        "products.html",
        {"products": products},
        os.path.join(DOCS_DIR, "products", "index.html")
    )
    
    # Render category pages
    categories = set(p["category"] for p in products)
    for category in categories:
        category_products = [p for p in products if p["category"] == category]
        render_template(
            "products.html",
            {"products": category_products, "category": category},
            os.path.join(DOCS_DIR, "products", f"{category}.html")
        )

if __name__ == "__main__":
    build_site()
    print("Static site built successfully in docs directory")
