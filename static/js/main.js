// Global state
let cart = [];
let cartTotal = 0;

// Initialize the application
document.addEventListener('DOMContentLoaded', async () => {
    await loadProducts();
    setupEventListeners();
});

// Load products from the API
async function loadProducts() {
    try {
        const response = await fetch('/products/');
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        showToast('Error loading products');
        console.error('Error:', error);
    }
}

// Display products in the UI
function displayProducts(products) {
    const container = document.getElementById('products-container');
    container.innerHTML = '';

    products.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'col-md-4 mb-4';
        productCard.innerHTML = `
            <div class="card product-card" data-category="${product.category}">
                <img src="${product.image_url}" class="card-img-top product-image" alt="${product.name}">
                <div class="card-body">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text">${product.description}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="h5 mb-0">$${product.price.toFixed(2)}</span>
                        <button class="btn btn-success" onclick="addToCart(${JSON.stringify(product).replace(/"/g, '&quot;')})">
                            Add to Cart
                        </button>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(productCard);
    });
}

// Cart functions
function addToCart(product) {
    const existingItem = cart.find(item => item.id === product.id);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            ...product,
            quantity: 1
        });
    }
    
    updateCartBadge();
    updateCartDisplay();
    showToast(`${product.name} added to cart!`);
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCartBadge();
    updateCartDisplay();
}

function updateQuantity(productId, change) {
    const item = cart.find(item => item.id === productId);
    if (item) {
        item.quantity = Math.max(1, item.quantity + change);
        updateCartDisplay();
    }
}

function updateCartBadge() {
    const badge = document.getElementById('cart-badge');
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    badge.textContent = totalItems;
}

function updateCartDisplay() {
    const cartContent = document.getElementById('cart-content');
    cartContent.innerHTML = '';
    
    cartTotal = 0;
    
    cart.forEach(item => {
        const itemTotal = item.price * item.quantity;
        cartTotal += itemTotal;
        
        const cartItem = document.createElement('div');
        cartItem.className = 'cart-item';
        cartItem.innerHTML = `
            <img src="${item.image_url}" alt="${item.name}">
            <div class="cart-item-details">
                <div class="cart-item-title">${item.name}</div>
                <div class="cart-item-price">$${item.price.toFixed(2)}</div>
                <div class="quantity-controls">
                    <button class="btn btn-sm btn-outline-secondary" onclick="updateQuantity(${item.id}, -1)">-</button>
                    <span class="mx-2">${item.quantity}</span>
                    <button class="btn btn-sm btn-outline-secondary" onclick="updateQuantity(${item.id}, 1)">+</button>
                </div>
            </div>
            <i class="fas fa-trash cart-item-remove" onclick="removeFromCart(${item.id})"></i>
        `;
        
        cartContent.appendChild(cartItem);
    });
    
    document.getElementById('cart-total').textContent = `$${cartTotal.toFixed(2)}`;
}

// UI functions
function toggleCart() {
    const sidebar = document.getElementById('cart-sidebar');
    const overlay = document.querySelector('.cart-overlay');
    
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}

function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast animate-fade-in';
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Search and filter functions
function searchProducts() {
    const searchInput = document.getElementById('search-input').value.toLowerCase();
    const productCards = document.querySelectorAll('.product-card');
    
    productCards.forEach(card => {
        const title = card.querySelector('.card-title').textContent.toLowerCase();
        const description = card.querySelector('.card-text').textContent.toLowerCase();
        
        if (title.includes(searchInput) || description.includes(searchInput)) {
            card.parentElement.style.display = 'block';
        } else {
            card.parentElement.style.display = 'none';
        }
    });
}

async function filterProducts(category) {
    try {
        const response = await fetch('/products/');
        const products = await response.json();
        
        const filteredProducts = category === 'all' 
            ? products 
            : products.filter(product => product.category === category);
        
        displayProducts(filteredProducts);
    } catch (error) {
        showToast('Error filtering products');
        console.error('Error:', error);
    }
}

// Contact form functions
function setupEventListeners() {
    document.getElementById('contactForm').addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const formData = {
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            message: document.getElementById('message').value
        };

        try {
            const response = await fetch('/contact', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (response.ok) {
                showToast('Message sent successfully!');
                const modal = bootstrap.Modal.getInstance(document.getElementById('contactModal'));
                modal.hide();
                this.reset();
            } else {
                showToast('Error sending message');
            }
        } catch (error) {
            showToast('Error sending message');
            console.error('Error:', error);
        }
    });
}

function contactForPurchase() {
    const cartItems = cart.map(item => 
        `${item.quantity}x ${item.name} ($${item.price.toFixed(2)} each)`
    ).join('\n');
    
    document.getElementById('message').value = 
        `I'm interested in purchasing the following items:\n\n${cartItems}\n\nTotal: $${cartTotal.toFixed(2)}`;
    
    const modal = new bootstrap.Modal(document.getElementById('contactModal'));
    modal.show();
}
