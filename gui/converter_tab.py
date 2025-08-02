"""
Converter tab for Thomson PDF Generator
File conversion interface and functionality
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import os
import threading
from pathlib import Path
from typing import List, Optional

from core.converter import FileConverter
from utils.file_utils import FileUtils
from utils.ui_utils import UIUtils


class ConverterTab:
    """File converter tab implementation"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.file_list = []
        self.converter = None
        self.conversion_in_progress = False
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup converter tab UI"""
        # Main container
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="File to PDF Converter",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # File selection area
        self._setup_file_selection(main_frame)
        
        # File list area
        self._setup_file_list(main_frame)
        
        # Conversion options
        self._setup_conversion_options(main_frame)
        
        # Action buttons
        self._setup_action_buttons(main_frame)
        
        # Progress area
        self._setup_progress_area(main_frame)
    
    def _setup_file_selection(self, parent):
        """Setup file selection area"""
        selection_frame = ctk.CTkFrame(parent)
        selection_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Instructions
        info_label = ctk.CTkLabel(
            selection_frame,
            text="Select files to convert to PDF. Supported formats: TXT, DOC, DOCX, XLSX, Images",
            font=ctk.CTkFont(size=12)
        )
        info_label.pack(pady=10)
        
        # File selection buttons
        button_frame = ctk.CTkFrame(selection_frame)
        button_frame.pack(pady=(0, 10))
        
        self.add_files_btn = ctk.CTkButton(
            button_frame,
            text="Add Files",
            command=self._add_files,
            width=120
        )
        self.add_files_btn.pack(side=tk.LEFT, padx=5)
        
        self.add_folder_btn = ctk.CTkButton(
            button_frame,
            text="Add Folder",
            command=self._add_folder,
            width=120
        )
        self.add_folder_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_list_btn = ctk.CTkButton(
            button_frame,
            text="Clear List",
            command=self._clear_list,
            width=120
        )
        self.clear_list_btn.pack(side=tk.LEFT, padx=5)
        
        # Drag and drop area (placeholder)
        self.drop_frame = ctk.CTkFrame(selection_frame, height=100)
        self.drop_frame.pack(fill=tk.X, padx=10, pady=10)
        self.drop_frame.pack_propagate(False)
        
        drop_label = ctk.CTkLabel(
            self.drop_frame,
            text="Drag and drop files here (or use buttons above)",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        drop_label.pack(expand=True)
    
    def _setup_file_list(self, parent):
        """Setup file list display"""
        list_frame = ctk.CTkFrame(parent)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # List header
        header_label = ctk.CTkLabel(
            list_frame,
            text="Files to Convert:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        header_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # File list with scrollbar
        list_container = ctk.CTkFrame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Create Treeview for file list
        columns = ("filename", "type", "size", "status")
        self.file_tree = ttk.Treeview(list_container, columns=columns, show="headings", height=10)
        
        # Configure columns
        self.file_tree.heading("filename", text="Filename")
        self.file_tree.heading("type", text="Type")
        self.file_tree.heading("size", text="Size")
        self.file_tree.heading("status", text="Status")
        
        self.file_tree.column("filename", width=300)
        self.file_tree.column("type", width=100)
        self.file_tree.column("size", width=100)
        self.file_tree.column("status", width=150)
        
        # Scrollbar for tree
        tree_scroll = ttk.Scrollbar(list_container, orient="vertical", command=self.file_tree.yview)
        self.file_tree.configure(yscrollcommand=tree_scroll.set)
        
        # Pack tree and scrollbar
        self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Context menu for file list
        self.context_menu = tk.Menu(self.file_tree, tearoff=0)
        self.context_menu.add_command(label="Remove", command=self._remove_selected)
        self.context_menu.add_command(label="Open Location", command=self._open_file_location)
        
        self.file_tree.bind("<Button-3>", self._show_context_menu)
    
    def _setup_conversion_options(self, parent):
        """Setup conversion options"""
        options_frame = ctk.CTkFrame(parent)
        options_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Options title
        options_label = ctk.CTkLabel(
            options_frame,
            text="Conversion Options:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        options_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Options container
        options_container = ctk.CTkFrame(options_frame)
        options_container.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Output directory
        output_dir_frame = ctk.CTkFrame(options_container)
        output_dir_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ctk.CTkLabel(output_dir_frame, text="Output Directory:").pack(side=tk.LEFT, padx=(10, 5))
        
        self.output_dir_var = tk.StringVar(value=os.path.expanduser("~/Desktop"))
        self.output_dir_entry = ctk.CTkEntry(
            output_dir_frame,
            textvariable=self.output_dir_var,
            width=400
        )
        self.output_dir_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        self.browse_dir_btn = ctk.CTkButton(
            output_dir_frame,
            text="Browse",
            command=self._browse_output_dir,
            width=80
        )
        self.browse_dir_btn.pack(side=tk.RIGHT, padx=(5, 10))
        
        # Additional options
        additional_frame = ctk.CTkFrame(options_container)
        additional_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.combine_files_var = tk.BooleanVar()
        self.combine_files_cb = ctk.CTkCheckBox(
            additional_frame,
            text="Combine all files into single PDF",
            variable=self.combine_files_var
        )
        self.combine_files_cb.pack(side=tk.LEFT, padx=10)
        
        self.open_after_var = tk.BooleanVar(value=True)
        self.open_after_cb = ctk.CTkCheckBox(
            additional_frame,
            text="Open PDF after conversion",
            variable=self.open_after_var
        )
        self.open_after_cb.pack(side=tk.LEFT, padx=20)
    
    def _setup_action_buttons(self, parent):
        """Setup action buttons"""
        button_frame = ctk.CTkFrame(parent)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Convert button
        self.convert_btn = ctk.CTkButton(
            button_frame,
            text="Convert to PDF",
            command=self._start_conversion,
            font=ctk.CTkFont(size=16, weight="bold"),
            height=40,
            width=200
        )
        self.convert_btn.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Preview button
        self.preview_btn = ctk.CTkButton(
            button_frame,
            text="Preview",
            command=self._preview_conversion,
            width=100
        )
        self.preview_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Settings button
        self.settings_btn = ctk.CTkButton(
            button_frame,
            text="Settings",
            command=self._show_settings,
            width=100
        )
        self.settings_btn.pack(side=tk.LEFT, padx=5, pady=10)
        
        # Batch convert button
        self.batch_btn = ctk.CTkButton(
            button_frame,
            text="Batch Mode",
            command=self.show_batch_dialog,
            width=120
        )
        self.batch_btn.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def _setup_progress_area(self, parent):
        """Setup progress display area"""
        self.progress_frame = ctk.CTkFrame(parent)
        self.progress_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.progress_frame.pack_forget()  # Hidden by default
        
        # Progress label
        self.progress_label = ctk.CTkLabel(
            self.progress_frame,
            text="Converting...",
            font=ctk.CTkFont(size=14)
        )
        self.progress_label.pack(pady=(10, 5))
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Cancel button
        self.cancel_btn = ctk.CTkButton(
            self.progress_frame,
            text="Cancel",
            command=self._cancel_conversion,
            width=100
        )
        self.cancel_btn.pack(pady=(0, 10))
    
    def _add_files(self):
        """Add files to conversion list"""
        files = UIUtils.select_files("Select Files to Convert", parent=self.main_window.root)
        for file_path in files:
            self.add_file(file_path)
    
    def _add_folder(self):
        """Add all supported files from a folder"""
        folder_path = UIUtils.select_directory("Select Folder", parent=self.main_window.root)
        if folder_path:
            added_count = 0
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if FileUtils.is_supported_file(file_path):
                        self.add_file(file_path)
                        added_count += 1
            
            if added_count > 0:
                self.main_window.update_status(f"Added {added_count} files from folder")
            else:
                UIUtils.show_info("No Files", "No supported files found in the selected folder.", self.main_window.root)
    
    def add_file(self, file_path: str) -> bool:
        """Add a single file to the conversion list"""
        if not FileUtils.validate_file_exists(file_path):
            UIUtils.show_error("File Error", f"File not found or not readable: {file_path}", self.main_window.root)
            return False
        
        if not FileUtils.is_supported_file(file_path):
            UIUtils.show_error("File Error", f"Unsupported file type: {file_path}", self.main_window.root)
            return False
        
        # Check if file already in list
        for existing_file in self.file_list:
            if existing_file['path'] == file_path:
                UIUtils.show_warning("Duplicate", f"File already in list: {os.path.basename(file_path)}", self.main_window.root)
                return False
        
        # Add to list
        file_info = {
            'path': file_path,
            'filename': os.path.basename(file_path),
            'type': FileUtils.get_file_type(file_path),
            'size': FileUtils.get_file_size(file_path),
            'status': 'Ready'
        }
        
        self.file_list.append(file_info)
        self._update_file_tree()
        
        self.main_window.update_status(f"Added: {file_info['filename']}")
        return True
    
    def _update_file_tree(self):
        """Update the file list display"""
        # Clear existing items
        for item in self.file_tree.get_children():
            self.file_tree.delete(item)
        
        # Add current files
        for file_info in self.file_list:
            size_str = f"{file_info['size']:,} bytes" if file_info['size'] > 0 else "Unknown"
            self.file_tree.insert("", "end", values=(
                file_info['filename'],
                Path(file_info['path']).suffix.upper(),
                size_str,
                file_info['status']
            ))
    
    def _clear_list(self):
        """Clear all files from list"""
        if self.file_list and UIUtils.ask_yes_no("Clear List", "Remove all files from the conversion list?", self.main_window.root):
            self.file_list.clear()
            self._update_file_tree()
            self.main_window.update_status("File list cleared")
    
    def _browse_output_dir(self):
        """Browse for output directory"""
        directory = UIUtils.select_directory("Select Output Directory", parent=self.main_window.root)
        if directory:
            self.output_dir_var.set(directory)
    
    def _show_context_menu(self, event):
        """Show context menu for file list"""
        if self.file_tree.selection():
            self.context_menu.post(event.x_root, event.y_root)
    
    def _remove_selected(self):
        """Remove selected file from list"""
        selection = self.file_tree.selection()
        if selection:
            item = selection[0]
            index = self.file_tree.index(item)
            if 0 <= index < len(self.file_list):
                removed_file = self.file_list.pop(index)
                self._update_file_tree()
                self.main_window.update_status(f"Removed: {removed_file['filename']}")
    
    def _open_file_location(self):
        """Open file location in system explorer"""
        selection = self.file_tree.selection()
        if selection:
            item = selection[0]
            index = self.file_tree.index(item)
            if 0 <= index < len(self.file_list):
                file_path = self.file_list[index]['path']
                try:
                    import subprocess
                    if os.name == 'nt':  # Windows
                        subprocess.run(['explorer', '/select,', file_path])
                    elif os.name == 'posix':  # macOS and Linux
                        subprocess.run(['xdg-open', os.path.dirname(file_path)])
                except Exception as e:
                    UIUtils.show_error("Error", f"Could not open file location: {str(e)}", self.main_window.root)
    
    def _start_conversion(self):
        """Start the conversion process"""
        if not self.file_list:
            UIUtils.show_warning("No Files", "Please add files to convert first.", self.main_window.root)
            return
        
        output_dir = self.output_dir_var.get()
        if not output_dir or not os.path.exists(output_dir):
            UIUtils.show_error("Invalid Directory", "Please select a valid output directory.", self.main_window.root)
            return
        
        if self.conversion_in_progress:
            UIUtils.show_warning("Conversion in Progress", "A conversion is already in progress.", self.main_window.root)
            return
        
        # Start conversion in separate thread
        self.conversion_in_progress = True
        self._show_progress()
        
        conversion_thread = threading.Thread(target=self._run_conversion, daemon=True)
        conversion_thread.start()
    
    def _run_conversion(self):
        """Run the actual conversion process"""
        try:
            self.converter = FileConverter(progress_callback=self._update_conversion_progress)
            output_dir = self.output_dir_var.get()
            combine_files = self.combine_files_var.get()
            
            if combine_files:
                # Combine all files into single PDF
                self._convert_combined()
            else:
                # Convert each file separately
                self._convert_individual()
            
            # Conversion completed
            self.main_window.root.after(0, self._conversion_completed)
            
        except Exception as e:
            self.main_window.root.after(0, lambda: self._conversion_error(str(e)))
    
    def _convert_individual(self):
        """Convert each file individually"""
        output_dir = self.output_dir_var.get()
        total_files = len(self.file_list)
        
        for i, file_info in enumerate(self.file_list):
            if not self.conversion_in_progress:  # Check for cancellation
                break
            
            try:
                # Update status
                self.main_window.root.after(0, lambda f=file_info: self._update_file_status(f, "Converting..."))
                
                # Generate output path
                output_filename = FileUtils.ensure_pdf_extension(
                    FileUtils.get_safe_filename(Path(file_info['path']).stem)
                )
                output_path = os.path.join(output_dir, output_filename)
                
                # Convert file
                success = self.converter.convert_to_pdf(file_info['path'], output_path)
                
                # Update status
                status = "Completed" if success else "Failed"
                self.main_window.root.after(0, lambda f=file_info, s=status: self._update_file_status(f, s))
                
                # Update overall progress
                progress = (i + 1) / total_files
                self.main_window.root.after(0, lambda p=progress: self.main_window.set_progress(p))
                
            except Exception as e:
                print(f"Error converting {file_info['path']}: {str(e)}")
                self.main_window.root.after(0, lambda f=file_info: self._update_file_status(f, "Error"))
    
    def _convert_combined(self):
        """Convert all files into a single combined PDF"""
        # This is a simplified implementation
        # In a real application, you might want more sophisticated merging
        UIUtils.show_info("Combined Conversion", "Combined PDF conversion is not yet implemented in this demo.", self.main_window.root)
    
    def _update_file_status(self, file_info, status):
        """Update status of a specific file"""
        file_info['status'] = status
        self._update_file_tree()
    
    def _update_conversion_progress(self, message: str, percentage: int):
        """Update conversion progress"""
        self.main_window.root.after(0, lambda: self.progress_label.configure(text=message))
        if percentage >= 0:
            self.main_window.root.after(0, lambda: self.progress_bar.set(percentage / 100.0))
    
    def _show_progress(self):
        """Show progress area"""
        self.progress_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        self.convert_btn.configure(state="disabled")
        self.progress_bar.set(0)
    
    def _hide_progress(self):
        """Hide progress area"""
        self.progress_frame.pack_forget()
        self.convert_btn.configure(state="normal")
    
    def _conversion_completed(self):
        """Handle conversion completion"""
        self.conversion_in_progress = False
        self._hide_progress()
        self.main_window.update_status("Conversion completed!")
        
        # Show completion message
        completed_files = sum(1 for f in self.file_list if f['status'] == 'Completed')
        total_files = len(self.file_list)
        
        message = f"Conversion completed!\n{completed_files} of {total_files} files converted successfully."
        UIUtils.show_info("Conversion Complete", message, self.main_window.root)
        
        # Open output directory if requested
        if self.open_after_var.get() and completed_files > 0:
            try:
                import subprocess
                output_dir = self.output_dir_var.get()
                if os.name == 'nt':  # Windows
                    subprocess.run(['explorer', output_dir])
                elif os.name == 'posix':  # macOS and Linux
                    subprocess.run(['xdg-open', output_dir])
            except Exception:
                pass  # Ignore errors when opening directory
    
    def _conversion_error(self, error_message):
        """Handle conversion error"""
        self.conversion_in_progress = False
        self._hide_progress()
        self.main_window.update_status("Conversion failed")
        UIUtils.show_error("Conversion Error", f"Conversion failed: {error_message}", self.main_window.root)
    
    def _cancel_conversion(self):
        """Cancel ongoing conversion"""
        if UIUtils.ask_yes_no("Cancel Conversion", "Are you sure you want to cancel the conversion?", self.main_window.root):
            self.conversion_in_progress = False
            self._hide_progress()
            self.main_window.update_status("Conversion cancelled")
    
    def _preview_conversion(self):
        """Preview conversion settings"""
        if not self.file_list:
            UIUtils.show_warning("No Files", "Please add files to preview first.", self.main_window.root)
            return
        
        output_dir = self.output_dir_var.get()
        combine_files = self.combine_files_var.get()
        
        preview_text = f"""
Conversion Preview:

Files to convert: {len(self.file_list)}
Output directory: {output_dir}
Combine into single PDF: {'Yes' if combine_files else 'No'}

Files:
"""
        
        for file_info in self.file_list[:10]:  # Show first 10 files
            preview_text += f"• {file_info['filename']} ({Path(file_info['path']).suffix.upper()})\n"
        
        if len(self.file_list) > 10:
            preview_text += f"... and {len(self.file_list) - 10} more files\n"
        
        UIUtils.show_info("Conversion Preview", preview_text, self.main_window.root)
    
    def _show_settings(self):
        """Show conversion settings dialog"""
        UIUtils.show_info("Settings", "Advanced conversion settings coming soon!", self.main_window.root)
    
    def show_batch_dialog(self):
        """Show batch conversion dialog"""
        UIUtils.show_info("Batch Mode", "Batch conversion dialog coming soon!", self.main_window.root)
    
    def reset(self):
        """Reset the converter tab"""
        if not self.conversion_in_progress:
            self.file_list.clear()
            self._update_file_tree()
            self._hide_progress()
            self.main_window.update_status("Converter reset")