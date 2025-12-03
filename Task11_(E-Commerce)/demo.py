"""
Quick demo script to test the e-commerce system programmatically
"""
from decimal import Decimal
from ecommerce.app import ECommerceApp
from ecommerce.models.user import UserRole


def run_demo():
    """Run a quick demonstration of the system"""
    print("=" * 60)
    print("E-COMMERCE SYSTEM DEMO")
    print("=" * 60)
    
    # Initialize app
    app = ECommerceApp()
    print("\n✓ System initialized")
    
    # Register a test user
    try:
        user = app.auth_service.register(
            username="testuser",
            email="test@example.com",
            password="test123",
            first_name="Test",
            last_name="User"
        )
        print(f"✓ Registered user: {user.username}")
    except ValueError as e:
        print(f"User may already exist: {e}")
        # Try to login instead
        user = app.auth_service.login("testuser", "test123")
        if user:
            print(f"✓ Logged in as: {user.username}")
    
    # Login as admin
    admin = app.auth_service.login("admin", "admin123")
    if admin:
        app.current_user = admin
        print(f"✓ Logged in as admin: {admin.username}")
    
    # View categories
    categories = app.category_service.get_all_categories(active_only=True)
    print(f"\n✓ Found {len(categories)} categories")
    for cat in categories:
        print(f"  - {cat.name}")
    
    # View products
    products = app.product_service.get_all_products(active_only=True)
    print(f"\n✓ Found {len(products)} products")
    for prod in products:
        print(f"  - {prod.name}: ${prod.price:.2f} (Stock: {prod.stock_quantity})")
    
    # Login as test user and add to cart
    test_user = app.auth_service.login("testuser", "test123")
    if test_user:
        app.current_user = test_user
        print(f"\n✓ Logged in as: {test_user.username}")
        
        if products:
            # Add first product to cart
            product = products[0]
            try:
                app.cart_service.add_to_cart(test_user.id, product.id, 2)
                print(f"✓ Added {product.name} to cart")
                
                # View cart
                summary = app.cart_service.get_cart_summary(test_user.id)
                print(f"✓ Cart total: ${summary['total_amount']:.2f}")
                print(f"✓ Cart items: {summary['item_count']}")
            except Exception as e:
                print(f"✗ Error adding to cart: {e}")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETE")
    print("=" * 60)
    print("\nRun 'python main.py' to use the interactive CLI")


if __name__ == "__main__":
    run_demo()

