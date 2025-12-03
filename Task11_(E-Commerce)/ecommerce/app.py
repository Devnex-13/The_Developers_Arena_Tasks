"""
Main E-commerce Application
"""
from typing import Optional
from decimal import Decimal
from .core.base import BaseRepository
from .models.user import User, UserRole
from .models.category import Category
from .models.product import Product, ProductStatus
from .models.cart import Cart
from .models.order import Order
from .services.auth import AuthenticationService, AuthorizationService
from .services.category_service import CategoryService
from .services.product_service import ProductService
from .services.cart_service import CartService
from .services.order_service import OrderService


class ECommerceApp:
    """Main E-commerce application class"""
    
    def __init__(self):
        # Initialize repositories
        self.user_repository = BaseRepository()
        self.category_repository = BaseRepository()
        self.product_repository = BaseRepository()
        self.cart_repository = BaseRepository()
        self.order_repository = BaseRepository()
        
        # Initialize services
        self.auth_service = AuthenticationService(self.user_repository)
        self.authz_service = AuthorizationService()
        self.category_service = CategoryService(self.category_repository)
        self.product_service = ProductService(
            self.product_repository,
            self.category_repository
        )
        self.cart_service = CartService(
            self.cart_repository,
            self.product_repository
        )
        self.order_service = OrderService(
            self.order_repository,
            self.cart_repository,
            self.product_repository
        )
        
        # Current logged-in user
        self.current_user: Optional[User] = None
        
        # Initialize with sample data
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample data for demonstration"""
        # Create admin user
        try:
            admin = self.auth_service.register(
                username="admin",
                email="admin@ecommerce.com",
                password="admin123",
                role=UserRole.ADMIN,
                first_name="Admin",
                last_name="User"
            )
        except ValueError:
            pass  # User already exists
        
        # Create sample categories
        try:
            electronics = self.category_service.create_category(
                name="Electronics",
                description="Electronic devices and gadgets"
            )
            
            clothing = self.category_service.create_category(
                name="Clothing",
                description="Apparel and fashion items"
            )
            
            books = self.category_service.create_category(
                name="Books",
                description="Books and literature"
            )
            
            # Create sample products
            self.product_service.create_product(
                name="Laptop Pro 15",
                price=Decimal("1299.99"),
                category_id=electronics.id,
                description="High-performance laptop with 16GB RAM",
                stock_quantity=50
            )
            
            self.product_service.create_product(
                name="Wireless Mouse",
                price=Decimal("29.99"),
                category_id=electronics.id,
                description="Ergonomic wireless mouse",
                stock_quantity=100
            )
            
            self.product_service.create_product(
                name="Cotton T-Shirt",
                price=Decimal("19.99"),
                category_id=clothing.id,
                description="Comfortable cotton t-shirt",
                stock_quantity=200
            )
            
            self.product_service.create_product(
                name="Python Programming Book",
                price=Decimal("49.99"),
                category_id=books.id,
                description="Complete guide to Python programming",
                stock_quantity=75
            )
        except Exception:
            pass  # Sample data already exists
    
    def login(self, username: str, password: str) -> bool:
        """Login user"""
        user = self.auth_service.login(username, password)
        if user:
            self.current_user = user
            return True
        return False
    
    def logout(self) -> None:
        """Logout current user"""
        self.current_user = None
    
    def register(self, username: str, email: str, password: str, **kwargs) -> bool:
        """Register new user"""
        try:
            user = self.auth_service.register(
                username=username,
                email=email,
                password=password,
                **kwargs
            )
            if user:
                self.current_user = user
                return True
        except ValueError as e:
            print(f"Registration failed: {e}")
        return False
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return self.current_user is not None
    
    def require_auth(self) -> None:
        """Require authentication or raise exception"""
        if not self.is_authenticated():
            raise PermissionError("Authentication required")
    
    def require_admin(self) -> None:
        """Require admin role or raise exception"""
        self.require_auth()
        if not self.current_user.is_admin():
            raise PermissionError("Admin access required")
    
    def require_manager(self) -> None:
        """Require manager or admin role"""
        self.require_auth()
        if not self.current_user.can_manage_products():
            raise PermissionError("Manager or Admin access required")

