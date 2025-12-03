"""
Initialize database with sample data
"""
from app_web import app, ecommerce_app
from ecommerce.database import db
from ecommerce.models.user import UserRole
from decimal import Decimal

def init_sample_data():
    """Initialize database with sample data"""
    with app.app_context():
        # Check if admin user exists
        admin = ecommerce_app.user_repository.find_by_username("admin") if hasattr(ecommerce_app.user_repository, 'find_by_username') else None
        
        if not admin:
            print("Creating sample data...")
            
            # Create admin user
            try:
                admin = ecommerce_app.auth_service.register(
                    username="admin",
                    email="admin@ecommerce.com",
                    password="admin123",
                    role=UserRole.ADMIN,
                    first_name="Admin",
                    last_name="User"
                )
                print("✓ Admin user created")
            except ValueError as e:
                print(f"Admin user: {e}")
            
            # Create sample categories
            try:
                electronics = ecommerce_app.category_service.create_category(
                    name="Electronics",
                    description="Electronic devices and gadgets"
                )
                print("✓ Electronics category created")
                
                clothing = ecommerce_app.category_service.create_category(
                    name="Clothing",
                    description="Apparel and fashion items"
                )
                print("✓ Clothing category created")
                
                books = ecommerce_app.category_service.create_category(
                    name="Books",
                    description="Books and literature"
                )
                print("✓ Books category created")
                
                # Create sample products
                ecommerce_app.product_service.create_product(
                    name="Laptop Pro 15",
                    price=Decimal("1299.99"),
                    category_id=electronics.id,
                    description="High-performance laptop with 16GB RAM",
                    stock_quantity=50
                )
                print("✓ Laptop Pro 15 created")
                
                ecommerce_app.product_service.create_product(
                    name="Wireless Mouse",
                    price=Decimal("29.99"),
                    category_id=electronics.id,
                    description="Ergonomic wireless mouse",
                    stock_quantity=100
                )
                print("✓ Wireless Mouse created")
                
                ecommerce_app.product_service.create_product(
                    name="Cotton T-Shirt",
                    price=Decimal("19.99"),
                    category_id=clothing.id,
                    description="Comfortable cotton t-shirt",
                    stock_quantity=200
                )
                print("✓ Cotton T-Shirt created")
                
                ecommerce_app.product_service.create_product(
                    name="Python Programming Book",
                    price=Decimal("49.99"),
                    category_id=books.id,
                    description="Complete guide to Python programming",
                    stock_quantity=75
                )
                print("✓ Python Programming Book created")
                
            except Exception as e:
                print(f"Error creating sample data: {e}")
        else:
            print("Sample data already exists")

if __name__ == '__main__':
    print("Initializing database...")
    init_sample_data()
    print("\n✓ Database initialization complete!")
    print("\nDefault admin credentials:")
    print("  Username: admin")
    print("  Password: admin123")

