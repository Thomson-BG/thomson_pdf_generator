"""
Viewer tab for Thomson PDF Generator
PDF viewing and basic manipulation interface
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import os
from pathlib import Path
from typing import Optional, List, Dict, Any

from core.pdf_handler import PDFHandler
from utils.ui_utils import UIUtils


class ViewerTab:
    """PDF viewer tab implementation"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.pdf_handler = PDFHandler()
        self.current_page = 1
        self.search_results = []
        self.current_search_index = 0
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup viewer tab UI"""
        # Main container
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="PDF Viewer",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Toolbar
        self._setup_toolbar(main_frame)
        
        # Main content area
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel (document info and navigation)
        self._setup_left_panel(content_frame)
        
        # Right panel (document viewer)
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
        
        self.save_as_btn = ctk.CTkButton(
            toolbar_frame,
            text="Save As",
            command=self._save_as,
            width=100,
            state="disabled"
        )
        self.save_as_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Separator
        separator = ctk.CTkFrame(toolbar_frame, width=2, height=30)
        separator.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Navigation buttons
        self.first_btn = ctk.CTkButton(
            toolbar_frame,
            text="⏮",
            command=self._first_page,
            width=40,
            state="disabled"
        )
        self.first_btn.pack(side=tk.LEFT, padx=2, pady=10)
        
        self.prev_btn = ctk.CTkButton(
            toolbar_frame,
            text="◀",
            command=self._prev_page,
            width=40,
            state="disabled"
        )
        self.prev_btn.pack(side=tk.LEFT, padx=2, pady=10)
        
        # Page input
        self.page_var = tk.StringVar(value="1")
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
        
        self.next_btn = ctk.CTkButton(
            toolbar_frame,
            text="▶",
            command=self._next_page,
            width=40,
            state="disabled"
        )
        self.next_btn.pack(side=tk.LEFT, padx=2, pady=10)
        
        self.last_btn = ctk.CTkButton(
            toolbar_frame,
            text="⏭",
            command=self._last_page,
            width=40,
            state="disabled"
        )
        self.last_btn.pack(side=tk.LEFT, padx=2, pady=10)
        
        # Search
        search_frame = ctk.CTkFrame(toolbar_frame)
        search_frame.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.search_var = tk.StringVar()
        self.search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search text...",
            width=150
        )
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind("<Return>", self._search_text)
        
        self.search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            command=self._search_text,
            width=80,
            state="disabled"
        )
        self.search_btn.pack(side=tk.LEFT, padx=5)
    
    def _setup_left_panel(self, parent):
        """Setup left panel with document info and tools"""
        left_frame = ctk.CTkFrame(parent, width=300)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_frame.pack_propagate(False)
        
        # Document info section
        info_label = ctk.CTkLabel(
            left_frame,
            text="Document Information",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_label.pack(pady=(10, 5), padx=10)
        
        # Info display
        self.info_frame = ctk.CTkScrollableFrame(left_frame, height=200)
        self.info_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.info_text = ctk.CTkTextbox(self.info_frame, height=180)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Tools section
        tools_label = ctk.CTkLabel(
            left_frame,
            text="Tools",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        tools_label.pack(pady=(10, 5), padx=10)
        
        tools_frame = ctk.CTkFrame(left_frame)
        tools_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Extract pages button
        self.extract_btn = ctk.CTkButton(
            tools_frame,
            text="Extract Pages",
            command=self._extract_pages,
            state="disabled"
        )
        self.extract_btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Merge PDFs button
        self.merge_btn = ctk.CTkButton(
            tools_frame,
            text="Merge PDFs",
            command=self.show_merge_dialog,
            state="normal"
        )
        self.merge_btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Split PDF button
        self.split_btn = ctk.CTkButton(
            tools_frame,
            text="Split PDF",
            command=self.show_split_dialog,
            state="disabled"
        )
        self.split_btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Add watermark button
        self.watermark_btn = ctk.CTkButton(
            tools_frame,
            text="Add Watermark",
            command=self._add_watermark,
            state="disabled"
        )
        self.watermark_btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Search results section
        search_label = ctk.CTkLabel(
            left_frame,
            text="Search Results",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        search_label.pack(pady=(10, 5), padx=10)
        
        self.search_frame = ctk.CTkScrollableFrame(left_frame, height=200)
        self.search_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.search_listbox = tk.Listbox(self.search_frame, height=10)
        self.search_listbox.pack(fill=tk.BOTH, expand=True)
        self.search_listbox.bind("<Double-Button-1>", self._goto_search_result)
    
    def _setup_right_panel(self, parent):
        """Setup right panel with document viewer"""
        right_frame = ctk.CTkFrame(parent)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Document display area
        self.display_frame = ctk.CTkScrollableFrame(right_frame)
        self.display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Document text display
        self.document_text = ctk.CTkTextbox(self.display_frame, wrap="word")
        self.document_text.pack(fill=tk.BOTH, expand=True)
        
        # Initial message
        self.document_text.insert("0.0", "No PDF document loaded.\n\nClick 'Open PDF' to load a document.")
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
        """Open PDF file"""
        file_path = UIUtils.select_file(
            "Open PDF File",
            [("PDF Files", "*.pdf")],
            self.main_window.root
        )
        
        if file_path:
            self.load_file(file_path)
    
    def load_file(self, file_path: str):
        """Load PDF file into viewer"""
        try:
            if self.pdf_handler.open_pdf(file_path):
                self.current_page = 1
                self._update_display()
                self._update_navigation_state()
                self._update_document_info()
                self.status_label.configure(text=f"Loaded: {os.path.basename(file_path)}")
                self.main_window.update_status(f"PDF loaded: {os.path.basename(file_path)}")
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
                
                if page_text.strip():
                    self.document_text.insert("0.0", f"Page {self.current_page} of {page_count}\n\n{page_text}")
                else:
                    self.document_text.insert("0.0", f"Page {self.current_page} of {page_count}\n\n(This page contains no extractable text)")
                
                self.document_text.configure(state="disabled")
            else:
                self.document_text.configure(state="normal")
                self.document_text.delete("0.0", tk.END)
                self.document_text.insert("0.0", "PDF document is empty or corrupted.")
                self.document_text.configure(state="disabled")
    
    def _update_navigation_state(self):
        """Update navigation button states"""
        has_pdf = self.pdf_handler.current_pdf is not None
        page_count = self.pdf_handler.get_page_count() if has_pdf else 0
        
        # Enable/disable navigation buttons
        state = "normal" if has_pdf and page_count > 0 else "disabled"
        
        self.first_btn.configure(state=state)
        self.prev_btn.configure(state=state)
        self.next_btn.configure(state=state)
        self.last_btn.configure(state=state)
        self.page_entry.configure(state=state)
        
        # Enable/disable other buttons
        tool_state = "normal" if has_pdf else "disabled"
        self.save_as_btn.configure(state=tool_state)
        self.search_btn.configure(state=tool_state)
        self.extract_btn.configure(state=tool_state)
        self.split_btn.configure(state=tool_state)
        self.watermark_btn.configure(state=tool_state)
        
        # Update navigation button states based on current page
        if has_pdf and page_count > 0:
            if self.current_page <= 1:
                self.first_btn.configure(state="disabled")
                self.prev_btn.configure(state="disabled")
            if self.current_page >= page_count:
                self.next_btn.configure(state="disabled")
                self.last_btn.configure(state="disabled")
    
    def _update_document_info(self):
        """Update document information display"""
        if self.pdf_handler.current_pdf:
            info = self.pdf_handler.get_pdf_info()
            
            info_text = f"""Filename: {info.get('filename', 'Unknown')}
