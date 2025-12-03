"""
DP Ecommerce - Professional Web Application
Flask-based frontend for the Advanced E-commerce System
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from decimal import Decimal
from functools import wraps
import json
from ecommerce.app import ECommerceApp
from ecommerce.models.user import UserRole
from ecommerce.models.order import OrderStatus
from ecommerce.services.payment import PaymentProcessor
from ecommerce.utils.currency import usd_to_inr, format_inr
from ecommerce.database import init_db, db
from ecommerce.repositories.db_repository import UserRepository, CategoryRepository, ProductRepository
from ecommerce.services.auth import AuthenticationService
from ecommerce.services.category_service import CategoryService
from ecommerce.services.product_service import ProductService

app = Flask(__name__)
app.secret_key = 'dp-ecommerce-secret-key-change-in-production'

# Initialize database
init_db(app)

# Add currency filter to Jinja2
@app.template_filter('inr')
def inr_filter(amount):
    """Convert USD to INR and format"""
    if isinstance(amount, (int, float)):
        amount = Decimal(str(amount))
    inr_amount = usd_to_inr(amount)
    return format_inr(inr_amount)

# Initialize e-commerce app with database repositories
ecommerce_app = ECommerceApp()
# Override with database repositories
ecommerce_app.user_repository = UserRepository()
ecommerce_app.category_repository = CategoryRepository()
ecommerce_app.product_repository = ProductRepository()
# Reinitialize services with new repositories
ecommerce_app.auth_service = AuthenticationService(ecommerce_app.user_repository)
ecommerce_app.category_service = CategoryService(ecommerce_app.category_repository)
ecommerce_app.product_service = ProductService(
    ecommerce_app.product_repository,
    ecommerce_app.category_repository
)
# Reinitialize cart service with new product repository
from ecommerce.services.cart_service import CartService
ecommerce_app.cart_service = CartService(
    ecommerce_app.cart_repository,
    ecommerce_app.product_repository
)
# Reinitialize order service with new repositories
from ecommerce.services.order_service import OrderService
ecommerce_app.order_service = OrderService(
    ecommerce_app.order_repository,
    ecommerce_app.cart_repository,
    ecommerce_app.product_repository
)

# Session management
def get_user_id():
    """Get current user ID from session"""
    return session.get('user_id')

def get_user():
    """Get current user object"""
    user_id = get_user_id()
    if user_id:
        users = ecommerce_app.user_repository.find_all()
        from ecommerce.models.user import User
        for user in users:
            if isinstance(user, User) and user.id == user_id:
                ecommerce_app.current_user = user
                return user
    return None

def login_required(f):
    """Decorator for routes that require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not get_user():
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator for routes that require admin role"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        user = get_user()
        if not user or not user.is_admin():
            flash('Admin access required', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

def manager_required(f):
    """Decorator for routes that require manager or admin role"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        user = get_user()
        if not user or not user.can_manage_products():
            flash('Manager or Admin access required', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Helper functions for JSON serialization
def decimal_default(obj):
    """JSON serializer for Decimal objects"""
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

# Routes
@app.route('/')
def index():
    """Home page"""
    products = ecommerce_app.product_service.get_all_products(active_only=True)[:8]
    categories = ecommerce_app.category_service.get_all_categories(active_only=True)
    user = get_user()
    
    return render_template('index.html', 
                         products=products, 
                         categories=categories,
                         user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = ecommerce_app.auth_service.login(username, password)
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            flash(f'Welcome back, {user.full_name}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        try:
            user = ecommerce_app.auth_service.register(
                username=username,
                email=email,
                password=password,
                first_name=first_name or None,
                last_name=last_name or None
            )
            if user:
                session['user_id'] = user.id
                session['username'] = user.username
                flash('Registration successful! Welcome!', 'success')
                return redirect(url_for('index'))
        except ValueError as e:
            flash(str(e), 'danger')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    ecommerce_app.logout()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/products')
def products():
    """Products listing page"""
    category_id = request.args.get('category')
    search = request.args.get('search')
    
    if search:
        product_list = ecommerce_app.product_service.search_products(search)
    elif category_id:
        product_list = ecommerce_app.product_service.get_products_by_category(category_id)
    else:
        product_list = ecommerce_app.product_service.get_all_products(active_only=True)
    
    categories = ecommerce_app.category_service.get_all_categories(active_only=True)
    user = get_user()
    
    return render_template('products.html',
                         products=product_list,
                         categories=categories,
                         user=user,
                         selected_category=category_id,
                         search_query=search)

@app.route('/product/<product_id>')
def product_detail(product_id):
    """Product detail page"""
    product = ecommerce_app.product_service.get_product(product_id)
    if not product:
        flash('Product not found', 'danger')
        return redirect(url_for('products'))
    
    category = ecommerce_app.category_service.get_category(product.category_id)
    user = get_user()
    
    return render_template('product_detail.html',
                         product=product,
                         category=category,
                         user=user)

@app.route('/cart')
@login_required
def cart():
    """Shopping cart page"""
    user = get_user()
    cart_summary = ecommerce_app.cart_service.get_cart_summary(user.id)
    
    return render_template('cart.html',
                         cart=cart_summary,
                         user=user)

@app.route('/api/cart/add', methods=['POST'])
@login_required
def api_add_to_cart():
    """API endpoint to add product to cart"""
    data = request.json
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    
    user = get_user()
    try:
        ecommerce_app.cart_service.add_to_cart(user.id, product_id, quantity)
        cart_summary = ecommerce_app.cart_service.get_cart_summary(user.id)
        return jsonify({
            'success': True,
            'message': 'Product added to cart',
            'cart': cart_summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/cart/update', methods=['POST'])
@login_required
def api_update_cart():
    """API endpoint to update cart item"""
    data = request.json
    product_id = data.get('product_id')
    quantity = int(data.get('quantity', 1))
    
    user = get_user()
    try:
        ecommerce_app.cart_service.update_cart_item(user.id, product_id, quantity)
        cart_summary = ecommerce_app.cart_service.get_cart_summary(user.id)
        return jsonify({
            'success': True,
            'message': 'Cart updated',
            'cart': cart_summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/cart/remove', methods=['POST'])
@login_required
def api_remove_from_cart():
    """API endpoint to remove item from cart"""
    data = request.json
    product_id = data.get('product_id')
    
    user = get_user()
    try:
        ecommerce_app.cart_service.remove_from_cart(user.id, product_id)
        cart_summary = ecommerce_app.cart_service.get_cart_summary(user.id)
        return jsonify({
            'success': True,
            'message': 'Item removed from cart',
            'cart': cart_summary
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

@app.route('/api/cart/summary')
@login_required
def api_cart_summary():
    """API endpoint to get cart summary"""
    user = get_user()
    cart_summary = ecommerce_app.cart_service.get_cart_summary(user.id)
    return jsonify(cart_summary)

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Checkout page"""
    user = get_user()
    cart_summary = ecommerce_app.cart_service.get_cart_summary(user.id)
    
    if cart_summary['item_count'] == 0:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('cart'))
    
    if request.method == 'POST':
        payment_method = request.form.get('payment_method')
        shipping_address = request.form.get('shipping_address')
        
        # Payment info based on method
        payment_info = {}
        if payment_method == 'credit_card':
            payment_info = {
                'card_number': request.form.get('card_number'),
                'cvv': request.form.get('cvv'),
                'expiry': request.form.get('expiry')
            }
        elif payment_method == 'paypal':
            payment_info = {
                'email': request.form.get('paypal_email'),
                'password': request.form.get('paypal_password')
            }
        elif payment_method == 'bank_transfer':
            payment_info = {
                'account_number': request.form.get('account_number'),
                'routing_number': request.form.get('routing_number')
            }
        elif payment_method in ['google_pay', 'phonepe', 'paytm', 'bhim_upi']:
            payment_info = {
                'upi_id': request.form.get('upi_id'),
                'pin': request.form.get('upi_pin')
            }
        
        try:
            order = ecommerce_app.order_service.create_order_from_cart(
                user.id,
                payment_method,
                payment_info,
                shipping_address
            )
            if order:
                flash(f'Order placed successfully! Order ID: {order.id[:8]}', 'success')
                return redirect(url_for('order_detail', order_id=order.id))
        except Exception as e:
            flash(str(e), 'danger')
    
    payment_methods = PaymentProcessor.get_available_methods()
    return render_template('checkout.html',
                         cart=cart_summary,
                         payment_methods=payment_methods,
                         user=user)

