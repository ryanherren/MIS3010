#!/usr/bin/env python3
"""
Simple installation script for MIS 3010 Flask App
Handles Python version compatibility automatically
"""

import sys
import subprocess
import os

def run_command(cmd):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {cmd}")
            return True
        else:
            print(f"✗ {cmd}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗ {cmd}")
        print(f"Error: {e}")
        return False

def main():
    print("🚀 MIS 3010 Flask App Installation Script")
    print("=" * 50)
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Determine which packages to install
    if python_version >= (3, 13):
        print("📦 Installing packages for Python 3.13+...")
        packages = [
            "Flask>=3.0.0",
            "Flask-SQLAlchemy>=3.1.0", 
            "Flask-Login>=0.6.0",
            "Flask-WTF>=1.2.0",
            "WTForms>=3.1.0",
            "Werkzeug>=3.0.0"
        ]
    else:
        print("📦 Installing packages for Python 3.8-3.12...")
        packages = [
            "Flask==2.3.3",
            "Flask-SQLAlchemy==3.0.5",
            "Flask-Login==0.6.3", 
            "Flask-WTF==1.1.1",
            "WTForms==3.0.1",
            "Werkzeug==2.3.7"
        ]
    
    # Install packages
    success_count = 0
    for package in packages:
        if run_command(f"pip install '{package}'"):
            success_count += 1
    
    print("\n" + "=" * 50)
    if success_count == len(packages):
        print("🎉 Installation completed successfully!")
        print("\nTo run the application:")
        print("  python app.py")
        print("\nThen open: http://localhost:5000")
        print("Login with: ryanherren / admin123")
    else:
        print(f"⚠️  Installation completed with {len(packages) - success_count} errors")
        print("\nTry installing manually:")
        print("  pip install Flask Flask-SQLAlchemy Flask-Login Flask-WTF")

if __name__ == "__main__":
    main()
