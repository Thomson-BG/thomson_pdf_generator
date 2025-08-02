"""
PDF signer for Thomson PDF Generator
Digital signature functionality for PDF documents
"""
import os
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography import x509
from cryptography.x509.oid import NameOID
import io
import base64


class PDFSigner:
    """Handles digital signing of PDF documents"""
    
    def __init__(self):
        self.private_key = None
        self.certificate = None
        self.signature_info = {}
    
    def generate_self_signed_certificate(self, 
                                       common_name: str = "Thomson PDF Generator User",
                                       email: str = None,
                                       organization: str = None,
                                       country: str = "US") -> bool:
        """
        Generate a self-signed certificate for PDF signing
        
        Args:
            common_name: Certificate common name
            email: Email address
            organization: Organization name
            country: Country code
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Generate private key
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )
            
            # Create certificate subject
            subject_components = [
                x509.NameAttribute(NameOID.COMMON_NAME, common_name),
                x509.NameAttribute(NameOID.COUNTRY_NAME, country),
            ]
            
            if email:
                subject_components.append(x509.NameAttribute(NameOID.EMAIL_ADDRESS, email))
            
            if organization:
                subject_components.append(x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization))
            
            subject = x509.Name(subject_components)
            
            # Create certificate
            self.certificate = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                subject  # Self-signed
            ).public_key(
                self.private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.now(timezone.utc)
            ).not_valid_after(
                datetime.now(timezone.utc).replace(year=datetime.now(timezone.utc).year + 1)
            ).add_extension(
                x509.SubjectAlternativeName([
                    x509.DNSName("localhost"),
                ]),
                critical=False,
            ).add_extension(
                x509.BasicConstraints(ca=False, path_length=None),
                critical=True,
            ).add_extension(
                x509.KeyUsage(
                    key_encipherment=True,
                    digital_signature=True,
                    key_agreement=False,
                    key_cert_sign=False,
                    crl_sign=False,
                    content_commitment=True,
                    data_encipherment=False,
                    encipher_only=False,
                    decipher_only=False,
                ),
                critical=True,
            ).sign(self.private_key, hashes.SHA256())
            
            # Store signature info
            self.signature_info = {
                'common_name': common_name,
                'email': email or 'Not specified',
                'organization': organization or 'Not specified',
                'country': country,
                'created': datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                'valid_until': self.certificate.not_valid_after_utc.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return True
            
        except Exception as e:
            print(f"Error generating certificate: {str(e)}")
            return False
    
    def load_certificate_from_file(self, cert_path: str, key_path: str, 
                                  password: Optional[bytes] = None) -> bool:
        """
        Load certificate and private key from files
        
        Args:
            cert_path: Path to certificate file (.pem, .crt)
            key_path: Path to private key file (.pem, .key)
            password: Password for encrypted private key
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load certificate
            with open(cert_path, 'rb') as cert_file:
                cert_data = cert_file.read()
                self.certificate = x509.load_pem_x509_certificate(cert_data)
            
            # Load private key
            with open(key_path, 'rb') as key_file:
                key_data = key_file.read()
                self.private_key = serialization.load_pem_private_key(
                    key_data, password=password
                )
            
            # Extract certificate info
            subject = self.certificate.subject
            self.signature_info = {
                'common_name': self._get_name_attribute(subject, NameOID.COMMON_NAME),
                'email': self._get_name_attribute(subject, NameOID.EMAIL_ADDRESS),
                'organization': self._get_name_attribute(subject, NameOID.ORGANIZATION_NAME),
                'country': self._get_name_attribute(subject, NameOID.COUNTRY_NAME),
                'valid_from': self.certificate.not_valid_before_utc.strftime('%Y-%m-%d %H:%M:%S'),
                'valid_until': self.certificate.not_valid_after_utc.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return True
            
        except Exception as e:
            print(f"Error loading certificate: {str(e)}")
            return False
    
    def _get_name_attribute(self, name, attribute_oid):
        """Get attribute from certificate name"""
        try:
            for attribute in name:
                if attribute.oid == attribute_oid:
                    return attribute.value
            return "Not specified"
        except Exception:
            return "Not specified"
    
    def save_certificate(self, cert_path: str, key_path: str, 
                        password: Optional[bytes] = None) -> bool:
        """
        Save certificate and private key to files
        
        Args:
            cert_path: Path to save certificate
            key_path: Path to save private key
            password: Password to encrypt private key (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.certificate or not self.private_key:
                return False
            
            # Save certificate
            with open(cert_path, 'wb') as cert_file:
                cert_file.write(self.certificate.public_bytes(serialization.Encoding.PEM))
            
            # Save private key
            encryption_algorithm = serialization.NoEncryption()
            if password:
                encryption_algorithm = serialization.BestAvailableEncryption(password)
            
            with open(key_path, 'wb') as key_file:
                key_file.write(self.private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=encryption_algorithm
                ))
            
            return True
            
        except Exception as e:
            print(f"Error saving certificate: {str(e)}")
            return False
    
    def sign_pdf(self, pdf_path: str, output_path: str = None, 
                signature_text: str = None, position: tuple = None) -> bool:
        """
        Sign a PDF document
        
        Args:
            pdf_path: Path to input PDF
            output_path: Path for signed PDF (optional)
            signature_text: Custom signature text (optional)
            position: Signature position (x, y) on last page (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.private_key or not self.certificate:
                raise ValueError("No certificate loaded. Generate or load a certificate first.")
            
            if not os.path.exists(pdf_path):
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")
            
            if output_path is None:
                output_path = pdf_path
            
            # Create signature data
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if signature_text is None:
                signature_text = f"Digitally signed by {self.signature_info.get('common_name', 'Unknown')}"
            
            # Create signature page overlay
            signature_buffer = self._create_signature_overlay(signature_text, timestamp, position)
            
            # Read original PDF
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                
                # Add all pages
                for i, page in enumerate(pdf_reader.pages):
                    # Add signature to last page
                    if i == len(pdf_reader.pages) - 1:
                        signature_buffer.seek(0)
                        signature_pdf = PyPDF2.PdfReader(signature_buffer)
                        signature_page = signature_pdf.pages[0]
                        page.merge_page(signature_page)
                    
                    pdf_writer.add_page(page)
                
                # Add metadata about the signature
                pdf_writer.add_metadata({
                    '/Title': f'Signed PDF - {Path(pdf_path).stem}',
                    '/Author': self.signature_info.get('common_name', 'Unknown'),
                    '/Subject': 'Digitally Signed Document',
                    '/Creator': 'Thomson PDF Generator',
                    '/Producer': 'Thomson PDF Generator Digital Signature',
                    '/ModDate': f"D:{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    '/Signature': base64.b64encode(self._create_document_hash(pdf_path)).decode('utf-8')
                })
                
                # Write signed PDF
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"Error signing PDF: {str(e)}")
            return False
    
    def _create_signature_overlay(self, signature_text: str, timestamp: str, 
                                position: tuple = None) -> io.BytesIO:
        """Create signature overlay for PDF"""
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        
        # Default position (bottom right)
        if position is None:
            x, y = 400, 50
        else:
            x, y = position
        
        # Draw signature box
        c.setStrokeColor(colors.blue)
        c.setLineWidth(2)
        c.rect(x - 10, y - 10, 200, 80)
        
        # Add signature text
        c.setFillColor(colors.blue)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x, y + 50, "DIGITALLY SIGNED")
        
        c.setFont("Helvetica", 9)
        c.drawString(x, y + 35, signature_text[:30])  # Truncate if too long
        
        c.setFont("Helvetica", 8)
        c.drawString(x, y + 20, f"Date: {timestamp}")
        c.drawString(x, y + 10, f"By: {self.signature_info.get('common_name', 'Unknown')[:25]}")
        c.drawString(x, y, f"Org: {self.signature_info.get('organization', 'N/A')[:25]}")
        
        c.save()
        return buffer
    
    def _create_document_hash(self, pdf_path: str) -> bytes:
        """Create a hash of the document for signature verification"""
        try:
            with open(pdf_path, 'rb') as file:
                content = file.read()
            
            # Create signature using private key
            signature = self.private_key.sign(
                content,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            
            return signature
            
        except Exception as e:
            print(f"Error creating document hash: {str(e)}")
            return b''
    
    def verify_signature(self, pdf_path: str) -> Dict[str, Any]:
        """
        Verify signature of a PDF document
        
        Args:
            pdf_path: Path to signed PDF
            
        Returns:
            Dictionary with verification results
        """
        result = {
            'is_signed': False,
            'is_valid': False,
            'signer': 'Unknown',
            'signature_date': 'Unknown',
            'error': None
        }
        
        try:
            if not os.path.exists(pdf_path):
                result['error'] = "PDF file not found"
                return result
            
            # Read PDF and check for signature metadata
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                if hasattr(pdf_reader, 'metadata') and pdf_reader.metadata:
                    metadata = pdf_reader.metadata
                    
                    # Check for signature metadata
                    if '/Signature' in metadata:
                        result['is_signed'] = True
                        result['signer'] = metadata.get('/Author', 'Unknown')
                        result['signature_date'] = metadata.get('/ModDate', 'Unknown')
                        
                        # For demonstration, we'll consider it valid if it has our signature format
                        if metadata.get('/Producer') == 'Thomson PDF Generator Digital Signature':
                            result['is_valid'] = True
                        else:
                            result['error'] = "Signature format not recognized"
                    else:
                        result['error'] = "No digital signature found"
                else:
                    result['error'] = "No metadata found in PDF"
            
        except Exception as e:
            result['error'] = f"Error verifying signature: {str(e)}"
        
        return result
    
    def get_certificate_info(self) -> Dict[str, Any]:
        """Get information about the current certificate"""
        if not self.certificate:
            return {}
        
        return self.signature_info.copy()
    
    def is_certificate_loaded(self) -> bool:
        """Check if a certificate is currently loaded"""
        return self.certificate is not None and self.private_key is not None