@app.route('/orders')
@login_required
def orders():
    """User orders page"""
    user = get_user()
    order_list = ecommerce_app.order_service.get_user_orders(user.id)
    
    return render_template('orders.html',
                         orders=order_list,
                         user=user)

@app.route('/order/<order_id>')
@login_required
def order_detail(order_id):
    """Order detail page"""
    user = get_user()
    order = ecommerce_app.order_service.get_order(order_id)
    
    if not order or order.user_id != user.id:
        flash('Order not found', 'danger')
        return redirect(url_for('orders'))
    
    return render_template('order_detail.html',
                         order=order,
                         user=user)

# Admin/Manager Routes
@app.route('/admin/products')
@manager_required
def admin_products():
    """Admin product management"""
    user = get_user()
    products = ecommerce_app.product_service.get_all_products()
    categories = ecommerce_app.category_service.get_all_categories(active_only=True)
    
    return render_template('admin/products.html',
                         products=products,
                         categories=categories,
                         user=user)

@app.route('/admin/products/create', methods=['POST'])
@manager_required
def admin_create_product():
    """Create product API"""
    try:
        product = ecommerce_app.product_service.create_product(
            name=request.form.get('name'),
            price=Decimal(request.form.get('price')),
            category_id=request.form.get('category_id'),
            description=request.form.get('description') or None,
            stock_quantity=int(request.form.get('stock_quantity', 0))
        )
        flash(f'Product {product.name} created successfully', 'success')
    except Exception as e:
        flash(str(e), 'danger')
    
    return redirect(url_for('admin_products'))

