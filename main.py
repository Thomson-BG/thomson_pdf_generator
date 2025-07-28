#!/usr/bin/env python3
"""
Thomson PDF Generator
Main application entry point

A comprehensive PDF converter, viewer, editor, and signing tool
"""
import os
import sys
import tkinter as tk
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from gui.main_window import MainWindow
except ImportError as e:
    print(f"Error importing GUI modules: {e}")
    print("Please ensure all dependencies are installed:")
    print("pip install -r requirements.txt")
    sys.exit(1)


def check_dependencies():
    """Check if all required dependencies are available"""
    required_modules = [
        'customtkinter',
        'reportlab', 
        'PyPDF2',
        'docx',
        'openpyxl',
        'PIL',
        'cryptography'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print("Missing required dependencies:")
        for module in missing_modules:
            print(f"  - {module}")
        print("\nPlease install missing dependencies:")
        print("pip install -r requirements.txt")
        return False
    
    return True


def setup_error_handling():
    """Setup global error handling"""
    def handle_exception(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        error_msg = f"An unexpected error occurred:\n\n{exc_type.__name__}: {exc_value}"
        
        # Try to show error in GUI if available
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            tk.messagebox.showerror("Thomson PDF Generator - Error", error_msg)
            root.destroy()
        except:
            # Fallback to console
            print(f"ERROR: {error_msg}")
        
        # Log the full traceback
        import traceback
        traceback.print_exception(exc_type, exc_value, exc_traceback)
    
    sys.excepthook = handle_exception


def main():
    """Main application entry point"""
    print("Thomson PDF Generator starting...")
    
    # Check dependencies first
    if not check_dependencies():
        return 1
    
    # Setup error handling
    setup_error_handling()
    
    try:
        # Create and run the application
        app = MainWindow()
        print("GUI initialized successfully")
        app.run()
        
    except Exception as e:
        print(f"Failed to start application: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("Thomson PDF Generator closed")
    return 0


if __name__ == "__main__":
    sys.exit(main())