Pages: {info.get('pages', 0)}
File Size: {info.get('file_size', 0):,} bytes

Metadata:
Title: {info.get('title', 'Unknown')}
Author: {info.get('author', 'Unknown')}
Subject: {info.get('subject', 'Unknown')}
Creator: {info.get('creator', 'Unknown')}
Producer: {info.get('producer', 'Unknown')}
Created: {info.get('creation_date', 'Unknown')}
Modified: {info.get('modification_date', 'Unknown')}"""
            
            self.info_text.delete("0.0", tk.END)
            self.info_text.insert("0.0", info_text)
        else:
            self.info_text.delete("0.0", tk.END)
            self.info_text.insert("0.0", "No document loaded")
    
    def _first_page(self):
        """Go to first page"""
        if self.pdf_handler.current_pdf and self.current_page > 1:
            self.current_page = 1
            self._update_display()
            self._update_navigation_state()
    
    def _prev_page(self):
        """Go to previous page"""
        if self.pdf_handler.current_pdf and self.current_page > 1:
            self.current_page -= 1
            self._update_display()
            self._update_navigation_state()
    
    def _next_page(self):
        """Go to next page"""
        page_count = self.pdf_handler.get_page_count()
        if self.pdf_handler.current_pdf and self.current_page < page_count:
            self.current_page += 1
            self._update_display()
            self._update_navigation_state()
    
    def _last_page(self):
        """Go to last page"""
        page_count = self.pdf_handler.get_page_count()
        if self.pdf_handler.current_pdf and self.current_page < page_count:
            self.current_page = page_count
            self._update_display()
            self._update_navigation_state()
    
    def _goto_page(self, event=None):
        """Go to specific page"""
        try:
            page_num = int(self.page_var.get())
            page_count = self.pdf_handler.get_page_count()
            
            if 1 <= page_num <= page_count:
                self.current_page = page_num
                self._update_display()
                self._update_navigation_state()
            else:
                UIUtils.show_warning("Invalid Page", f"Page number must be between 1 and {page_count}.", self.main_window.root)
                self.page_var.set(str(self.current_page))
        
        except ValueError:
            UIUtils.show_warning("Invalid Input", "Please enter a valid page number.", self.main_window.root)
            self.page_var.set(str(self.current_page))
    
    def _search_text(self, event=None):
        """Search for text in document"""
        search_term = self.search_var.get().strip()
        
        if not search_term:
            UIUtils.show_warning("Search", "Please enter text to search for.", self.main_window.root)
            return
        
        if not self.pdf_handler.current_pdf:
            UIUtils.show_warning("Search", "No document loaded.", self.main_window.root)
            return
        
        # Perform search
        self.search_results = self.pdf_handler.search_text(search_term)
        self.current_search_index = 0
        
        # Update search results display
        self.search_listbox.delete(0, tk.END)
        
        if self.search_results:
            for i, result in enumerate(self.search_results):
                context = result['context'][:50] + "..." if len(result['context']) > 50 else result['context']
                display_text = f"Page {result['page']}: {context}"
                self.search_listbox.insert(tk.END, display_text)
            
            self.main_window.update_status(f"Found {len(self.search_results)} matches for '{search_term}'")
        else:
            self.search_listbox.insert(tk.END, "No matches found")
            self.main_window.update_status(f"No matches found for '{search_term}'")
    
    def _goto_search_result(self, event=None):
        """Go to selected search result"""
        selection = self.search_listbox.curselection()
        if selection and self.search_results:
            index = selection[0]
            if 0 <= index < len(self.search_results):
                result = self.search_results[index]
                self.current_page = result['page']
                self._update_display()
                self._update_navigation_state()
    
    def _save_as(self):
        """Save PDF as new file"""
        if not self.pdf_handler.current_pdf:
            return
        
        output_path = UIUtils.save_file(
            "Save PDF As",
            ".pdf",
            [("PDF Files", "*.pdf"), ("All Files", "*.*")],
            self.main_window.root
        )
        
        if output_path:
            try:
                # Simple copy of current PDF
                import shutil
                shutil.copy2(self.pdf_handler.current_path, output_path)
                self.main_window.update_status(f"Saved as: {os.path.basename(output_path)}")
                UIUtils.show_info("Saved", f"PDF saved as: {os.path.basename(output_path)}", self.main_window.root)
            except Exception as e:
                UIUtils.show_error("Error", f"Failed to save PDF: {str(e)}", self.main_window.root)
    
    def _extract_pages(self):
        """Extract specific pages to new PDF"""
        if not self.pdf_handler.current_pdf:
            return
        
        page_count = self.pdf_handler.get_page_count()
        
        # Simple dialog to get page range
        dialog = ctk.CTkInputDialog(
            text=f"Enter page numbers to extract (1-{page_count}):\nExample: 1,3,5-8",
            title="Extract Pages"
        )
        result = dialog.get_input()
        
        if result:
            try:
                # Parse page numbers
                pages = self._parse_page_range(result, page_count)
                
                if pages:
                    output_path = UIUtils.save_file(
                        "Save Extracted Pages",
                        ".pdf",
                        [("PDF Files", "*.pdf")],
                        self.main_window.root
                    )
                    
                    if output_path:
                        if self.pdf_handler.extract_pages(pages, output_path):
                            UIUtils.show_info("Success", f"Extracted {len(pages)} pages to: {os.path.basename(output_path)}", self.main_window.root)
                        else:
                            UIUtils.show_error("Error", "Failed to extract pages.", self.main_window.root)
                else:
                    UIUtils.show_warning("Invalid Range", "No valid pages specified.", self.main_window.root)
            
            except Exception as e:
                UIUtils.show_error("Error", f"Invalid page range: {str(e)}", self.main_window.root)
    
    def _parse_page_range(self, range_str: str, max_page: int) -> List[int]:
        """Parse page range string like '1,3,5-8' into list of page numbers"""
        pages = []
        parts = range_str.replace(" ", "").split(",")
        
        for part in parts:
            if "-" in part:
                # Range like "5-8"
                start, end = part.split("-", 1)
                start_page = int(start)
                end_page = int(end)
                
                if 1 <= start_page <= end_page <= max_page:
                    pages.extend(range(start_page, end_page + 1))
            else:
                # Single page
                page_num = int(part)
                if 1 <= page_num <= max_page:
                    pages.append(page_num)
        
        return sorted(list(set(pages)))  # Remove duplicates and sort
    
    def _add_watermark(self):
        """Add watermark to PDF"""
        if not self.pdf_handler.current_pdf:
            return
        
        # Get watermark text
        dialog = ctk.CTkInputDialog(
            text="Enter watermark text:",
            title="Add Watermark"
        )
        watermark_text = dialog.get_input()
        
        if watermark_text:
            output_path = UIUtils.save_file(
                "Save Watermarked PDF",
                ".pdf",
                [("PDF Files", "*.pdf")],
                self.main_window.root
            )
            
            if output_path:
                if self.pdf_handler.add_watermark(watermark_text, output_path):
                    UIUtils.show_info("Success", f"Watermark added to: {os.path.basename(output_path)}", self.main_window.root)
                else:
                    UIUtils.show_error("Error", "Failed to add watermark.", self.main_window.root)
    
    def show_merge_dialog(self):
        """Show PDF merge dialog"""
        files = UIUtils.select_files(
            "Select PDFs to Merge",
            [("PDF Files", "*.pdf"), ("All Files", "*.*")],
            self.main_window.root
        )
        
        if len(files) >= 2:
            output_path = UIUtils.save_file(
                "Save Merged PDF",
                ".pdf",
                [("PDF Files", "*.pdf")],
                self.main_window.root
            )
            
            if output_path:
                if self.pdf_handler.merge_pdfs(files, output_path):
                    UIUtils.show_info("Success", f"Merged {len(files)} PDFs into: {os.path.basename(output_path)}", self.main_window.root)
                    # Load the merged PDF
                    self.load_file(output_path)
                else:
                    UIUtils.show_error("Error", "Failed to merge PDFs.", self.main_window.root)
        else:
            UIUtils.show_warning("Insufficient Files", "Please select at least 2 PDF files to merge.", self.main_window.root)
    
    def show_split_dialog(self):
        """Show PDF split dialog"""
        if not self.pdf_handler.current_pdf:
            UIUtils.show_warning("No Document", "Please open a PDF document first.", self.main_window.root)
            return
        
        output_dir = UIUtils.select_directory("Select Output Directory", self.main_window.root)
        
        if output_dir:
            page_count = self.pdf_handler.get_page_count()
            
            # Ask for pages per file
            dialog = ctk.CTkInputDialog(
                text=f"Pages per file (1-{page_count}):",
                title="Split PDF"
            )
            result = dialog.get_input()
            
            if result:
                try:
                    pages_per_file = int(result)
                    if 1 <= pages_per_file <= page_count:
                        if self.pdf_handler.split_pdf(output_dir, pages_per_file):
                            file_count = (page_count + pages_per_file - 1) // pages_per_file
                            UIUtils.show_info("Success", f"PDF split into {file_count} files in: {output_dir}", self.main_window.root)
                        else:
                            UIUtils.show_error("Error", "Failed to split PDF.", self.main_window.root)
                    else:
                        UIUtils.show_warning("Invalid Input", f"Pages per file must be between 1 and {page_count}.", self.main_window.root)
                except ValueError:
                    UIUtils.show_warning("Invalid Input", "Please enter a valid number.", self.main_window.root)
    
    def reset(self):
        """Reset the viewer tab"""
        self.pdf_handler.close_pdf()
        self.current_page = 1
        self.search_results = []
        self.current_search_index = 0
        
        # Reset UI
        self.document_text.configure(state="normal")
        self.document_text.delete("0.0", tk.END)
        self.document_text.insert("0.0", "No PDF document loaded.\n\nClick 'Open PDF' to load a document.")
        self.document_text.configure(state="disabled")
        
        self.info_text.delete("0.0", tk.END)
        self.info_text.insert("0.0", "No document loaded")
        
        self.search_listbox.delete(0, tk.END)
        self.search_var.set("")
        self.page_var.set("1")
        self.page_label.configure(text="of 0")
        
        self._update_navigation_state()
        self.status_label.configure(text="No document loaded")