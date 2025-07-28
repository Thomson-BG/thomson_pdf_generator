"""
UI utilities for Thomson PDF Generator
Common UI functions and styling helpers
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Callable, Optional, List, Tuple
import customtkinter as ctk


class UIUtils:
    """Utility class for UI operations"""
    
    # Color schemes
    COLORS = {
        'primary': '#1f538d',
        'secondary': '#14a085',
        'success': '#28a745',
        'warning': '#ffc107',
        'error': '#dc3545',
        'info': '#17a2b8',
        'light': '#f8f9fa',
        'dark': '#343a40',
        'background': '#ffffff',
        'text': '#212529'
    }
    
    @staticmethod
    def show_info(title: str, message: str, parent=None):
        """Show info message dialog"""
        messagebox.showinfo(title, message, parent=parent)
    
    @staticmethod
    def show_warning(title: str, message: str, parent=None):
        """Show warning message dialog"""
        messagebox.showwarning(title, message, parent=parent)
    
    @staticmethod
    def show_error(title: str, message: str, parent=None):
        """Show error message dialog"""
        messagebox.showerror(title, message, parent=parent)
    
    @staticmethod
    def ask_yes_no(title: str, message: str, parent=None) -> bool:
        """Ask yes/no question"""
        return messagebox.askyesno(title, message, parent=parent)
    
    @staticmethod
    def select_file(title: str = "Select File", 
                   filetypes: List[Tuple[str, str]] = None,
                   parent=None) -> Optional[str]:
        """Open file selection dialog"""
        if filetypes is None:
            filetypes = [
                ("All Supported", "*.txt;*.doc;*.docx;*.xlsx;*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
                ("Text Files", "*.txt"),
                ("Word Documents", "*.doc;*.docx"),
                ("Excel Files", "*.xlsx"),
                ("Images", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
                ("All Files", "*.*")
            ]
        
        return filedialog.askopenfilename(
            title=title,
            filetypes=filetypes,
            parent=parent
        )
    
    @staticmethod
    def select_files(title: str = "Select Files",
                    filetypes: List[Tuple[str, str]] = None,
                    parent=None) -> List[str]:
        """Open multiple file selection dialog"""
        if filetypes is None:
            filetypes = [
                ("All Supported", "*.txt;*.doc;*.docx;*.xlsx;*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
                ("Text Files", "*.txt"),
                ("Word Documents", "*.doc;*.docx"),
                ("Excel Files", "*.xlsx"),
                ("Images", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"),
                ("All Files", "*.*")
            ]
        
        files = filedialog.askopenfilenames(
            title=title,
            filetypes=filetypes,
            parent=parent
        )
        return list(files) if files else []
    
    @staticmethod
    def save_file(title: str = "Save File",
                 defaultextension: str = ".pdf",
                 filetypes: List[Tuple[str, str]] = None,
                 parent=None) -> Optional[str]:
        """Open save file dialog"""
        if filetypes is None:
            filetypes = [("PDF Files", "*.pdf"), ("All Files", "*.*")]
        
        return filedialog.asksaveasfilename(
            title=title,
            defaultextension=defaultextension,
            filetypes=filetypes,
            parent=parent
        )
    
    @staticmethod
    def select_directory(title: str = "Select Directory", parent=None) -> Optional[str]:
        """Open directory selection dialog"""
        return filedialog.askdirectory(title=title, parent=parent)
    
    @staticmethod
    def create_progress_window(parent, title: str = "Processing...") -> Tuple[tk.Toplevel, ttk.Progressbar, tk.Label]:
        """Create a progress dialog window"""
        progress_window = tk.Toplevel(parent)
        progress_window.title(title)
        progress_window.geometry("400x120")
        progress_window.resizable(False, False)
        progress_window.transient(parent)
        progress_window.grab_set()
        
        # Center the window
        progress_window.update_idletasks()
        x = (progress_window.winfo_screenwidth() // 2) - (400 // 2)
        y = (progress_window.winfo_screenheight() // 2) - (120 // 2)
        progress_window.geometry(f"400x120+{x}+{y}")
        
        # Progress bar
        progress_frame = ttk.Frame(progress_window)
        progress_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        progress_label = tk.Label(progress_frame, text="Initializing...")
        progress_label.pack(pady=(0, 10))
        
        progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        progress_bar.pack(fill=tk.X, pady=(0, 10))
        progress_bar.start()
        
        return progress_window, progress_bar, progress_label
    
    @staticmethod
    def center_window(window, width: int, height: int):
        """Center a window on screen"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Basic email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None