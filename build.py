from pathlib import Path
import shutil
import json
from jinja2 import Environment, FileSystemLoader
from app.main import PRODUCTS

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader('templates'))

# Create build directory
BUILD_DIR = Path('build')
if BUILD_DIR.exists():
    shutil.rmtree(BUILD_DIR)
BUILD_DIR.mkdir()

# Create static directories
STATIC_DIR = BUILD_DIR / 'static'
(STATIC_DIR / 'css').mkdir(parents=True)
(STATIC_DIR / 'images').mkdir(parents=True)

# Copy static files
shutil.copy('static/css/style.css', STATIC_DIR / 'css' / 'style.css')
shutil.copy('static/images/hero-bg.jpg', STATIC_DIR / 'images' / 'hero-bg.jpg')
shutil.copy('static/images/placeholder.jpg', STATIC_DIR / 'images' / 'placeholder.jpg')

# Helper function to simulate url_for in templates
def url_for(endpoint, **kwargs):
    if endpoint == 'static':
        return f"/static/{kwargs['path']}"
    return '/'

# Generate index.html
template = env.get_template('index.html')
html = template.render(
    request={},  # Dummy request object
    products=PRODUCTS[:3],  # Featured products
    category=None,
    cart_count=0,
    url_for=url_for
)
with open(BUILD_DIR / 'index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Generate products.html for each category
categories = ['fabrics', 'clothes', 'design', 'cartooning', 'tailoring']
template = env.get_template('products.html')

# All products page
products_dir = BUILD_DIR / 'products'
products_dir.mkdir(exist_ok=True)
html = template.render(
    request={},
    products=PRODUCTS,
    category=None,
    cart_count=0,
    url_for=url_for
)
with open(products_dir / 'index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Category pages
for category in categories:
    category_dir = products_dir / category
    category_dir.mkdir(exist_ok=True)
    filtered_products = [p for p in PRODUCTS if p['category'] == category]
    html = template.render(
        request={},
        products=filtered_products,
        category=category,
        cart_count=0,
        url_for=url_for
    )
    with open(category_dir / 'index.html', 'w', encoding='utf-8') as f:
        f.write(html)

# Generate products.json for search functionality
with open(BUILD_DIR / 'products.json', 'w', encoding='utf-8') as f:
    json.dump(PRODUCTS, f)

print("Static site generated successfully in the 'build' directory")
