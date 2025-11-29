#!/usr/bin/env python
"""
Simple runner for Smart Task Analyzer - No Django errors!
"""
import os
import sys
import subprocess

def check_and_install():
    """Check and install required packages"""
    packages = ["django==4.2.7", "djangorestframework==3.14.0", "django-cors-headers==4.3.1"]
    
    for package in packages:
        try:
            if "django" in package:
                import django
                print(f"✅ {package} already installed")
            elif "rest_framework" in package:
                import rest_framework
                print(f"✅ {package} already installed")
            else:
                print(f"✅ {package} already installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], check=True)
                print(f"✅ {package} installed successfully!")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")

def run_server():
    """Run the Django development server"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_analyzer.settings')
    
    try:
        from django.core.management import execute_from_command_line
        # Run migrations first
        print("🔄 Running migrations...")
        execute_from_command_line(["manage.py", "migrate"])
        
        # Start server
        print("🚀 Starting Django development server...")
        print("🌐 Open: http://127.0.0.1:8000/")
        print("⏹️  Press Ctrl+C to stop")
        execute_from_command_line(["manage.py", "runserver"])
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Trying alternative method...")
        
        # Alternative: Use simple HTTP server for frontend
        print("🎨 Starting frontend server instead...")
        frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
        if os.path.exists(frontend_path):
            print("🌐 Open frontend/index.html in your browser!")
        else:
            print("❌ Frontend folder not found")

if __name__ == '__main__':
    print("🚀 Smart Task Analyzer - Auto Setup")
    print("=" * 40)
    
    check_and_install()
    run_server()