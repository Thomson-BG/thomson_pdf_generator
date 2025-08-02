"""
Editor tab for Thomson PDF Generator
PDF editing interface with annotations and modifications
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import os
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple

from core.editor import PDFEditor
from core.pdf_handler import PDFHandler
from utils.ui_utils import UIUtils


class EditorTab:
    """PDF editor tab implementation"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.pdf_editor = PDFEditor()
        self.pdf_handler = PDFHandler()
        self.current_pdf_path = None
        self.current_page = 1
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup editor tab UI"""
        # Main container
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="PDF Editor",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Toolbar
        self._setup_toolbar(main_frame)
        
        # Main content area
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel (tools and options)
        self._setup_left_panel(content_frame)
        
        # Right panel (document editor)
        self._setup_right_panel(content_frame)
        
        # Status bar
        self._setup_status_bar(main_frame)
    
    def _setup_toolbar(self, parent):
        """Setup toolbar with file operations"""
        toolbar_frame = ctk.CTkFrame(parent)
        toolbar_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # File operations
        self.open_btn = ctk.CTkButton(
            toolbar_frame,
            text="Open PDF",
            command=self._open_pdf,
            width=100
        )
        self.open_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        self.save_btn = ctk.CTkButton(
            toolbar_frame,
            text="Save",
            command=self._save_pdf,
            width=80,
            state="disabled"
        )
        self.save_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        self.save_as_btn = ctk.CTkButton(
            toolbar_frame,
            text="Save As",
            command=self._save_as_pdf,
            width=100,
            state="disabled"
        )
        self.save_as_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Separator
        separator = ctk.CTkFrame(toolbar_frame, width=2, height=30)
        separator.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Navigation
        self.page_var = tk.StringVar(value="1")
        page_label = ctk.CTkLabel(toolbar_frame, text="Page:")
        page_label.pack(side=tk.LEFT, padx=5, pady=10)
        
        self.page_entry = ctk.CTkEntry(
            toolbar_frame,
            textvariable=self.page_var,
            width=60,
            state="disabled"
        )
        self.page_entry.pack(side=tk.LEFT, padx=5, pady=10)
        self.page_entry.bind("<Return>", self._goto_page)
        
        self.page_label = ctk.CTkLabel(toolbar_frame, text="of 0")
        self.page_label.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Undo/Redo (placeholder)
        undo_frame = ctk.CTkFrame(toolbar_frame)
        undo_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.undo_btn = ctk.CTkButton(
            undo_frame,
            text="Undo",
            command=self._undo,
            width=60,
            state="disabled"
        )
        self.undo_btn.pack(side=tk.LEFT, padx=2)
        
        self.redo_btn = ctk.CTkButton(
            undo_frame,
            text="Redo",
            command=self._redo,
            width=60,
            state="disabled"
        )
        self.redo_btn.pack(side=tk.LEFT, padx=2)
    
    def _setup_left_panel(self, parent):
        """Setup left panel with editing tools"""
        left_frame = ctk.CTkFrame(parent, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_frame.pack_propagate(False)
        
        # Annotation tools
        tools_label = ctk.CTkLabel(
            left_frame,
            text="Annotation Tools",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        tools_label.pack(pady=(10, 5), padx=10)
        
        tools_frame = ctk.CTkScrollableFrame(left_frame, height=250)
        tools_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Text annotation
        text_frame = ctk.CTkFrame(tools_frame)
        text_frame.pack(fill=tk.X, padx=5, pady=5)
        
        text_label = ctk.CTkLabel(text_frame, text="Add Text", font=ctk.CTkFont(weight="bold"))
        text_label.pack(pady=5)
        
        self.text_entry = ctk.CTkEntry(text_frame, placeholder_text="Enter text...")
        self.text_entry.pack(fill=tk.X, padx=5, pady=2)
        
        self.text_size_var = tk.StringVar(value="12")
        size_frame = ctk.CTkFrame(text_frame)
        size_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ctk.CTkLabel(size_frame, text="Size:").pack(side=tk.LEFT)
        ctk.CTkOptionMenu(size_frame, variable=self.text_size_var, 
                         values=["8", "10", "12", "14", "16", "18", "20"]).pack(side=tk.RIGHT)
        
        self.text_color_var = tk.StringVar(value="black")
        color_frame = ctk.CTkFrame(text_frame)
        color_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ctk.CTkLabel(color_frame, text="Color:").pack(side=tk.LEFT)
        ctk.CTkOptionMenu(color_frame, variable=self.text_color_var,
                         values=["black", "red", "blue", "green", "orange"]).pack(side=tk.RIGHT)
        
        self.add_text_btn = ctk.CTkButton(
            text_frame,
            text="Add Text",
            command=self._add_text_annotation,
            state="disabled"
        )
        self.add_text_btn.pack(pady=5)
        
        # Shape annotation
        shape_frame = ctk.CTkFrame(tools_frame)
        shape_frame.pack(fill=tk.X, padx=5, pady=5)
        
        shape_label = ctk.CTkLabel(shape_frame, text="Add Shape", font=ctk.CTkFont(weight="bold"))
        shape_label.pack(pady=5)
        
        self.shape_type_var = tk.StringVar(value="rectangle")
        ctk.CTkOptionMenu(shape_frame, variable=self.shape_type_var,
                         values=["rectangle", "circle", "line"]).pack(fill=tk.X, padx=5, pady=2)
        
        self.shape_color_var = tk.StringVar(value="red")
        shape_color_frame = ctk.CTkFrame(shape_frame)
        shape_color_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ctk.CTkLabel(shape_color_frame, text="Color:").pack(side=tk.LEFT)
        ctk.CTkOptionMenu(shape_color_frame, variable=self.shape_color_var,
                         values=["red", "blue", "green", "black", "orange"]).pack(side=tk.RIGHT)
        
        self.add_shape_btn = ctk.CTkButton(
            shape_frame,
            text="Add Shape",
            command=self._add_shape_annotation,
            state="disabled"
        )
        self.add_shape_btn.pack(pady=5)
        
        # Highlight tool
        highlight_frame = ctk.CTkFrame(tools_frame)
        highlight_frame.pack(fill=tk.X, padx=5, pady=5)
        
        highlight_label = ctk.CTkLabel(highlight_frame, text="Highlight", font=ctk.CTkFont(weight="bold"))
        highlight_label.pack(pady=5)
        
        self.highlight_color_var = tk.StringVar(value="yellow")
        highlight_color_frame = ctk.CTkFrame(highlight_frame)
        highlight_color_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ctk.CTkLabel(highlight_color_frame, text="Color:").pack(side=tk.LEFT)
        ctk.CTkOptionMenu(highlight_color_frame, variable=self.highlight_color_var,
                         values=["yellow", "green", "pink", "orange", "cyan"]).pack(side=tk.RIGHT)
        
        self.highlight_btn = ctk.CTkButton(
            highlight_frame,
            text="Add Highlight",
            command=self._add_highlight,
            state="disabled"
        )
        self.highlight_btn.pack(pady=5)
        
        # Page operations
        page_ops_label = ctk.CTkLabel(
            left_frame,
            text="Page Operations",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        page_ops_label.pack(pady=(10, 5), padx=10)
        
        page_ops_frame = ctk.CTkFrame(left_frame)
        page_ops_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Rotate page
        rotate_frame = ctk.CTkFrame(page_ops_frame)
        rotate_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ctk.CTkLabel(rotate_frame, text="Rotate Page", font=ctk.CTkFont(weight="bold")).pack(pady=2)
        
        rotate_buttons = ctk.CTkFrame(rotate_frame)
        rotate_buttons.pack(fill=tk.X, padx=5, pady=2)
        
        self.rotate_90_btn = ctk.CTkButton(
            rotate_buttons,
            text="90°",
            command=lambda: self._rotate_page(90),
            width=50,
            state="disabled"
        )
        self.rotate_90_btn.pack(side=tk.LEFT, padx=2)
        
        self.rotate_180_btn = ctk.CTkButton(
            rotate_buttons,
            text="180°",
            command=lambda: self._rotate_page(180),
            width=50,
            state="disabled"
        )
        self.rotate_180_btn.pack(side=tk.LEFT, padx=2)
        
        self.rotate_270_btn = ctk.CTkButton(
            rotate_buttons,
            text="270°",
            command=lambda: self._rotate_page(270),
            width=50,
            state="disabled"
        )
        self.rotate_270_btn.pack(side=tk.LEFT, padx=2)
        
        # Delete page
        self.delete_page_btn = ctk.CTkButton(
            page_ops_frame,
            text="Delete Current Page",
            command=self._delete_page,
            state="disabled"
        )
        self.delete_page_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Insert blank page
        self.insert_page_btn = ctk.CTkButton(
            page_ops_frame,
            text="Insert Blank Page",
            command=self._insert_blank_page,
            state="disabled"
        )
        self.insert_page_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Insert image
        self.insert_image_btn = ctk.CTkButton(
            page_ops_frame,
            text="Insert Image",
            command=self._insert_image,
            state="disabled"
        )
        self.insert_image_btn.pack(fill=tk.X, padx=5, pady=5)
    
    def _setup_right_panel(self, parent):
        """Setup right panel with document editor"""
        right_frame = ctk.CTkFrame(parent)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Document display area
        self.display_frame = ctk.CTkScrollableFrame(right_frame)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Document text display (simplified editor)
        self.document_text = ctk.CTkTextbox(
            self.display_frame,
            wrap="word",
            font=("Arial", 12)
        )
        self.document_text.pack(fill=tk.BOTH, expand=True)
        
        # Initial message
        self.document_text.insert("0.0", 
            "PDF Editor\n\n"
            "1. Open a PDF document using 'Open PDF' button\n"
            "2. Navigate to the page you want to edit\n"
            "3. Use the tools on the left to add annotations\n"
            "4. Save your changes when done\n\n"
            "Note: This is a simplified editor interface. "
            "For precise positioning, coordinates are estimated based on text position."
        )
        self.document_text.configure(state="disabled")
    
    def _setup_status_bar(self, parent):
        """Setup status bar"""
        self.status_frame = ctk.CTkFrame(parent, height=30)
        self.status_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        self.status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="No document loaded",
            anchor="w"
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    def _open_pdf(self):
        """Open PDF file for editing"""
        file_path = UIUtils.select_file(
            "Open PDF File",
            [("PDF Files", "*.pdf"), ("All Files", "*.*")],
            self.main_window.root
        )
        
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path: str):
        """Load PDF file into editor"""
        try:
            if self.pdf_handler.open_pdf(file_path):
                self.current_pdf_path = file_path
                self.current_page = 1
                self._update_display()
                self._update_controls_state()
                self.status_label.configure(text=f"Loaded: {os.path.basename(file_path)}")
                self.main_window.update_status(f"PDF loaded for editing: {os.path.basename(file_path)}")
            else:
                UIUtils.show_error("Error", "Failed to open PDF file.", self.main_window.root)
        
        except Exception as e:
            UIUtils.show_error("Error", f"Error opening PDF: {str(e)}", self.main_window.root)
    
    def _update_display(self):
        """Update document display"""
        if self.pdf_handler.current_pdf:
            page_count = self.pdf_handler.get_page_count()
            
            if page_count > 0:
                # Update page controls
                self.page_var.set(str(self.current_page))
                self.page_label.configure(text=f"of {page_count}")
                
                # Get and display page text
                page_text = self.pdf_handler.get_page_text(self.current_page)
                
                self.document_text.configure(state="normal")
                self.document_text.delete("0.0", tk.END)
                
                header = f"Editing Page {self.current_page} of {page_count}\n" + "="*50 + "\n\n"
                
                if page_text.strip():
                    self.document_text.insert("0.0", header + page_text)
                else:
                    self.document_text.insert("0.0", header + "(This page contains no extractable text or contains only images)")
                
                # Keep editable for demonstration
                # In a real implementation, you'd want more sophisticated editing
            else:
                self.document_text.configure(state="normal")
                self.document_text.delete("0.0", tk.END)
                self.document_text.insert("0.0", "PDF document is empty or corrupted.")
                self.document_text.configure(state="disabled")
    
    def _update_controls_state(self):
        """Update control states"""
        has_pdf = self.pdf_handler.current_pdf is not None
        state = "normal" if has_pdf else "disabled"
        
        # File operations
        self.save_btn.configure(state=state)
        self.save_as_btn.configure(state=state)
        self.page_entry.configure(state=state)
        
        # Annotation tools
        self.add_text_btn.configure(state=state)
        self.add_shape_btn.configure(state=state)
        self.highlight_btn.configure(state=state)
        
        # Page operations
        self.rotate_90_btn.configure(state=state)
        self.rotate_180_btn.configure(state=state)
        self.rotate_270_btn.configure(state=state)
        self.delete_page_btn.configure(state=state)
        self.insert_page_btn.configure(state=state)
        self.insert_image_btn.configure(state=state)
    
    def _goto_page(self, event=None):
        """Go to specific page"""
        try:
            page_num = int(self.page_var.get())
            page_count = self.pdf_handler.get_page_count()
            
            if 1 <= page_num <= page_count:
                self.current_page = page_num
                self._update_display()
            else:
                UIUtils.show_warning("Invalid Page", f"Page number must be between 1 and {page_count}.", self.main_window.root)
                self.page_var.set(str(self.current_page))
        
        except ValueError:
            UIUtils.show_warning("Invalid Input", "Please enter a valid page number.", self.main_window.root)
            self.page_var.set(str(self.current_page))
    
    def _add_text_annotation(self):
        """Add text annotation to current page"""
        if not self.current_pdf_path:
            return
        
        text = self.text_entry.get().strip()
        if not text:
            UIUtils.show_warning("No Text", "Please enter text to add.", self.main_window.root)
            return
        
        # For demo purposes, use fixed coordinates
        # In a real implementation, you'd have a more sophisticated positioning system
        x, y = 100, 700  # Fixed position for demo
        font_size = int(self.text_size_var.get())
        color = self.text_color_var.get()
        
        # Create temporary output path
        temp_path = self.current_pdf_path + ".temp"
        
        try:
            if self.pdf_editor.add_text_annotation(
                self.current_pdf_path, self.current_page, x, y, text, font_size, color, temp_path
            ):
                # Replace original with modified version
                import shutil
                shutil.move(temp_path, self.current_pdf_path)
                
                # Reload the document
                self.pdf_handler.open_pdf(self.current_pdf_path)
                self._update_display()
                
                self.main_window.update_status(f"Added text annotation: {text}")
                self.text_entry.delete(0, tk.END)
            else:
                UIUtils.show_error("Error", "Failed to add text annotation.", self.main_window.root)
        
        except Exception as e:
            UIUtils.show_error("Error", f"Error adding text annotation: {str(e)}", self.main_window.root)
            # Clean up temp file if it exists
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def _add_shape_annotation(self):
        """Add shape annotation to current page"""
        if not self.current_pdf_path:
            return
        
        shape_type = self.shape_type_var.get()
        color = self.shape_color_var.get()
        
        # For demo purposes, use fixed coordinates
        coordinates = [150, 600, 300, 650]  # x1, y1, x2, y2
        
        temp_path = self.current_pdf_path + ".temp"
        
        try:
            if self.pdf_editor.add_shape_annotation(
                self.current_pdf_path, self.current_page, shape_type, coordinates, color, output_path=temp_path
            ):
                # Replace original with modified version
                import shutil
                shutil.move(temp_path, self.current_pdf_path)
                
                # Reload the document
                self.pdf_handler.open_pdf(self.current_pdf_path)
                self._update_display()
                
                self.main_window.update_status(f"Added {shape_type} annotation")
            else:
                UIUtils.show_error("Error", f"Failed to add {shape_type} annotation.", self.main_window.root)
        
        except Exception as e:
            UIUtils.show_error("Error", f"Error adding shape annotation: {str(e)}", self.main_window.root)
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def _add_highlight(self):
        """Add highlight annotation"""
        if not self.current_pdf_path:
            return
        
        color = self.highlight_color_var.get()
        coordinates = [100, 650, 400, 670]  # Highlight area
        
        temp_path = self.current_pdf_path + ".temp"
        
        try:
            if self.pdf_editor.highlight_text(
                self.current_pdf_path, self.current_page, coordinates, color, temp_path
            ):
                import shutil
                shutil.move(temp_path, self.current_pdf_path)
                
                self.pdf_handler.open_pdf(self.current_pdf_path)
                self._update_display()
                
                self.main_window.update_status("Added highlight annotation")
            else:
                UIUtils.show_error("Error", "Failed to add highlight.", self.main_window.root)
        
        except Exception as e:
            UIUtils.show_error("Error", f"Error adding highlight: {str(e)}", self.main_window.root)
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def _rotate_page(self, rotation: int):
        """Rotate current page"""
        if not self.current_pdf_path:
            return
        
        temp_path = self.current_pdf_path + ".temp"
        
        try:
            if self.pdf_editor.rotate_page(self.current_pdf_path, self.current_page, rotation, temp_path):
                import shutil
                shutil.move(temp_path, self.current_pdf_path)
                
                self.pdf_handler.open_pdf(self.current_pdf_path)
                self._update_display()
                
                self.main_window.update_status(f"Rotated page {self.current_page} by {rotation} degrees")
            else:
                UIUtils.show_error("Error", "Failed to rotate page.", self.main_window.root)
        
        except Exception as e:
            UIUtils.show_error("Error", f"Error rotating page: {str(e)}", self.main_window.root)
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def _delete_page(self):
        """Delete current page"""
        if not self.current_pdf_path:
            return
        
        page_count = self.pdf_handler.get_page_count()
        if page_count <= 1:
            UIUtils.show_warning("Cannot Delete", "Cannot delete the only page in the document.", self.main_window.root)
            return
        
        if UIUtils.ask_yes_no("Delete Page", f"Are you sure you want to delete page {self.current_page}?", self.main_window.root):
            temp_path = self.current_pdf_path + ".temp"
            
            try:
                if self.pdf_editor.delete_page(self.current_pdf_path, self.current_page, temp_path):
                    import shutil
                    shutil.move(temp_path, self.current_pdf_path)
                    
                    # Adjust current page if necessary
                    if self.current_page > 1:
                        self.current_page -= 1
                    
                    self.pdf_handler.open_pdf(self.current_pdf_path)
                    self._update_display()
                    
                    self.main_window.update_status(f"Deleted page {self.current_page + 1}")
                else:
                    UIUtils.show_error("Error", "Failed to delete page.", self.main_window.root)
            
            except Exception as e:
                UIUtils.show_error("Error", f"Error deleting page: {str(e)}", self.main_window.root)
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    
    def _insert_blank_page(self):
        """Insert blank page after current page"""
        if not self.current_pdf_path:
            return
        
        temp_path = self.current_pdf_path + ".temp"
        
        try:
            if self.pdf_editor.insert_blank_page(self.current_pdf_path, self.current_page + 1, output_path=temp_path):
                import shutil
                shutil.move(temp_path, self.current_pdf_path)
                
                self.current_page += 1
                self.pdf_handler.open_pdf(self.current_pdf_path)
                self._update_display()
                
                self.main_window.update_status(f"Inserted blank page at position {self.current_page}")
            else:
                UIUtils.show_error("Error", "Failed to insert blank page.", self.main_window.root)
        
        except Exception as e:
            UIUtils.show_error("Error", f"Error inserting blank page: {str(e)}", self.main_window.root)
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    def _insert_image(self):
        """Insert image into current page"""
        if not self.current_pdf_path:
            return
        
        image_path = UIUtils.select_file(
            "Select Image",
            [("Images", "*.png;*.jpg;*.jpeg;*.gif;*.bmp"), ("All Files", "*.*")],
            self.main_window.root
        )
        
        if image_path:
            temp_path = self.current_pdf_path + ".temp"
            
            try:
                # Fixed position for demo
                x, y, width, height = 200, 500, 150, 100
                
                if self.pdf_editor.insert_image(
                    self.current_pdf_path, self.current_page, image_path, x, y, width, height, temp_path
                ):
                    import shutil
                    shutil.move(temp_path, self.current_pdf_path)
                    
                    self.pdf_handler.open_pdf(self.current_pdf_path)
                    self._update_display()
                    
                    self.main_window.update_status(f"Inserted image: {os.path.basename(image_path)}")
                else:
                    UIUtils.show_error("Error", "Failed to insert image.", self.main_window.root)
            
            except Exception as e:
                UIUtils.show_error("Error", f"Error inserting image: {str(e)}", self.main_window.root)
                if os.path.exists(temp_path):
                    os.remove(temp_path)
    
    def _save_pdf(self):
        """Save current PDF"""
        if self.current_pdf_path:
            self.main_window.update_status("PDF saved")
            UIUtils.show_info("Saved", "PDF has been saved.", self.main_window.root)
    
    def _save_as_pdf(self):
        """Save PDF with new name"""
        if not self.current_pdf_path:
            return
        
        output_path = UIUtils.save_file(
            "Save PDF As",
            ".pdf",
            [("PDF Files", "*.pdf"), ("All Files", "*.*")],
            self.main_window.root
        )
        
        if output_path:
            try:
                import shutil
                shutil.copy2(self.current_pdf_path, output_path)
                self.current_pdf_path = output_path
                self.main_window.update_status(f"Saved as: {os.path.basename(output_path)}")
                UIUtils.show_info("Saved", f"PDF saved as: {os.path.basename(output_path)}", self.main_window.root)
            except Exception as e:
                UIUtils.show_error("Error", f"Failed to save PDF: {str(e)}", self.main_window.root)
    
    def _undo(self):
        """Undo last operation (placeholder)"""
        UIUtils.show_info("Undo", "Undo functionality coming soon!", self.main_window.root)
    
    def _redo(self):
        """Redo last operation (placeholder)"""
        UIUtils.show_info("Redo", "Redo functionality coming soon!", self.main_window.root)
    
    def reset(self):
        """Reset the editor tab"""
        self.pdf_handler.close_pdf()
        self.current_pdf_path = None
        self.current_page = 1
        
        # Reset UI
        self.document_text.configure(state="normal")
        self.document_text.delete("0.0", tk.END)
        self.document_text.insert("0.0", 
            "PDF Editor\n\n"
            "1. Open a PDF document using 'Open PDF' button\n"
            "2. Navigate to the page you want to edit\n"
            "3. Use the tools on the left to add annotations\n"
            "4. Save your changes when done\n\n"
            "Note: This is a simplified editor interface. "
            "For precise positioning, coordinates are estimated based on text position."
        )
        self.document_text.configure(state="disabled")
        
        self.text_entry.delete(0, tk.END)
        self.page_var.set("1")
        self.page_label.configure(text="of 0")
        
        self._update_controls_state()
        self.status_label.configure(text="No document loaded")