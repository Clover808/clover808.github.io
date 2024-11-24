document.addEventListener('DOMContentLoaded', function() {
    // Load products data
    fetch('/static/data/site.json')
        .then(response => response.json())
        .then(data => {
            const products = data.products;
            const productsContainer = document.querySelector('.products-container');
            
            // Search functionality
            const searchForm = document.querySelector('form');
            if (searchForm) {
                searchForm.addEventListener('submit', function(e) {
                    e.preventDefault();
                    const searchQuery = this.querySelector('input[name="q"]').value.toLowerCase();
                    const filteredProducts = products.filter(product => 
                        product.name.toLowerCase().includes(searchQuery) ||
                        product.description.toLowerCase().includes(searchQuery)
                    );
                    displayProducts(filteredProducts);
                });
            }

            // Category filtering
            const categoryButtons = document.querySelectorAll('.category-filter-btn');
            categoryButtons.forEach(button => {
                button.addEventListener('click', function(e) {
                    e.preventDefault();
                    const category = this.getAttribute('data-category');
                    const filteredProducts = category ? 
                        products.filter(product => product.category === category) :
                        products;
                    displayProducts(filteredProducts);
                    
                    // Update active state
                    categoryButtons.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');
                });
            });

            // Display products function
            function displayProducts(productsToShow) {
                if (!productsContainer) return;
                
                productsContainer.innerHTML = productsToShow.map(product => `
                    <div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <img src="${product.image}" class="card-img-top" alt="${product.name}">
                            <div class="card-body">
                                <h5 class="card-title">${product.name}</h5>
                                <p class="card-text">${product.description}</p>
                                <p class="card-text"><strong>$${product.price.toFixed(2)}</strong></p>
                                <button class="btn btn-success add-to-cart" data-product-id="${product.id}">
                                    Add to Cart
                                </button>
                            </div>
                        </div>
                    </div>
                `).join('');
            }

            // Initial display
            if (productsContainer) {
                displayProducts(products);
            }
        })
        .catch(error => console.error('Error loading products:', error));
});
