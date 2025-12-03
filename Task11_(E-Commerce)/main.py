"""
E-commerce System CLI Application
"""
import sys
from decimal import Decimal
from ecommerce.app import ECommerceApp
from ecommerce.models.user import UserRole
from ecommerce.models.product import ProductStatus
from ecommerce.models.order import OrderStatus
from ecommerce.services.payment import PaymentProcessor


class CLI:
    """Command Line Interface for E-commerce System"""
    
    def __init__(self):
        self.app = ECommerceApp()
        self.running = True
    
    def print_header(self, title: str):
        """Print formatted header"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)
    
    def print_menu(self, items: list):
        """Print menu items"""
        for i, item in enumerate(items, 1):
            print(f"{i}. {item}")
    
    def get_input(self, prompt: str) -> str:
        """Get user input"""
        return input(f"\n{prompt}: ").strip()
    
    def get_decimal(self, prompt: str) -> Decimal:
        """Get decimal input"""
        while True:
            try:
                value = self.get_input(prompt)
                return Decimal(value)
            except ValueError:
                print("Invalid number. Please try again.")
    
    def get_int(self, prompt: str) -> int:
        """Get integer input"""
        while True:
            try:
                value = self.get_input(prompt)
                return int(value)
            except ValueError:
                print("Invalid number. Please try again.")
    
    def show_main_menu(self):
        """Show main menu"""
        self.print_header("E-COMMERCE SYSTEM")
        
        if not self.app.is_authenticated():
            print("\nYou are not logged in.")
            self.print_menu([
                "Login",
                "Register",
                "View Products",
                "View Categories",
                "Exit"
            ])
        else:
            user = self.app.current_user
            print(f"\nWelcome, {user.full_name} ({user.role.value})!")
            self.print_menu([
                "View Products",
                "View Categories",
                "Search Products",
                "Shopping Cart",
                "My Orders",
                "Account Settings"
            ])
            
            if user.can_manage_products():
                print("\n--- Admin/Manager Options ---")
                self.print_menu([
                    "Manage Products",
                    "Manage Categories",
                    "View All Orders"
                ])
            
            if user.is_admin():
                print("\n--- Admin Only ---")
                self.print_menu([
                    "Manage Users"
                ])
            
            self.print_menu(["Logout", "Exit"])
    
    def handle_login(self):
        """Handle user login"""
        self.print_header("LOGIN")
        username = self.get_input("Username")
        password = self.get_input("Password")
        
        if self.app.login(username, password):
            print("\n✓ Login successful!")
        else:
            print("\n✗ Login failed. Invalid credentials.")
    
    def handle_register(self):
        """Handle user registration"""
        self.print_header("REGISTER")
        username = self.get_input("Username")
        email = self.get_input("Email")
        password = self.get_input("Password")
        first_name = self.get_input("First Name (optional)")
        last_name = self.get_input("Last Name (optional)")
        
        kwargs = {}
        if first_name:
            kwargs['first_name'] = first_name
        if last_name:
            kwargs['last_name'] = last_name
        
        if self.app.register(username, email, password, **kwargs):
            print("\n✓ Registration successful! You are now logged in.")
        else:
            print("\n✗ Registration failed.")
    
    def handle_view_products(self):
        """View all products"""
        self.print_header("PRODUCTS")
        products = self.app.product_service.get_all_products(active_only=True)
        
        if not products:
            print("\nNo products available.")
            return
        
        for i, product in enumerate(products, 1):
            status_icon = "✓" if product.is_available() else "✗"
            print(f"\n{i}. {status_icon} {product.name}")
            print(f"   Price: ${product.price:.2f}")
            print(f"   Stock: {product.stock_quantity}")
            if product.description:
                print(f"   Description: {product.description}")
            print(f"   ID: {product.id}")
        
        if self.app.is_authenticated():
            choice = self.get_input("\nEnter product number to add to cart (or press Enter to go back)")
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(products):
                    product = products[idx]
                    quantity = self.get_int("Quantity")
                    try:
                        self.app.cart_service.add_to_cart(
                            self.app.current_user.id,
                            product.id,
                            quantity
                        )
                        print(f"\n✓ Added {quantity} x {product.name} to cart!")
                    except Exception as e:
                        print(f"\n✗ Error: {e}")
    
    def handle_view_categories(self):
        """View all categories"""
        self.print_header("CATEGORIES")
        categories = self.app.category_service.get_all_categories(active_only=True)
        
        if not categories:
            print("\nNo categories available.")
            return
        
        for i, category in enumerate(categories, 1):
            print(f"\n{i}. {category.name}")
            if category.description:
                print(f"   {category.description}")
            
            # Show products in category
            products = self.app.product_service.get_products_by_category(category.id)
            print(f"   Products: {len(products)}")
    
    def handle_search_products(self):
        """Search products"""
        self.print_header("SEARCH PRODUCTS")
        query = self.get_input("Search query")
        products = self.app.product_service.search_products(query)
        
        if not products:
            print(f"\nNo products found for '{query}'")
            return
        
        print(f"\nFound {len(products)} product(s):")
        for i, product in enumerate(products, 1):
            print(f"\n{i}. {product.name} - ${product.price:.2f}")
    
    def handle_shopping_cart(self):
        """Handle shopping cart operations"""
        self.app.require_auth()
        user_id = self.app.current_user.id
        
        while True:
            self.print_header("SHOPPING CART")
            summary = self.app.cart_service.get_cart_summary(user_id)
            
            if summary['item_count'] == 0:
                print("\nYour cart is empty.")
            else:
                print(f"\nTotal Items: {summary['item_count']}")
                print(f"Total Amount: ${summary['total_amount']:.2f}")
                print("\nItems:")
                for item in summary['items']:
                    print(f"  - {item['product_name']} x{item['quantity']} = ${item['subtotal']:.2f}")
            
            self.print_menu([
                "Add Product",
                "Update Quantity",
                "Remove Item",
                "Checkout",
                "Clear Cart",
                "Back"
            ])
            
            choice = self.get_input("Choice")
            
            if choice == "1":
                self.handle_add_to_cart()
            elif choice == "2":
                self.handle_update_cart_item()
            elif choice == "3":
                self.handle_remove_from_cart()
            elif choice == "4":
                self.handle_checkout()
                break
            elif choice == "5":
                self.app.cart_service.clear_cart(user_id)
                print("\n✓ Cart cleared!")
            elif choice == "6" or choice.lower() == "back":
                break
    
    def handle_add_to_cart(self):
        """Add product to cart"""
        products = self.app.product_service.get_all_products(active_only=True)
        for i, p in enumerate(products, 1):
            print(f"{i}. {p.name} - ${p.price:.2f} (Stock: {p.stock_quantity})")
        
        idx = self.get_int("Product number") - 1
        if 0 <= idx < len(products):
            product = products[idx]
            quantity = self.get_int("Quantity")
            try:
                self.app.cart_service.add_to_cart(
                    self.app.current_user.id,
                    product.id,
                    quantity
                )
                print(f"\n✓ Added to cart!")
            except Exception as e:
                print(f"\n✗ Error: {e}")
    
    def handle_update_cart_item(self):
        """Update cart item quantity"""
        summary = self.app.cart_service.get_cart_summary(self.app.current_user.id)
        if summary['item_count'] == 0:
            print("\nCart is empty.")
            return
        
        for i, item in enumerate(summary['items'], 1):
            print(f"{i}. {item['product_name']} - Quantity: {item['quantity']}")
        
        idx = self.get_int("Item number") - 1
        if 0 <= idx < len(summary['items']):
            item = summary['items'][idx]
            quantity = self.get_int("New quantity")
            try:
                self.app.cart_service.update_cart_item(
                    self.app.current_user.id,
                    item['product_id'],
                    quantity
                )
                print("\n✓ Cart updated!")
            except Exception as e:
                print(f"\n✗ Error: {e}")
    
    def handle_remove_from_cart(self):
        """Remove item from cart"""
        summary = self.app.cart_service.get_cart_summary(self.app.current_user.id)
        if summary['item_count'] == 0:
            print("\nCart is empty.")
            return
        
        for i, item in enumerate(summary['items'], 1):
            print(f"{i}. {item['product_name']}")
        
        idx = self.get_int("Item number to remove") - 1
        if 0 <= idx < len(summary['items']):
            item = summary['items'][idx]
            self.app.cart_service.remove_from_cart(
                self.app.current_user.id,
                item['product_id']
            )
            print("\n✓ Item removed!")
    
    def handle_checkout(self):
        """Handle checkout process"""
        self.print_header("CHECKOUT")
        summary = self.app.cart_service.get_cart_summary(self.app.current_user.id)
        
        if summary['item_count'] == 0:
            print("\nCart is empty. Cannot checkout.")
            return
        
        print(f"\nOrder Summary:")
        print(f"Items: {summary['item_count']}")
        print(f"Subtotal: ${summary['total_amount']:.2f}")
        tax = summary['total_amount'] * 0.10
        shipping = 5.00
        total = summary['total_amount'] + tax + shipping
        print(f"Tax (10%): ${tax:.2f}")
        print(f"Shipping: ${shipping:.2f}")
        print(f"Total: ${total:.2f}")
        
        print("\nPayment Methods:")
        methods = PaymentProcessor.get_available_methods()
        for i, method in enumerate(methods, 1):
            print(f"{i}. {method.replace('_', ' ').title()}")
        
        method_idx = self.get_int("Payment method number") - 1
        if not (0 <= method_idx < len(methods)):
            print("\n✗ Invalid payment method.")
            return
        
        payment_method = methods[method_idx]
        payment_info = {}
        
        if payment_method == "credit_card":
            payment_info['card_number'] = self.get_input("Card Number")
            payment_info['cvv'] = self.get_input("CVV")
            payment_info['expiry'] = self.get_input("Expiry (MM/YY)")
        elif payment_method == "paypal":
            payment_info['email'] = self.get_input("PayPal Email")
            payment_info['password'] = self.get_input("PayPal Password")
        elif payment_method == "bank_transfer":
            payment_info['account_number'] = self.get_input("Account Number")
            payment_info['routing_number'] = self.get_input("Routing Number")
        
        shipping_address = self.get_input("Shipping Address")
        
        try:
            order = self.app.order_service.create_order_from_cart(
                self.app.current_user.id,
                payment_method,
                payment_info,
                shipping_address
            )
            if order:
                print(f"\n✓ Order placed successfully!")
                print(f"Order ID: {order.id}")
                print(f"Status: {order.status.value}")
            else:
                print("\n✗ Failed to create order.")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def handle_my_orders(self):
        """View user orders"""
        self.app.require_auth()
        self.print_header("MY ORDERS")
        orders = self.app.order_service.get_user_orders(self.app.current_user.id)
        
        if not orders:
            print("\nNo orders found.")
            return
        
        for i, order in enumerate(orders, 1):
            print(f"\n{i}. Order #{order.id[:8]}")
            print(f"   Status: {order.status.value}")
            print(f"   Total: ${order.total:.2f}")
            print(f"   Items: {len(order.items)}")
            print(f"   Date: {order.created_at.strftime('%Y-%m-%d %H:%M')}")
    
    def handle_manage_products(self):
        """Manage products (Admin/Manager)"""
        self.app.require_manager()
        
        while True:
            self.print_header("MANAGE PRODUCTS")
            self.print_menu([
                "List All Products",
                "Add Product",
                "Update Product",
                "Delete Product",
                "Back"
            ])
            
            choice = self.get_input("Choice")
            
            if choice == "1":
                products = self.app.product_service.get_all_products()
                for p in products:
                    print(f"\n{p.name} - ${p.price:.2f} - Stock: {p.stock_quantity} - Status: {p.status.value}")
            elif choice == "2":
                self.handle_add_product()
            elif choice == "3":
                self.handle_update_product()
            elif choice == "4":
                self.handle_delete_product()
            elif choice == "5" or choice.lower() == "back":
                break
    
    def handle_add_product(self):
        """Add new product"""
        name = self.get_input("Product Name")
        price = self.get_decimal("Price")
        
        categories = self.app.category_service.get_all_categories(active_only=True)
        for i, c in enumerate(categories, 1):
            print(f"{i}. {c.name}")
        cat_idx = self.get_int("Category number") - 1
        if not (0 <= cat_idx < len(categories)):
            print("Invalid category.")
            return
        
        category_id = categories[cat_idx].id
        description = self.get_input("Description (optional)")
        stock = self.get_int("Stock Quantity")
        
        try:
            product = self.app.product_service.create_product(
                name=name,
                price=price,
                category_id=category_id,
                description=description if description else None,
                stock_quantity=stock
            )
            print(f"\n✓ Product created: {product.name}")
        except Exception as e:
            print(f"\n✗ Error: {e}")
    
    def handle_update_product(self):
        """Update product"""
        products = self.app.product_service.get_all_products()
        for i, p in enumerate(products, 1):
            print(f"{i}. {p.name}")
        
        idx = self.get_int("Product number") - 1
        if not (0 <= idx < len(products)):
            print("Invalid product.")
            return
        
        product = products[idx]
        print(f"\nCurrent: {product.name} - ${product.price:.2f} - Stock: {product.stock_quantity}")
        
        name = self.get_input("New name (or press Enter to keep)")
        if name:
            try:
                self.app.product_service.update_product(product.id, name=name)
                print("\n✓ Product updated!")
            except Exception as e:
                print(f"\n✗ Error: {e}")
    
    def handle_delete_product(self):
        """Delete product"""
        products = self.app.product_service.get_all_products()
        for i, p in enumerate(products, 1):
            print(f"{i}. {p.name}")
        
        idx = self.get_int("Product number") - 1
        if not (0 <= idx < len(products)):
            print("Invalid product.")
            return
        
        product = products[idx]
        if self.app.product_service.delete_product(product.id):
            print(f"\n✓ Product deleted: {product.name}")
    
    def handle_manage_categories(self):
        """Manage categories (Admin/Manager)"""
        self.app.require_manager()
        
        while True:
            self.print_header("MANAGE CATEGORIES")
            categories = self.app.category_service.get_all_categories()
            for i, c in enumerate(categories, 1):
                print(f"{i}. {c.name} - {'Active' if c.is_active else 'Inactive'}")
            
            self.print_menu([
                "Add Category",
                "Update Category",
                "Delete Category",
                "Back"
            ])
            
            choice = self.get_input("Choice")
            
            if choice == "1":
                name = self.get_input("Category Name")
                description = self.get_input("Description (optional)")
                try:
                    category = self.app.category_service.create_category(
                        name=name,
                        description=description if description else None
                    )
                    print(f"\n✓ Category created: {category.name}")
                except Exception as e:
                    print(f"\n✗ Error: {e}")
            elif choice == "2" or choice == "3":
                print("Feature not fully implemented in CLI")
            elif choice == "4" or choice.lower() == "back":
                break
    
    def run(self):
        """Run the CLI application"""
        print("\n" + "=" * 60)
        print("  WELCOME TO ADVANCED E-COMMERCE SYSTEM")
        print("=" * 60)
        
        while self.running:
            try:
                self.show_main_menu()
                choice = self.get_input("\nEnter your choice")
                
                if not self.app.is_authenticated():
                    if choice == "1":
                        self.handle_login()
                    elif choice == "2":
                        self.handle_register()
                    elif choice == "3":
                        self.handle_view_products()
                    elif choice == "4":
                        self.handle_view_categories()
                    elif choice == "5" or choice.lower() == "exit":
                        print("\nThank you for using E-commerce System!")
                        break
                else:
                    user = self.app.current_user
                    
                    # Handle logout and exit first
                    if choice.lower() == "logout":
                        self.app.logout()
                        print("\n✓ Logged out successfully!")
                        continue
                    elif choice.lower() == "exit":
                        print("\nThank you for using E-commerce System!")
                        break
                    
                    # Main menu options
                    menu_map = {
                        "1": self.handle_view_products,
                        "2": self.handle_view_categories,
                        "3": self.handle_search_products,
                        "4": self.handle_shopping_cart,
                        "5": self.handle_my_orders,
                        "6": lambda: print("\nAccount settings not implemented in CLI")
                    }
                    
                    if choice in menu_map:
                        menu_map[choice]()
                    elif user.can_manage_products():
                        # Admin/Manager menu options (starting from 7)
                        menu_num = 7
                        if choice == str(menu_num):
                            self.handle_manage_products()
                        elif choice == str(menu_num + 1):
                            self.handle_manage_categories()
                        elif user.is_admin() and choice == str(menu_num + 2):
                            print("\nUser management not fully implemented in CLI")
                    else:
                        print("\nInvalid choice. Please try again.")
                        
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
            except Exception as e:
                print(f"\n✗ Error: {e}")
                import traceback
                traceback.print_exc()


if __name__ == "__main__":
    cli = CLI()
    cli.run()

