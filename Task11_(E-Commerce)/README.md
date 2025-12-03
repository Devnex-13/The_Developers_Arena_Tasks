# Advanced E-commerce System

A professional, premium-grade e-commerce platform built with advanced Object-Oriented Programming (OOP) concepts in Python. This system demonstrates enterprise-level software design patterns and best practices.

## 🚀 Features

### Core Functionality
- **User Management**: Complete authentication and authorization system with role-based access control (Customer, Manager, Admin)
- **Product Management**: Full CRUD operations for products with inventory tracking
- **Category Management**: Hierarchical category system for product organization
- **Shopping Cart**: Advanced cart system with real-time updates and validation
- **Order Processing**: Complete order lifecycle management with payment processing
- **Payment Integration**: Multiple payment methods using Strategy pattern

### Advanced OOP Concepts Implemented

1. **Abstract Base Classes (ABC)**
   - `Identifiable`, `Timestampable`, `Validatable` interfaces
   - Repository pattern with abstract base classes
   - Payment strategy interfaces

2. **Design Patterns**
   - **Strategy Pattern**: Payment processing (Credit Card, PayPal, Bank Transfer)
   - **Observer Pattern**: Cart notifications and event handling
   - **Repository Pattern**: Data persistence abstraction
   - **Factory Pattern**: Entity creation with validation

3. **Inheritance & Polymorphism**
   - Base entity classes with common functionality
   - Service layer with polymorphic behavior
   - Product status management with enums

4. **Encapsulation**
   - Private attributes with property decorators
   - Controlled access through getters and setters
   - Validation in setters

5. **Composition**
   - Cart contains CartItems
   - Order contains OrderItems
   - Services composed of repositories

## 📁 Project Structure

```
ecommerce/
├── __init__.py
├── core/
│   ├── __init__.py
│   ├── interfaces.py      # Abstract interfaces
│   └── base.py            # Base classes
├── models/
│   ├── __init__.py
│   ├── user.py            # User entity with roles
│   ├── category.py        # Category entity
│   ├── product.py         # Product entity
│   ├── cart.py            # Shopping cart with observer
│   └── order.py           # Order entity
├── services/
│   ├── __init__.py
│   ├── auth.py            # Authentication & authorization
│   ├── payment.py          # Payment strategies
│   ├── category_service.py # Category management
│   ├── product_service.py  # Product management
│   ├── cart_service.py    # Cart operations
│   └── order_service.py   # Order processing
└── app.py                 # Main application class

main.py                    # CLI interface
requirements.txt           # Dependencies
README.md                  # Documentation
```
## 🛠️ Installation

1. **Clone or download the project**

2. **Ensure Python 3.8+ is installed**
   ```bash
   python --version
   ```

3. **No external dependencies required!**
   The system uses only Python standard library.

## 🎯 Usage

### Option 1: Web Interface (Recommended)

Run the premium web frontend:

```bash
python app_web.py
```

Or use the quick start script:

```bash
python run_web.py
```

Then open your browser to: `http://localhost:5000`

### Option 2: Command Line Interface

Run the interactive CLI:

```bash
python main.py
```

### Sample Credentials

**Admin Account:**
- Username: `admin`
- Password: `admin123`

### Features Walkthrough

1. **Registration & Login**
   - Register new customer accounts
   - Login with credentials
   - Role-based access control

2. **Browse Products**
   - View all available products
   - Search products by name/description
   - Filter by categories
   - View product details and stock

3. **Shopping Cart**
   - Add products to cart
   - Update quantities
   - Remove items
   - Real-time cart total calculation

4. **Checkout**
   - Review order summary
   - Select payment method (Credit Card, PayPal, Bank Transfer)
   - Enter shipping address
   - Process payment
   - Automatic inventory reduction

5. **Order Management**
   - View order history
   - Track order status
   - Cancel orders (if eligible)

6. **Admin Features** (Admin/Manager roles)
   - Create/Update/Delete products
   - Manage categories
   - View all orders
   - User management (Admin only)

