"""
Database Reset Script
Use this script to completely reset the database if needed.
WARNING: This will delete all data!
"""

import os
from app import app, db

def reset_database():
    """Delete and recreate the database"""
    with app.app_context():
        # Delete the database file
        db_path = os.path.join('instance', 'blog.db')
        if os.path.exists(db_path):
            os.remove(db_path)
            print(f"✓ Deleted existing database: {db_path}")
        
        # Create all tables
        db.create_all()
        print("✓ Created new database with all tables")
        
        # Create default admin user
        from app import User, Category
        admin = User(
            username="admin",
            email="admin@blog.com",
            is_admin=True,
        )
        admin.set_password("admin123")
        db.session.add(admin)
        
        # Create default category
        category = Category(name="Uncategorized", slug="uncategorized", description="Default category")
        db.session.add(category)
        
        db.session.commit()
        print("✓ Created default admin user (username: admin, password: admin123)")
        print("✓ Created default category")
        print("\nDatabase reset complete!")

if __name__ == "__main__":
    confirm = input("WARNING: This will delete all data! Type 'yes' to continue: ")
    if confirm.lower() == 'yes':
        reset_database()
    else:
        print("Reset cancelled.")

