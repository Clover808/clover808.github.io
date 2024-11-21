// Cart functionality
let cart = [];
let cartTotal = 0;

// Initialize products
document.addEventListener('DOMContentLoaded', () => {
    displayProducts('all');
    setupContactForm();
});

function displayProducts(category) {
    const container = document.getElementById('products-container');
    container.innerHTML = '';

    const filteredProducts = category === 'all' 
        ? products 
        : products.filter(product => product.category === category);

    filteredProducts.forEach(product => {
        const productCard = document.createElement('div');
        productCard.className = 'col-md-4 mb-4';
        productCard.innerHTML = `
            <div class="card product-card" data-category="${product.category}">
                <img src="${product.image}" class="card-img-top product-image" alt="${product.name}">
                <div class="card-body">
                    <h5 class="card-title">${product.name}</h5>
                    <p class="card-text">${product.description}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="h5 mb-0">$${product.price.toFixed(2)}</span>
                        <button class="btn btn-success" onclick="addToCart(${product.id}, '${product.name}', ${product.price}, '${product.image}')">
                            Add to Cart
                        </button>
                    </div>
                </div>
            </div>
        `;
        container.appendChild(productCard);
    });
}

function addToCart(id, name, price, image) {
    const existingItem = cart.find(item => item.id === id);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: id,
            name: name,
            price: price,
            image: image,
            quantity: 1
        });
    }
    
    updateCartBadge();
    updateCartDisplay();
    showToast(`${name} added to cart!`);
}

function removeFromCart(id) {
    const index = cart.findIndex(item => item.id === id);
    if (index > -1) {
        cart.splice(index, 1);
        updateCartBadge();
        updateCartDisplay();
    }
}

function updateQuantity(id, change) {
    const item = cart.find(item => item.id === id);
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
            <img src="${item.image}" alt="${item.name}">
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

function toggleCart() {
    const sidebar = document.getElementById('cart-sidebar');
    const overlay = document.querySelector('.cart-overlay');
    
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
}

// Search functionality
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

// Category filter functionality
function filterProducts(category) {
    const buttons = document.querySelectorAll('.category-filter-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    const activeButton = document.querySelector(`[data-category="${category}"]`);
    if (activeButton) {
        activeButton.classList.add('active');
    }
    
    displayProducts(category);
}

// Toast notifications
function showToast(message) {
    const toast = document.createElement('div');
    toast.className = 'toast animate-fade-in';
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// Contact form functionality
function setupContactForm() {
    const contactModal = new bootstrap.Modal(document.getElementById('contactModal'));
    
    document.getElementById('contactForm').addEventListener('submit', function(event) {
        event.preventDefault();
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;
        
        // In a static site, we'll use mailto: for form submission
        const mailtoLink = `mailto:your.email@example.com?subject=CloverClothes Inquiry from ${name}&body=${encodeURIComponent(`Name: ${name}\nEmail: ${email}\n\nMessage: ${message}`)}`;
        window.location.href = mailtoLink;
        
        contactModal.hide();
        showToast('Thank you for your message! We will contact you soon.');
    });
}

function contactUs() {
    const contactModal = new bootstrap.Modal(document.getElementById('contactModal'));
    contactModal.show();
}

function contactForPurchase() {
    const cartItems = cart.map(item => `${item.quantity}x ${item.name} ($${item.price.toFixed(2)} each)`).join('\n');
    const message = `I'm interested in purchasing the following items:\n\n${cartItems}\n\nTotal: $${cartTotal.toFixed(2)}`;
    
    document.getElementById('message').value = message;
    contactUs();
}
