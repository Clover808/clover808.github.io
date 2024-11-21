// Cart functionality
let cart = [];
let cartTotal = 0;

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
                    <button onclick="updateQuantity(${item.id}, -1)">-</button>
                    <span>${item.quantity}</span>
                    <button onclick="updateQuantity(${item.id}, 1)">+</button>
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
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
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
    
    const productCards = document.querySelectorAll('.product-card');
    productCards.forEach(card => {
        if (category === 'all' || card.dataset.category === category) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
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

// Payment processing
async function proceedToCheckout() {
    if (cart.length === 0) {
        showToast('Your cart is empty!');
        return;
    }

    try {
        // Create a payment intent
        const response = await fetch('/api/create-payment-intent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                items: cart,
                total: cartTotal
            }),
        });

        if (!response.ok) {
            throw new Error('Payment failed');
        }

        const data = await response.json();
        
        // Handle different payment methods
        if (data.payment_method === 'stripe') {
            const result = await stripe.confirmCardPayment(data.client_secret, {
                payment_method: {
                    card: elements.getElement('card'),
                    billing_details: {
                        name: document.getElementById('name').value,
                    },
                },
            });

            if (result.error) {
                showToast(result.error.message);
            } else {
                showToast('Payment successful!');
                cart = [];
                updateCartBadge();
                updateCartDisplay();
                toggleCart();
            }
        } else if (data.payment_method === 'bitcoin') {
            // Show Bitcoin payment UI
            const bitcoinPayment = document.createElement('div');
            bitcoinPayment.className = 'bitcoin-payment';
            bitcoinPayment.innerHTML = `
                <h3>Bitcoin Payment</h3>
                <p>Please send exactly ${data.btc_amount} BTC to:</p>
                <div class="bitcoin-address">${data.bitcoin_address}</div>
                <img src="${data.qr_code}" alt="Bitcoin QR Code" class="qr-code">
                <div class="payment-timer">Time remaining: <span id="payment-countdown">15:00</span></div>
                <div class="payment-status pending">Waiting for payment...</div>
            `;

            document.getElementById('cart-content').innerHTML = '';
            document.getElementById('cart-content').appendChild(bitcoinPayment);

            // Start payment monitoring
            monitorBitcoinPayment(data.payment_id);
        }
    } catch (error) {
        showToast('Error processing payment: ' + error.message);
    }
}

// Bitcoin payment monitoring
async function monitorBitcoinPayment(paymentId) {
    const statusElement = document.querySelector('.payment-status');
    const countdownElement = document.getElementById('payment-countdown');
    let timeLeft = 900; // 15 minutes in seconds

    const countdown = setInterval(() => {
        timeLeft--;
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        countdownElement.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;

        if (timeLeft <= 0) {
            clearInterval(countdown);
            statusElement.className = 'payment-status failed';
            statusElement.textContent = 'Payment time expired';
        }
    }, 1000);

    const checkStatus = async () => {
        try {
            const response = await fetch(`/api/check-bitcoin-payment/${paymentId}`);
            const data = await response.json();

            if (data.status === 'completed') {
                clearInterval(countdown);
                statusElement.className = 'payment-status success';
                statusElement.textContent = 'Payment successful!';
                cart = [];
                updateCartBadge();
                setTimeout(() => {
                    updateCartDisplay();
                    toggleCart();
                }, 3000);
                return;
            } else if (data.status === 'failed') {
                clearInterval(countdown);
                statusElement.className = 'payment-status failed';
                statusElement.textContent = 'Payment failed';
                return;
            }

            // Continue checking if payment is still pending
            setTimeout(checkStatus, 10000); // Check every 10 seconds
        } catch (error) {
            console.error('Error checking payment status:', error);
        }
    };

    checkStatus();
}

// Initialize category filter
document.addEventListener('DOMContentLoaded', () => {
    filterProducts('all');
});
