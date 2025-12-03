// DP Ecommerce - Main JavaScript

// Update cart badge on page load
document.addEventListener('DOMContentLoaded', function() {
    updateCartBadge();
    
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card, .product-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });
});

// Update cart badge
function updateCartBadge(count) {
    const badge = document.getElementById('cart-badge');
    if (badge) {
        if (count !== undefined) {
            badge.textContent = count;
            badge.style.display = count > 0 ? 'block' : 'none';
        } else {
            // Fetch from API if user is logged in
            fetch('/api/cart/summary')
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    }
                    return null;
                })
                .then(data => {
                    if (data && badge) {
                        badge.textContent = data.item_count;
                        badge.style.display = data.item_count > 0 ? 'block' : 'none';
                    }
                })
                .catch(error => {
                    console.log('User not logged in or cart unavailable');
                });
        }
    }
}

// Add to cart function (used in product detail page)
function addToCart(productId) {
    const quantity = parseInt(document.getElementById('quantity')?.value || 1);
    
    fetch('/api/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Show success message
            showNotification('Product added to cart!', 'success');
            updateCartBadge(data.cart.item_count);
        } else {
            showNotification('Error: ' + data.message, 'error');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('An error occurred. Please try again.', 'error');
    });
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 100px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 3 seconds
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

// Smooth scroll
function smoothScrollTo(element) {
    element.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (form) {
        if (!form.checkValidity()) {
            form.classList.add('was-validated');
            return false;
        }
    }
    return true;
}

// Quantity input handlers
function increaseQuantity(inputId) {
    const input = document.getElementById(inputId);
    if (input) {
        const max = parseInt(input.getAttribute('max')) || 999;
        const current = parseInt(input.value) || 1;
        if (current < max) {
            input.value = current + 1;
        }
    }
}

function decreaseQuantity(inputId) {
    const input = document.getElementById(inputId);
    if (input) {
        const current = parseInt(input.value) || 1;
        if (current > 1) {
            input.value = current - 1;
        }
    }
}

// Search functionality
function performSearch(query) {
    if (query.trim().length > 0) {
        window.location.href = `/products?search=${encodeURIComponent(query)}`;
    }
}

// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Auto-hide alerts
setTimeout(function() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    });
}, 5000);

