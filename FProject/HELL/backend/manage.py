#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess

def install_django():
    """Install Django if not available"""
    try:
        import django
        print("✅ Django is already installed!")
        return True
    except ImportError:
        print("📦 Django not found. Installing Django...")
        try:
            # Try different methods to install Django
            methods = [
                [sys.executable, "-m", "pip", "install", "django==4.2.7"],
                ["py", "-m", "pip", "install", "django==4.2.7"],
                ["python", "-m", "pip", "install", "django==4.2.7"],
                ["pip", "install", "django==4.2.7"]
            ]
            
            for method in methods:
                try:
                    print(f"🔄 Trying: {' '.join(method)}")
                    result = subprocess.run(method, check=True, capture_output=True, text=True)
                    print("✅ Django installed successfully!")
                    return True
                except (subprocess.CalledProcessError, FileNotFoundError):
                    continue
            
            print("❌ Could not install Django automatically.")
            print("💡 Please install manually: pip install django==4.2.7")
            return False
            
        except Exception as e:
            print(f"❌ Installation failed: {e}")
            return False

def main():
    """Run administrative tasks."""
    # First, ensure Django is installed
    if not install_django():
        print("❌ Please install Django manually and try again.")
        print("💡 Run: pip install django==4.2.7")
        return
    
    # Now try to run Django commands
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_analyzer.settings')
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        print(f"❌ Error importing Django: {exc}")
        print("💡 Try installing Django manually: pip install django==4.2.7")
        return
    
    try:
        execute_from_command_line(sys.argv)
    except Exception as e:
        print(f"❌ Django command failed: {e}")
        print("💡 Try running: python manage.py migrate")

if __name__ == '__main__':
    main()