@app.route('/admin/products/<product_id>/delete', methods=['POST'])
@manager_required
def admin_delete_product(product_id):
    """Delete a product"""
    try:
        product = ecommerce_app.product_service.get_product(product_id)
        if product:
            product_name = product.name
            ecommerce_app.product_service.delete_product(product_id)
            flash(f'Product {product_name} deleted successfully', 'success')
        else:
            flash('Product not found', 'danger')
    except Exception as e:
        flash(str(e), 'danger')
    
    return redirect(url_for('admin_products'))

@app.route('/admin/categories', methods=['GET', 'POST'])
@manager_required
def admin_categories():
    """Admin category management"""
    user = get_user()
    
    if request.method == 'POST':
        try:
            category = ecommerce_app.category_service.create_category(
                name=request.form.get('name'),
                description=request.form.get('description') or None
            )
            flash(f'Category {category.name} created successfully', 'success')
            return redirect(url_for('admin_categories'))
        except Exception as e:
            flash(str(e), 'danger')
    
    categories = ecommerce_app.category_service.get_all_categories()
    
    return render_template('admin/categories.html',
                         categories=categories,
                         user=user)

@app.route('/admin/orders')
@manager_required
def admin_orders():
    """Admin orders view"""
    user = get_user()
    from ecommerce.models.order import Order
    orders = ecommerce_app.order_repository.find_all()
    order_list = [o for o in orders if isinstance(o, Order)]
    
    # Get all users for display
    users = ecommerce_app.user_repository.find_all()
    
    return render_template('admin/orders.html',
                         orders=order_list,
                         users=users,
                         user=user)

@app.route('/admin/users')
@admin_required
def admin_users():
    """Admin user management dashboard"""
    user = get_user()
    users = ecommerce_app.user_repository.find_all()
    from ecommerce.models.user import User
    user_list = [u for u in users if isinstance(u, User)]
    
    # Get statistics
    total_users = len(user_list)
    active_users = len([u for u in user_list if u.is_active])
    admin_users = len([u for u in user_list if u.is_admin()])
    customer_users = len([u for u in user_list if u.role == UserRole.CUSTOMER])
    
    stats = {
        'total': total_users,
        'active': active_users,
        'admins': admin_users,
        'customers': customer_users
    }
    
    return render_template('admin/users.html',
                         users=user_list,
                         stats=stats,
                         user=user)

@app.route('/admin/users/<user_id>/toggle', methods=['POST'])
@admin_required
def admin_toggle_user(user_id):
    """Toggle user active status"""
    from ecommerce.models.user import User
    user_obj = ecommerce_app.user_repository.find_by_id(user_id)
    if user_obj and isinstance(user_obj, User):
        user_obj.is_active = not user_obj.is_active
        ecommerce_app.user_repository.save(user_obj)
        flash(f'User {user_obj.username} {"activated" if user_obj.is_active else "deactivated"}', 'success')
    else:
        flash('User not found', 'danger')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<user_id>/delete', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    """Delete a user"""
    from ecommerce.models.user import User
    user_obj = ecommerce_app.user_repository.find_by_id(user_id)
    current_user = get_user()
    
    if not user_obj:
        flash('User not found', 'danger')
    elif user_obj.id == current_user.id:
        flash('You cannot delete your own account', 'danger')
    elif isinstance(user_obj, User):
        username = user_obj.username
        ecommerce_app.user_repository.delete(user_obj.id)
        flash(f'User {username} deleted successfully', 'success')
    else:
        flash('Invalid user', 'danger')
    
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<user_id>/change_role', methods=['POST'])
@admin_required
def admin_change_role(user_id):
    """Change user role"""
    from ecommerce.models.user import User
    user_obj = ecommerce_app.user_repository.find_by_id(user_id)
    new_role = request.form.get('role')
    
    if user_obj and isinstance(user_obj, User) and new_role:
        try:
            user_obj.role = UserRole[new_role.upper()]
            ecommerce_app.user_repository.save(user_obj)
            flash(f'User {user_obj.username} role changed to {new_role}', 'success')
        except (KeyError, ValueError):
            flash('Invalid role', 'danger')
    else:
        flash('User not found or invalid role', 'danger')
    
    return redirect(url_for('admin_users'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

