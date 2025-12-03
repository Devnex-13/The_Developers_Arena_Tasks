"""
Quick start script for DP Ecommerce Web Application
"""
import sys
import os

# Check if Flask is installed
try:
    import flask
    print("✓ Flask is installed")
except ImportError:
    print("✗ Flask is not installed")
    print("Installing Flask...")
    os.system(f"{sys.executable} -m pip install Flask")
    print("✓ Flask installed successfully")

# Run the application
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  DP ECOMMERCE - WEB APPLICATION")
    print("=" * 60)
    print("\nStarting server...")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    
    from app_web import app
    app.run(debug=True, host='0.0.0.0', port=5000)