## 🏗️ Architecture

### Design Principles

1. **Separation of Concerns**
   - Models: Data entities
   - Services: Business logic
   - Repositories: Data access
   - CLI: User interface

2. **Dependency Injection**
   - Services receive repositories as dependencies
   - Easy to swap implementations

3. **Single Responsibility**
   - Each class has one clear purpose
   - Services handle specific domains

4. **Open/Closed Principle**
   - Easy to extend with new payment methods
   - New product types can be added

5. **Interface Segregation**
   - Small, focused interfaces
   - Classes implement only what they need

### Key Classes

#### Models
- `User`: User entity with authentication
- `Product`: Product with inventory management
- `Category`: Product categorization
- `Cart`: Shopping cart with observer pattern
- `Order`: Order with status management

#### Services
- `AuthenticationService`: User authentication
- `AuthorizationService`: Access control
- `ProductService`: Product operations
- `CategoryService`: Category operations
- `CartService`: Cart management
- `OrderService`: Order processing
- `PaymentProcessor`: Payment strategies

#### Core
- `BaseEntity`: Foundation for all entities
- `BaseRepository`: Data persistence
- `BaseObservable`: Observer pattern implementation

## 🔐 Security Features

- Password hashing (SHA-256, upgradeable to bcrypt)
- Role-based access control (RBAC)
- Input validation
- Stock validation before purchase
- Payment validation

## 📊 Advanced Features

### Observer Pattern
The cart system uses the Observer pattern to notify about changes:
- Item added
- Item removed
- Quantity updated
- Cart cleared

### Strategy Pattern
Payment processing supports multiple methods:
- Credit Card
- PayPal
- Bank Transfer
- Easy to add new payment methods

### Repository Pattern
Abstract data access layer:
- Easy to switch storage backends
- In-memory storage (can be replaced with database)
- Consistent interface across entities

## 🧪 Testing Recommendations

While not included, you can add tests for:
- Unit tests for services
- Integration tests for workflows
- Validation tests for entities
- Payment strategy tests

## 🔄 Extensibility

### Adding New Payment Methods

```python
class CryptocurrencyPayment(PaymentStrategy):
    def process_payment(self, amount, payment_info):
        # Implementation
        pass
    
    def get_payment_method_name(self):
        return "Cryptocurrency"

# Register it
PaymentProcessor.register_payment_method("crypto", CryptocurrencyPayment())
```

### Adding New User Roles

```python
class UserRole(Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    MANAGER = "manager"
    VENDOR = "vendor"  # New role
```

### Database Integration

Replace `BaseRepository` with database-backed implementation:
- SQLAlchemy for SQL databases
- MongoDB driver for NoSQL
- Redis for caching

## 📝 Code Quality

- Type hints throughout
- Comprehensive docstrings
- Error handling
- Validation at multiple levels
- Clean code principles
- SOLID principles

## 🌐 Web Frontend

The system includes a **premium web frontend** built with Flask:

- **Modern UI/UX**: Beautiful, responsive design with Bootstrap 5
- **Full E-commerce Features**: Browse, cart, checkout, orders
- **Admin Panel**: Product and category management
- **AJAX Integration**: Real-time cart updates
- **Professional Styling**: Custom CSS with animations

See `README_WEB.md` for detailed web frontend documentation.

## 🎓 Learning Points

This project demonstrates:
1. Advanced OOP concepts in Python
2. Design patterns in practice
3. Clean architecture
4. Professional code organization
5. Enterprise-level patterns
6. Best practices for maintainability
7. Full-stack web development (Backend + Frontend)

## 🤝 Contributing

This is a demonstration project. Feel free to:
- Add new features
- Improve existing code
- Add database persistence
- Create web interface
- Add unit tests

## 📄 License

This project is for educational and demonstration purposes.

## 👨‍💻 Author

Built as an advanced e-commerce system demonstrating professional Python development practices.

---

**Note**: This is an in-memory system. For production use, integrate with a database and add proper security measures (bcrypt for passwords, HTTPS, etc.).
