"""
Main window for Thomson PDF Generator
Central hub with tabbed interface for all functionality
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from typing import Optional
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.ui_utils import UIUtils
from .converter_tab import ConverterTab
from .viewer_tab import ViewerTab
from .editor_tab import EditorTab
from .signer_tab import SignerTab


class MainWindow:
    """Main application window with tabbed interface"""
    
    def __init__(self):
        # Configure CustomTkinter appearance
        ctk.set_appearance_mode("dark")  # "light" or "dark"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Thomson PDF Generator")
        self.root.geometry("1200x800")
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")  # Add icon file if available
        except:
            pass
        
        # Initialize variables
        self.current_file = None
        
        # Setup UI
        self._setup_menu()
        self._setup_main_interface()
        self._setup_status_bar()
        
        # Center window
        UIUtils.center_window(self.root, 1200, 800)
        
        # Configure window closing
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _setup_menu(self):
        """Setup application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Project", command=self._new_project)
        file_menu.add_separator()
        file_menu.add_command(label="Open File", command=self._open_file)
        file_menu.add_command(label="Open Recent", command=self._open_recent)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_closing)
        
        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Batch Convert", command=self._batch_convert)
        tools_menu.add_command(label="Merge PDFs", command=self._merge_pdfs)
        tools_menu.add_command(label="Split PDF", command=self._split_pdf)
        tools_menu.add_separator()
        tools_menu.add_command(label="Generate Certificate", command=self._generate_certificate)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Theme", command=self._toggle_theme)
        view_menu.add_command(label="Full Screen", command=self._toggle_fullscreen)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="User Guide", command=self._show_help)
        help_menu.add_command(label="Keyboard Shortcuts", command=self._show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self._show_about)
    
    def _setup_main_interface(self):
        """Setup main tabbed interface"""
        # Create main frame
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ctk.CTkTabview(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self._create_converter_tab()
        self._create_viewer_tab()
        self._create_editor_tab()
        self._create_signer_tab()
        
        # Set default tab
        self.notebook.set("Converter")
    
    def _create_converter_tab(self):
        """Create file converter tab"""
        tab = self.notebook.add("Converter")
        self.converter_tab = ConverterTab(tab, self)
    
    def _create_viewer_tab(self):
        """Create PDF viewer tab"""
        tab = self.notebook.add("Viewer")
        self.viewer_tab = ViewerTab(tab, self)
    
    def _create_editor_tab(self):
        """Create PDF editor tab"""
        tab = self.notebook.add("Editor")
        self.editor_tab = EditorTab(tab, self)
    
    def _create_signer_tab(self):
        """Create PDF signer tab"""
        tab = self.notebook.add("Signer")
        self.signer_tab = SignerTab(tab, self)
    
    def _setup_status_bar(self):
        """Setup status bar at bottom"""
        self.status_frame = ctk.CTkFrame(self.root, height=30)
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=(0, 10))
        self.status_frame.pack_propagate(False)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="Ready", 
            anchor="w"
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Progress bar (hidden by default)
        self.progress_bar = ctk.CTkProgressBar(self.status_frame)
        self.progress_bar.pack(side=tk.RIGHT, padx=10, pady=5)
        self.progress_bar.pack_forget()  # Hide initially
    
    def update_status(self, message: str, show_progress: bool = False):
        """Update status bar message"""
        self.status_label.configure(text=message)
        
        if show_progress:
            self.progress_bar.pack(side=tk.RIGHT, padx=10, pady=5)
            self.progress_bar.start()
        else:
            self.progress_bar.stop()
            self.progress_bar.pack_forget()
        
        self.root.update_idletasks()
    
    def set_progress(self, value: float):
        """Set progress bar value (0.0 to 1.0)"""
        self.progress_bar.set(value)
        self.root.update_idletasks()
    
    # Menu command implementations
    def _new_project(self):
        """Create new project"""
        self.current_file = None
        self.update_status("New project created")
        # Reset all tabs
        if hasattr(self, 'converter_tab'):
            self.converter_tab.reset()
        if hasattr(self, 'viewer_tab'):
            self.viewer_tab.reset()
        if hasattr(self, 'editor_tab'):
            self.editor_tab.reset()
    
    def _open_file(self):
        """Open file dialog"""
        file_path = UIUtils.select_file("Open File", parent=self.root)
        if file_path:
            self.current_file = file_path
            self.update_status(f"Opened: {os.path.basename(file_path)}")
            
            # Load file in appropriate tab based on type
            if file_path.lower().endswith('.pdf'):
                self.notebook.set("Viewer")
                self.viewer_tab.load_file(file_path)
            else:
                self.notebook.set("Converter")
                self.converter_tab.add_file(file_path)
    
    def _open_recent(self):
        """Open recent files menu (placeholder)"""
        UIUtils.show_info("Recent Files", "Recent files feature coming soon!", self.root)
    
    def _batch_convert(self):
        """Open batch conversion dialog"""
        self.notebook.set("Converter")
        self.converter_tab.show_batch_dialog()
    
    def _merge_pdfs(self):
        """Open PDF merge dialog"""
        self.notebook.set("Viewer")
        self.viewer_tab.show_merge_dialog()
    
    def _split_pdf(self):
        """Open PDF split dialog"""
        self.notebook.set("Viewer")
        self.viewer_tab.show_split_dialog()
    
    def _generate_certificate(self):
        """Open certificate generation dialog"""
        self.notebook.set("Signer")
        self.signer_tab.show_certificate_dialog()
    
    def _toggle_theme(self):
        """Toggle between light and dark themes"""
        current_mode = ctk.get_appearance_mode()
        new_mode = "dark" if current_mode == "light" else "light"
        ctk.set_appearance_mode(new_mode)
        self.update_status(f"Theme changed to {new_mode}")
    
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        current_state = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not current_state)
    
    def _show_help(self):
        """Show help dialog"""
        help_text = """
Thomson PDF Generator - User Guide

CONVERTER TAB:
• Drag and drop files or click 'Add Files' to select files
• Supported formats: .txt, .doc, .docx, .xlsx, images
• Click 'Convert to PDF' to start conversion
• Choose output location and filename

VIEWER TAB:
• Open PDF files to view and navigate
• Use navigation buttons or page input
• Search text within documents
• View document information and metadata

EDITOR TAB:
• Open PDF for editing
• Add text annotations and shapes
• Insert images and highlights
• Rotate, crop, or delete pages

SIGNER TAB:
• Generate or load digital certificates
• Sign PDF documents digitally
• Verify existing signatures
• Manage certificate information

KEYBOARD SHORTCUTS:
• Ctrl+O: Open file
• Ctrl+N: New project
• Ctrl+S: Save (where applicable)
• F11: Toggle fullscreen
• Ctrl+Q: Exit application
        """
        
        # Create help window
        help_window = ctk.CTkToplevel(self.root)
        help_window.title("User Guide")
        help_window.geometry("600x500")
        help_window.transient(self.root)
        help_window.grab_set()
        
        # Center help window
        UIUtils.center_window(help_window, 600, 500)
        
        # Add scrollable text
        text_widget = ctk.CTkTextbox(help_window)
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        text_widget.insert("0.0", help_text)
        text_widget.configure(state="disabled")
    
    def _show_shortcuts(self):
        """Show keyboard shortcuts"""
        shortcuts_text = """
KEYBOARD SHORTCUTS

File Operations:
• Ctrl+N         New project
• Ctrl+O         Open file
• Ctrl+S         Save (context dependent)
• Ctrl+Q         Exit application

View Operations:
• F11            Toggle fullscreen
• Ctrl+1         Switch to Converter tab
• Ctrl+2         Switch to Viewer tab
• Ctrl+3         Switch to Editor tab
• Ctrl+4         Switch to Signer tab

Navigation (in Viewer):
• Page Up        Previous page
• Page Down      Next page
• Home           First page
• End            Last page
• Ctrl+F         Find text

General:
• F1             Show help
• Alt+F4         Close window
• Esc            Cancel current operation
        """
        
        UIUtils.show_info("Keyboard Shortcuts", shortcuts_text, self.root)
    
    def _show_about(self):
        """Show about dialog"""
        about_text = """
Thomson PDF Generator
Version 1.0.0

A comprehensive PDF converter, viewer, editor, and signing tool.

Features:
• Convert multiple file formats to PDF
• View and navigate PDF documents
• Edit PDF content with annotations
• Digitally sign PDF documents
• All processing done locally (no external APIs)

Copyright © 2025 Thomson-BG
Licensed under MIT License

Built with Python, CustomTkinter, ReportLab, and PyPDF2.
        """
        
        UIUtils.show_info("About Thomson PDF Generator", about_text, self.root)
    
    def _on_closing(self):
        """Handle application closing"""
        if UIUtils.ask_yes_no("Exit", "Are you sure you want to exit?", self.root):
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Start the application"""
        self.root.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()