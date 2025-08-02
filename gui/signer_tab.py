"""
Signer tab for Thomson PDF Generator
Digital signature interface and certificate management
"""
import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import os
from pathlib import Path
from typing import Optional, Dict, Any

from core.signer import PDFSigner
from utils.ui_utils import UIUtils


class SignerTab:
    """Digital signature tab implementation"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.pdf_signer = PDFSigner()
        self.current_pdf_path = None
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup signer tab UI"""
        # Main container
        main_frame = ctk.CTkFrame(self.parent)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="PDF Digital Signature",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(10, 20))
        
        # Main content area
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel (certificate management)
        self._setup_left_panel(content_frame)
        
        # Right panel (signing operations)
        self._setup_right_panel(content_frame)
        
        # Status bar
        self._setup_status_bar(main_frame)
    
    def _setup_left_panel(self, parent):
        """Setup left panel with certificate management"""
        left_frame = ctk.CTkFrame(parent, width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))
        left_frame.pack_propagate(False)
        
        # Certificate section
        cert_label = ctk.CTkLabel(
            left_frame,
            text="Certificate Management",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        cert_label.pack(pady=(10, 15), padx=10)
        
        # Certificate status
        self.cert_status_frame = ctk.CTkFrame(left_frame)
        self.cert_status_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.cert_status_label = ctk.CTkLabel(
            self.cert_status_frame,
            text="No certificate loaded",
            font=ctk.CTkFont(size=14),
            text_color="red"
        )
        self.cert_status_label.pack(pady=10)
        
        # Certificate actions
        cert_actions_frame = ctk.CTkFrame(left_frame)
        cert_actions_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.generate_cert_btn = ctk.CTkButton(
            cert_actions_frame,
            text="Generate New Certificate",
            command=self.show_certificate_dialog,
            height=35
        )
        self.generate_cert_btn.pack(fill=tk.X, padx=10, pady=5)
        
        self.load_cert_btn = ctk.CTkButton(
            cert_actions_frame,
            text="Load Existing Certificate",
            command=self._load_certificate,
            height=35
        )
        self.load_cert_btn.pack(fill=tk.X, padx=10, pady=5)
        
        self.save_cert_btn = ctk.CTkButton(
            cert_actions_frame,
            text="Save Certificate",
            command=self._save_certificate,
            height=35,
            state="disabled"
        )
        self.save_cert_btn.pack(fill=tk.X, padx=10, pady=5)
        
        # Certificate information
        cert_info_label = ctk.CTkLabel(
            left_frame,
            text="Certificate Information",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        cert_info_label.pack(pady=(15, 5), padx=10)
        
        self.cert_info_frame = ctk.CTkScrollableFrame(left_frame, height=200)
        self.cert_info_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.cert_info_text = ctk.CTkTextbox(self.cert_info_frame, height=180)
        self.cert_info_text.pack(fill=tk.BOTH, expand=True)
        self.cert_info_text.insert("0.0", "No certificate information available")
        self.cert_info_text.configure(state="disabled")
        
        # Quick actions
        quick_actions_label = ctk.CTkLabel(
            left_frame,
            text="Quick Actions",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        quick_actions_label.pack(pady=(15, 5), padx=10)
        
        quick_actions_frame = ctk.CTkFrame(left_frame)
        quick_actions_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.test_cert_btn = ctk.CTkButton(
            quick_actions_frame,
            text="Test Certificate",
            command=self._test_certificate,
            state="disabled"
        )
        self.test_cert_btn.pack(fill=tk.X, padx=10, pady=5)
        
        self.view_cert_btn = ctk.CTkButton(
            quick_actions_frame,
            text="View Certificate Details",
            command=self._view_certificate_details,
            state="disabled"
        )
        self.view_cert_btn.pack(fill=tk.X, padx=10, pady=5)
    
    def _setup_right_panel(self, parent):
        """Setup right panel with signing operations"""
        right_frame = ctk.CTkFrame(parent)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # Signing section
        sign_label = ctk.CTkLabel(
            right_frame,
            text="Document Signing",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        sign_label.pack(pady=(10, 15), padx=10)
        
        # PDF file selection
        file_frame = ctk.CTkFrame(right_frame)
        file_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        file_label = ctk.CTkLabel(file_frame, text="PDF Document:", font=ctk.CTkFont(weight="bold"))
        file_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        file_input_frame = ctk.CTkFrame(file_frame)
        file_input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.file_path_var = tk.StringVar()
        self.file_path_entry = ctk.CTkEntry(
            file_input_frame,
            textvariable=self.file_path_var,
            placeholder_text="Select PDF file to sign...",
            state="readonly"
        )
        self.file_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.browse_file_btn = ctk.CTkButton(
            file_input_frame,
            text="Browse",
            command=self._browse_pdf_file,
            width=80
        )
        self.browse_file_btn.pack(side=tk.RIGHT)
        
        # Signature options
        options_frame = ctk.CTkFrame(right_frame)
        options_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        options_label = ctk.CTkLabel(options_frame, text="Signature Options:", font=ctk.CTkFont(weight="bold"))
        options_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Custom signature text
        text_frame = ctk.CTkFrame(options_frame)
        text_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ctk.CTkLabel(text_frame, text="Signature Text:").pack(anchor="w", padx=5, pady=2)
        self.signature_text_var = tk.StringVar()
        self.signature_text_entry = ctk.CTkEntry(
            text_frame,
            textvariable=self.signature_text_var,
            placeholder_text="Custom signature text (optional)..."
        )
        self.signature_text_entry.pack(fill=tk.X, padx=5, pady=2)
        
        # Signature position
        position_frame = ctk.CTkFrame(options_frame)
        position_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ctk.CTkLabel(position_frame, text="Position:").pack(anchor="w", padx=5, pady=2)
        
        pos_input_frame = ctk.CTkFrame(position_frame)
        pos_input_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ctk.CTkLabel(pos_input_frame, text="X:").pack(side=tk.LEFT, padx=2)
        self.pos_x_var = tk.StringVar(value="400")
        self.pos_x_entry = ctk.CTkEntry(pos_input_frame, textvariable=self.pos_x_var, width=60)
        self.pos_x_entry.pack(side=tk.LEFT, padx=2)
        
        ctk.CTkLabel(pos_input_frame, text="Y:").pack(side=tk.LEFT, padx=(10, 2))
        self.pos_y_var = tk.StringVar(value="50")
        self.pos_y_entry = ctk.CTkEntry(pos_input_frame, textvariable=self.pos_y_var, width=60)
        self.pos_y_entry.pack(side=tk.LEFT, padx=2)
        
        # Use default position checkbox
        self.use_default_pos_var = tk.BooleanVar(value=True)
        self.use_default_pos_cb = ctk.CTkCheckBox(
            position_frame,
            text="Use default position (bottom right)",
            variable=self.use_default_pos_var,
            command=self._toggle_position_controls
        )
        self.use_default_pos_cb.pack(anchor="w", padx=5, pady=2)
        
        # Initially disable position controls
        self._toggle_position_controls()
        
        # Action buttons
        action_frame = ctk.CTkFrame(right_frame)
        action_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.sign_btn = ctk.CTkButton(
            action_frame,
            text="Sign PDF",
            command=self._sign_pdf,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold"),
            state="disabled"
        )
        self.sign_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Verification section
        verify_label = ctk.CTkLabel(
            right_frame,
            text="Signature Verification",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        verify_label.pack(pady=(20, 10), padx=10)
        
        verify_frame = ctk.CTkFrame(right_frame)
        verify_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.verify_btn = ctk.CTkButton(
            verify_frame,
            text="Verify PDF Signature",
            command=self._verify_signature,
            height=35
        )
        self.verify_btn.pack(fill=tk.X, padx=10, pady=10)
        
        # Verification results
        self.verify_results_frame = ctk.CTkScrollableFrame(right_frame, height=150)
        self.verify_results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        self.verify_results_text = ctk.CTkTextbox(self.verify_results_frame, height=130)
        self.verify_results_text.pack(fill=tk.BOTH, expand=True)
        self.verify_results_text.insert("0.0", "No verification results")
        self.verify_results_text.configure(state="disabled")
    
    def _setup_status_bar(self, parent):
        """Setup status bar"""
        self.status_frame = ctk.CTkFrame(parent, height=30)
        self.status_frame.pack(fill=tk.X, padx=10, pady=(10, 0))
        self.status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="Ready for certificate operations",
            anchor="w"
        )
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
    
    def show_certificate_dialog(self):
        """Show certificate generation dialog"""
        dialog = CertificateDialog(self.main_window.root, self)
        dialog.show()
    
    def _load_certificate(self):
        """Load existing certificate from files"""
        cert_path = UIUtils.select_file(
            "Select Certificate File",
            [("Certificate Files", "*.pem;*.crt"), ("All Files", "*.*")],
            self.main_window.root
        )
        
        if not cert_path:
            return
        
        key_path = UIUtils.select_file(
            "Select Private Key File",
            [("Key Files", "*.pem;*.key"), ("All Files", "*.*")],
            self.main_window.root
        )
        
        if not key_path:
            return
        
        # Ask for password if needed
        password_dialog = ctk.CTkInputDialog(
            text="Enter private key password (leave empty if no password):",
            title="Private Key Password"
        )
        password = password_dialog.get_input()
        password_bytes = password.encode() if password else None
        
        try:
            if self.pdf_signer.load_certificate_from_file(cert_path, key_path, password_bytes):
                self._update_certificate_status()
                self.main_window.update_status("Certificate loaded successfully")
                UIUtils.show_info("Success", "Certificate loaded successfully!", self.main_window.root)
            else:
                UIUtils.show_error("Error", "Failed to load certificate. Please check the files and password.", self.main_window.root)
        
        except Exception as e:
            UIUtils.show_error("Error", f"Error loading certificate: {str(e)}", self.main_window.root)
    
    def _save_certificate(self):
        """Save current certificate to files"""
        if not self.pdf_signer.is_certificate_loaded():
            UIUtils.show_warning("No Certificate", "No certificate loaded to save.", self.main_window.root)
            return
        
        cert_path = UIUtils.save_file(
            "Save Certificate File",
            ".pem",
            [("Certificate Files", "*.pem"), ("All Files", "*.*")],
            self.main_window.root
        )
        
        if not cert_path:
            return
        
        key_path = UIUtils.save_file(
            "Save Private Key File",
            ".pem",
            [("Key Files", "*.pem"), ("All Files", "*.*")],
            self.main_window.root
        )
        
        if not key_path:
            return
        
        # Ask for password protection
        if UIUtils.ask_yes_no("Password Protection", "Do you want to password-protect the private key?", self.main_window.root):
            password_dialog = ctk.CTkInputDialog(
                text="Enter password for private key:",
                title="Private Key Password"
            )
            password = password_dialog.get_input()
            password_bytes = password.encode() if password else None
        else:
            password_bytes = None
        
        try:
            if self.pdf_signer.save_certificate(cert_path, key_path, password_bytes):
                self.main_window.update_status("Certificate saved successfully")
                UIUtils.show_info("Success", f"Certificate saved to:\n{cert_path}\n{key_path}", self.main_window.root)
            else:
                UIUtils.show_error("Error", "Failed to save certificate.", self.main_window.root)
        
        except Exception as e:
            UIUtils.show_error("Error", f"Error saving certificate: {str(e)}", self.main_window.root)
    
    def _browse_pdf_file(self):
        """Browse for PDF file to sign"""
        file_path = UIUtils.select_file(
            "Select PDF File to Sign",
            [("PDF Files", "*.pdf"), ("All Files", "*.*")],
            self.main_window.root
        )
        
        if file_path:
            self.file_path_var.set(file_path)
            self.current_pdf_path = file_path
            self._update_sign_button_state()
    
    def _toggle_position_controls(self):
        """Toggle position control states"""
        use_default = self.use_default_pos_var.get()
        state = "disabled" if use_default else "normal"
        self.pos_x_entry.configure(state=state)
        self.pos_y_entry.configure(state=state)
    
    def _sign_pdf(self):
        """Sign the selected PDF"""
        if not self.pdf_signer.is_certificate_loaded():
            UIUtils.show_warning("No Certificate", "Please generate or load a certificate first.", self.main_window.root)
            return
        
        if not self.current_pdf_path or not os.path.exists(self.current_pdf_path):
            UIUtils.show_warning("No File", "Please select a valid PDF file to sign.", self.main_window.root)
            return
        
        # Get signature options
        signature_text = self.signature_text_var.get().strip() or None
        
        position = None
        if not self.use_default_pos_var.get():
            try:
                x = float(self.pos_x_var.get())
                y = float(self.pos_y_var.get())
                position = (x, y)
            except ValueError:
                UIUtils.show_warning("Invalid Position", "Please enter valid position coordinates.", self.main_window.root)
                return
        
        # Get output path
        output_path = UIUtils.save_file(
            "Save Signed PDF",
            ".pdf",
            [("PDF Files", "*.pdf"), ("All Files", "*.*")],
            self.main_window.root
        )
        
        if not output_path:
            return
        
        try:
            # Show progress
            self.main_window.update_status("Signing PDF...", show_progress=True)
            self.sign_btn.configure(state="disabled")
            
            # Sign the PDF
            if self.pdf_signer.sign_pdf(self.current_pdf_path, output_path, signature_text, position):
                self.main_window.update_status("PDF signed successfully")
                UIUtils.show_info("Success", f"PDF signed successfully!\nSaved as: {os.path.basename(output_path)}", self.main_window.root)
                
                # Ask if user wants to verify the signature
                if UIUtils.ask_yes_no("Verify Signature", "Would you like to verify the signature now?", self.main_window.root):
                    self.file_path_var.set(output_path)
                    self.current_pdf_path = output_path
                    self._verify_signature()
            else:
                UIUtils.show_error("Error", "Failed to sign PDF.", self.main_window.root)
        
        except Exception as e:
            UIUtils.show_error("Error", f"Error signing PDF: {str(e)}", self.main_window.root)
        
        finally:
            self.main_window.update_status("Ready")
            self.sign_btn.configure(state="normal")
    
    def _verify_signature(self):
        """Verify PDF signature"""
        pdf_path = self.file_path_var.get()
        
        if not pdf_path:
            pdf_path = UIUtils.select_file(
                "Select PDF to Verify",
                [("PDF Files", "*.pdf"), ("All Files", "*.*")],
                self.main_window.root
            )
        
        if not pdf_path or not os.path.exists(pdf_path):
            UIUtils.show_warning("No File", "Please select a valid PDF file to verify.", self.main_window.root)
            return
        
        try:
            self.main_window.update_status("Verifying signature...")
            
            result = self.pdf_signer.verify_signature(pdf_path)
            
            # Display results
            results_text = f"""Signature Verification Results for:
{os.path.basename(pdf_path)}

Digitally Signed: {'Yes' if result['is_signed'] else 'No'}
Signature Valid: {'Yes' if result['is_valid'] else 'No'}
Signer: {result['signer']}
Signature Date: {result['signature_date']}"""
            
            if result['error']:
                results_text += f"\nError: {result['error']}"
            
            self.verify_results_text.configure(state="normal")
            self.verify_results_text.delete("0.0", tk.END)
            self.verify_results_text.insert("0.0", results_text)
            self.verify_results_text.configure(state="disabled")
            
            self.main_window.update_status(f"Verification complete - {'Valid' if result['is_valid'] else 'Invalid'}")
            
            # Show popup with results
            status = "Valid" if result['is_valid'] else "Invalid"
            color = "green" if result['is_valid'] else "red"
            UIUtils.show_info("Verification Results", f"Signature Status: {status}\n\n{results_text}", self.main_window.root)
        
        except Exception as e:
            UIUtils.show_error("Error", f"Error verifying signature: {str(e)}", self.main_window.root)
    
    def _test_certificate(self):
        """Test current certificate"""
        if not self.pdf_signer.is_certificate_loaded():
            UIUtils.show_warning("No Certificate", "No certificate loaded to test.", self.main_window.root)
            return
        
        cert_info = self.pdf_signer.get_certificate_info()
        
        test_results = f"""Certificate Test Results:

Certificate loaded: Yes
Common Name: {cert_info.get('common_name', 'Unknown')}
Email: {cert_info.get('email', 'Not specified')}
Organization: {cert_info.get('organization', 'Not specified')}
Country: {cert_info.get('country', 'Unknown')}
Valid Until: {cert_info.get('valid_until', 'Unknown')}

Status: Certificate is ready for signing operations."""
        
        UIUtils.show_info("Certificate Test", test_results, self.main_window.root)
    
    def _view_certificate_details(self):
        """View detailed certificate information"""
        if not self.pdf_signer.is_certificate_loaded():
            UIUtils.show_warning("No Certificate", "No certificate loaded.", self.main_window.root)
            return
        
        cert_info = self.pdf_signer.get_certificate_info()
        
        details_window = ctk.CTkToplevel(self.main_window.root)
        details_window.title("Certificate Details")
        details_window.geometry("500x400")
        details_window.transient(self.main_window.root)
        details_window.grab_set()
        
        UIUtils.center_window(details_window, 500, 400)
        
        details_text = ctk.CTkTextbox(details_window)
        details_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        details_content = f"""Certificate Details:

Common Name: {cert_info.get('common_name', 'Unknown')}
Email Address: {cert_info.get('email', 'Not specified')}
Organization: {cert_info.get('organization', 'Not specified')}
Country: {cert_info.get('country', 'Unknown')}

Validity:
Created: {cert_info.get('created', 'Unknown')}
Valid Until: {cert_info.get('valid_until', 'Unknown')}

Usage:
This certificate can be used to digitally sign PDF documents.
The certificate is self-signed and suitable for personal use.

Security Note:
Keep your private key secure and do not share it with others.
"""
        
        details_text.insert("0.0", details_content)
        details_text.configure(state="disabled")
    
    def _update_certificate_status(self):
        """Update certificate status display"""
        if self.pdf_signer.is_certificate_loaded():
            cert_info = self.pdf_signer.get_certificate_info()
            
            # Update status label
            self.cert_status_label.configure(
                text=f"Certificate loaded: {cert_info.get('common_name', 'Unknown')}",
                text_color="green"
            )
            
            # Update info display
            info_text = f"""Common Name: {cert_info.get('common_name', 'Unknown')}
Email: {cert_info.get('email', 'Not specified')}
Organization: {cert_info.get('organization', 'Not specified')}
Country: {cert_info.get('country', 'Unknown')}
Valid Until: {cert_info.get('valid_until', 'Unknown')}
Status: Ready for signing"""
            
            self.cert_info_text.configure(state="normal")
            self.cert_info_text.delete("0.0", tk.END)
            self.cert_info_text.insert("0.0", info_text)
            self.cert_info_text.configure(state="disabled")
            
            # Enable buttons
            self.save_cert_btn.configure(state="normal")
            self.test_cert_btn.configure(state="normal")
            self.view_cert_btn.configure(state="normal")
            
            self._update_sign_button_state()
        else:
            # No certificate loaded
            self.cert_status_label.configure(
                text="No certificate loaded",
                text_color="red"
            )
            
            self.cert_info_text.configure(state="normal")
            self.cert_info_text.delete("0.0", tk.END)
            self.cert_info_text.insert("0.0", "No certificate information available")
            self.cert_info_text.configure(state="disabled")
            
            # Disable buttons
            self.save_cert_btn.configure(state="disabled")
            self.test_cert_btn.configure(state="disabled")
            self.view_cert_btn.configure(state="disabled")
            self.sign_btn.configure(state="disabled")
    
    def _update_sign_button_state(self):
        """Update sign button state"""
        has_cert = self.pdf_signer.is_certificate_loaded()
        has_file = self.current_pdf_path and os.path.exists(self.current_pdf_path)
        
        state = "normal" if has_cert and has_file else "disabled"
        self.sign_btn.configure(state=state)
    
    def generate_certificate(self, common_name: str, email: str = None, 
                           organization: str = None, country: str = "US"):
        """Generate a new certificate with given information"""
        try:
            if self.pdf_signer.generate_self_signed_certificate(common_name, email, organization, country):
                self._update_certificate_status()
                self.main_window.update_status("New certificate generated")
                return True
            return False
        except Exception as e:
            UIUtils.show_error("Error", f"Error generating certificate: {str(e)}", self.main_window.root)
            return False
    
    def reset(self):
        """Reset the signer tab"""
        self.pdf_signer = PDFSigner()
        self.current_pdf_path = None
        self.file_path_var.set("")
        self.signature_text_var.set("")
        
        self._update_certificate_status()
        
        self.verify_results_text.configure(state="normal")
        self.verify_results_text.delete("0.0", tk.END)
        self.verify_results_text.insert("0.0", "No verification results")
        self.verify_results_text.configure(state="disabled")
        
        self.status_label.configure(text="Ready for certificate operations")


class CertificateDialog:
    """Dialog for generating new certificates"""
    
    def __init__(self, parent, signer_tab):
        self.parent = parent
        self.signer_tab = signer_tab
        self.dialog = None
    
    def show(self):
        """Show the certificate generation dialog"""
        self.dialog = ctk.CTkToplevel(self.parent)
        self.dialog.title("Generate Certificate")
        self.dialog.geometry("400x300")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        UIUtils.center_window(self.dialog, 400, 300)
        
        # Title
        title_label = ctk.CTkLabel(
            self.dialog,
            text="Generate New Certificate",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=20)
        
        # Form frame
        form_frame = ctk.CTkFrame(self.dialog)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Common Name (required)
        ctk.CTkLabel(form_frame, text="Full Name (Common Name)*:").pack(anchor="w", padx=10, pady=(10, 2))
        self.common_name_var = tk.StringVar()
        self.common_name_entry = ctk.CTkEntry(form_frame, textvariable=self.common_name_var)
        self.common_name_entry.pack(fill=tk.X, padx=10, pady=2)
        
        # Email (optional)
        ctk.CTkLabel(form_frame, text="Email Address:").pack(anchor="w", padx=10, pady=(10, 2))
        self.email_var = tk.StringVar()
        self.email_entry = ctk.CTkEntry(form_frame, textvariable=self.email_var)
        self.email_entry.pack(fill=tk.X, padx=10, pady=2)
        
        # Organization (optional)
        ctk.CTkLabel(form_frame, text="Organization:").pack(anchor="w", padx=10, pady=(10, 2))
        self.org_var = tk.StringVar()
        self.org_entry = ctk.CTkEntry(form_frame, textvariable=self.org_var)
        self.org_entry.pack(fill=tk.X, padx=10, pady=2)
        
        # Country
        ctk.CTkLabel(form_frame, text="Country Code:").pack(anchor="w", padx=10, pady=(10, 2))
        self.country_var = tk.StringVar(value="US")
        self.country_entry = ctk.CTkEntry(form_frame, textvariable=self.country_var)
        self.country_entry.pack(fill=tk.X, padx=10, pady=2)
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame)
        button_frame.pack(fill=tk.X, padx=10, pady=20)
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self._cancel,
            width=80
        )
        cancel_btn.pack(side=tk.RIGHT, padx=5)
        
        generate_btn = ctk.CTkButton(
            button_frame,
            text="Generate",
            command=self._generate,
            width=80
        )
        generate_btn.pack(side=tk.RIGHT, padx=5)
        
        # Focus on first entry
        self.common_name_entry.focus()
    
    def _generate(self):
        """Generate the certificate"""
        common_name = self.common_name_var.get().strip()
        
        if not common_name:
            UIUtils.show_warning("Missing Information", "Please enter your full name (Common Name).", self.dialog)
            return
        
        email = self.email_var.get().strip() or None
        organization = self.org_var.get().strip() or None
        country = self.country_var.get().strip() or "US"
        
        if self.signer_tab.generate_certificate(common_name, email, organization, country):
            UIUtils.show_info("Success", "Certificate generated successfully!", self.dialog)
            self._close()
        else:
            UIUtils.show_error("Error", "Failed to generate certificate.", self.dialog)
    
    def _cancel(self):
        """Cancel dialog"""
        self._close()
    
    def _close(self):
        """Close dialog"""
        if self.dialog:
            self.dialog.destroy()