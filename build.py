import os
import shutil
import json
from jinja2 import Environment, FileSystemLoader

# Configuration
DOCS_DIR = "docs"
STATIC_DIR = "static"
TEMPLATES_DIR = "templates"
# Use empty base URL for local development
BASE_URL = ""

# Sample product data
products = [
    {
        "id": 1,
        "name": "Premium Cotton Fabric",
        "description": "High-quality cotton fabric perfect for summer wear",
        "category": "fabrics",
        "price": 15.99,
        "image": "/static/images/placeholder.jpg"
    },
    {
        "id": 2,
        "name": "Custom Dress Design",
        "description": "Professional dress design consultation",
        "category": "design",
        "price": 99.99,
        "image": "/static/images/placeholder.jpg"
    },
    {
        "id": 3,
        "name": "Character Illustration",
        "description": "Custom character design and illustration",
        "category": "cartooning",
        "price": 49.99,
        "image": "/static/images/placeholder.jpg"
    },
    {
        "id": 4,
        "name": "Suit Tailoring",
        "description": "Professional suit alteration service",
        "category": "tailoring",
        "price": 149.99,
        "image": "/static/images/placeholder.jpg"
    },
    {
        "id": 5,
        "name": "Designer Clothes",
        "description": "Ready-to-wear designer clothing collection",
        "category": "clothes",
        "price": 199.99,
        "image": "/static/images/placeholder.jpg"
    }
]

def ensure_dir(directory):
    """Ensure directory exists, create if it doesn't"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def clean_directory(directory):
    """Completely remove and recreate a directory"""
    if os.path.exists(directory):
        print(f"Cleaning {directory}...")
        shutil.rmtree(directory)
    os.makedirs(directory)

def copy_static_files():
    """Copy static files to docs directory"""
    static_dest = os.path.join(DOCS_DIR, "static")
    if os.path.exists(STATIC_DIR):
        shutil.copytree(STATIC_DIR, static_dest, dirs_exist_ok=True)

def generate_products_json():
    """Generate products.json file"""
    with open(os.path.join(DOCS_DIR, "products.json"), "w") as f:
        json.dump(products, f, indent=2)

def url_for(endpoint, **kwargs):
    """Simulate FastAPI's url_for function for static site generation"""
    if endpoint == 'static':
        return f"/{endpoint}/{kwargs['path']}"
    return "/"

def render_template(template_name, context, output_path):
    """Render a template with given context to output path"""
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    env.globals['url_for'] = url_for
    template = env.get_template(template_name)
    html = template.render(**context)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

def build_site():
    """Build the static site"""
    print("Starting clean build...")
    
    # Clean and recreate docs directory
    clean_directory(DOCS_DIR)
    
    # Create products directory
    products_dir = os.path.join(DOCS_DIR, "products")
    ensure_dir(products_dir)
    
    # Copy static files
    print("Copying static files...")
    copy_static_files()
    
    # Generate products.json
    print("Generating products.json...")
    generate_products_json()
    
    # Render index page
    print("Building index page...")
    render_template(
        "index.html",
        {"products": products},
        os.path.join(DOCS_DIR, "index.html")
    )
    
    # Render main products page
    print("Building products pages...")
    render_template(
        "products.html",
        {"products": products, "category": None},
        os.path.join(DOCS_DIR, "products", "index.html")
    )
    
    # Render category pages
    categories = set(p["category"] for p in products)
    for category in categories:
        print(f"Building category page: {category}")
        # Create category directory
        category_dir = os.path.join(DOCS_DIR, "products", category)
        ensure_dir(category_dir)
        
        # Filter products for this category
        category_products = [p for p in products if p["category"] == category]
        
        # Generate category page
        render_template(
            "products.html",
            {"products": category_products, "category": category},
            os.path.join(DOCS_DIR, "products", f"{category}.html")
        )
        
        # Generate category index page
        render_template(
            "products.html",
            {"products": category_products, "category": category},
            os.path.join(category_dir, "index.html")
        )

    print("Build completed successfully!")

if __name__ == "__main__":
    build_site()
