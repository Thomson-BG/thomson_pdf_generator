"""
PDF handler for Thomson PDF Generator
Handles PDF operations like opening, viewing, and basic manipulation
"""
import os
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
import PyPDF2
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from PIL import Image as PILImage
import io


class PDFHandler:
    """Handles PDF file operations"""
    
    def __init__(self):
        self.current_pdf = None
        self.current_pages = []
        self.current_path = None
        self.file_stream = None
    
    def open_pdf(self, file_path: str) -> bool:
        """
        Open a PDF file for viewing/editing
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"PDF file not found: {file_path}")
            
            self.close_pdf()  # Close any previously opened PDF

            self.file_stream = open(file_path, 'rb')
            self.current_pdf = PyPDF2.PdfReader(self.file_stream)
            self.current_path = file_path

            return True

        except Exception as e:
            print(f"Error opening PDF: {str(e)}")
            self.close_pdf()
            return False
    
    def _extract_page_text(self, page) -> str:
        """Extract text from a PDF page"""
        try:
            return page.extract_text()
        except Exception:
            return "Error extracting text"
    
    def get_page_count(self) -> int:
        """Get number of pages in current PDF"""
        return len(self.current_pdf.pages) if self.current_pdf else 0
    
    def get_page_text(self, page_number: int) -> str:
        """Get text content of a specific page"""
        if not self.current_pdf or page_number < 1 or page_number > len(self.current_pdf.pages):
            return ""
        page = self.current_pdf.pages[page_number - 1]
        return page.extract_text()
    
    def get_page_info(self, page_number: int) -> Optional[Dict[str, Any]]:
        """Get information about a specific page"""
        if not self.current_pages or page_number < 1 or page_number > len(self.current_pages):
            return None
        return self.current_pages[page_number - 1].copy()
    
    def get_pdf_info(self) -> Dict[str, Any]:
        """Get general information about the current PDF"""
        if not self.current_pdf:
            return {}
        
        info = {}
        try:
            # Basic info
            info['pages'] = len(self.current_pages)
            info['path'] = self.current_path
            info['filename'] = Path(self.current_path).name if self.current_path else "Unknown"
            info['file_size'] = os.path.getsize(self.current_path) if self.current_path else 0
            
            # PDF metadata
            if hasattr(self.current_pdf, 'metadata') and self.current_pdf.metadata:
                metadata = self.current_pdf.metadata
                info['title'] = metadata.get('/Title', 'Unknown')
                info['author'] = metadata.get('/Author', 'Unknown')
                info['subject'] = metadata.get('/Subject', 'Unknown')
                info['creator'] = metadata.get('/Creator', 'Unknown')
                info['producer'] = metadata.get('/Producer', 'Unknown')
                info['creation_date'] = metadata.get('/CreationDate', 'Unknown')
                info['modification_date'] = metadata.get('/ModDate', 'Unknown')
            else:
                info.update({
                    'title': 'Unknown',
                    'author': 'Unknown',
                    'subject': 'Unknown',
                    'creator': 'Unknown',
                    'producer': 'Unknown',
                    'creation_date': 'Unknown',
                    'modification_date': 'Unknown'
                })
                
        except Exception as e:
            print(f"Error getting PDF info: {str(e)}")
        
        return info
    
    def search_text(self, search_term: str, case_sensitive: bool = False) -> List[Dict[str, Any]]:
        """
        Search for text in the current PDF
        
        Args:
            search_term: Text to search for
            case_sensitive: Whether search should be case sensitive
            
        Returns:
            List of search results with page numbers and context
        """
        results = []
        if not self.current_pages or not search_term:
            return results
        
        search_text = search_term if case_sensitive else search_term.lower()
        
        for page_info in self.current_pages:
            page_text = page_info['text'] if case_sensitive else page_info['text'].lower()
            
            if search_text in page_text:
                # Find all occurrences in this page
                start = 0
                while True:
                    pos = page_text.find(search_text, start)
                    if pos == -1:
                        break
                    
                    # Get context around the match
                    context_start = max(0, pos - 50)
                    context_end = min(len(page_text), pos + len(search_text) + 50)
                    context = page_text[context_start:context_end]
                    
                    results.append({
                        'page': page_info['number'],
                        'position': pos,
                        'context': context,
                        'match': search_text
                    })
                    
                    start = pos + 1
        
        return results
    
    def extract_pages(self, page_numbers: List[int], output_path: str) -> bool:
        """
        Extract specific pages to a new PDF
        
        Args:
            page_numbers: List of page numbers to extract (1-based)
            output_path: Path for output PDF
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.current_pdf or not page_numbers:
                return False
            
            # Create new PDF writer
            pdf_writer = PyPDF2.PdfWriter()
            
            # Add selected pages
            for page_num in page_numbers:
                if 1 <= page_num <= len(self.current_pdf.pages):
                    page = self.current_pdf.pages[page_num - 1]
                    pdf_writer.add_page(page)
            
            # Write to output file
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"Error extracting pages: {str(e)}")
            return False
    
    def merge_pdfs(self, pdf_paths: List[str], output_path: str) -> bool:
        """
        Merge multiple PDF files into one
        
        Args:
            pdf_paths: List of PDF file paths to merge
            output_path: Path for merged PDF
            
        Returns:
            True if successful, False otherwise
        """
        try:
            pdf_writer = PyPDF2.PdfWriter()
            
            for pdf_path in pdf_paths:
                if not os.path.exists(pdf_path):
                    continue
                
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    
                    # Handle encrypted PDFs
                    if pdf_reader.is_encrypted:
                        if not pdf_reader.decrypt(''):
                            print(f"Skipping encrypted PDF: {pdf_path}")
                            continue
                    
                    # Add all pages
                    for page in pdf_reader.pages:
                        pdf_writer.add_page(page)
            
            # Write merged PDF
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"Error merging PDFs: {str(e)}")
            return False
    
    def split_pdf(self, output_directory: str, pages_per_file: int = 1) -> bool:
        """
        Split current PDF into multiple files
        
        Args:
            output_directory: Directory to save split files
            pages_per_file: Number of pages per output file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.current_pdf or not os.path.exists(output_directory):
                return False
            
            total_pages = len(self.current_pdf.pages)
            base_name = Path(self.current_path).stem if self.current_path else "split"
            
            file_count = 1
            current_pages = 0
            pdf_writer = PyPDF2.PdfWriter()
            
            for page_num in range(total_pages):
                page = self.current_pdf.pages[page_num]
                pdf_writer.add_page(page)
                current_pages += 1
                
                # Save file when we reach the pages limit or end of document
                if current_pages >= pages_per_file or page_num == total_pages - 1:
                    output_path = os.path.join(output_directory, f"{base_name}_part_{file_count}.pdf")
                    
                    with open(output_path, 'wb') as output_file:
                        pdf_writer.write(output_file)
                    
                    # Reset for next file
                    pdf_writer = PyPDF2.PdfWriter()
                    current_pages = 0
                    file_count += 1
            
            return True
            
        except Exception as e:
            print(f"Error splitting PDF: {str(e)}")
            return False
    
    def add_watermark(self, watermark_text: str, output_path: str, 
                     opacity: float = 0.3, font_size: int = 50) -> bool:
        """
        Add text watermark to all pages
        
        Args:
            watermark_text: Text to use as watermark
            output_path: Path for watermarked PDF
            opacity: Watermark opacity (0.0 to 1.0)
            font_size: Watermark font size
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.current_pdf:
                return False
            
            # Create watermark PDF
            watermark_buffer = io.BytesIO()
            c = canvas.Canvas(watermark_buffer, pagesize=letter)
            
            # Set transparency and add watermark text
            c.setFillColorRGB(0.5, 0.5, 0.5, alpha=opacity)
            c.setFont("Helvetica-Bold", font_size)
            
            # Center the watermark
            page_width, page_height = letter
            text_width = c.stringWidth(watermark_text, "Helvetica-Bold", font_size)
            x = (page_width - text_width) / 2
            y = page_height / 2
            
            # Rotate and draw text
            c.saveState()
            c.translate(x, y)
            c.rotate(45)  # 45-degree rotation
            c.drawString(0, 0, watermark_text)
            c.restoreState()
            c.save()
            
            # Create watermark PDF reader
            watermark_buffer.seek(0)
            watermark_pdf = PyPDF2.PdfReader(watermark_buffer)
            watermark_page = watermark_pdf.pages[0]
            
            # Apply watermark to all pages
            pdf_writer = PyPDF2.PdfWriter()
            for page in self.current_pdf.pages:
                page.merge_page(watermark_page)
                pdf_writer.add_page(page)
            
            # Write output PDF
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"Error adding watermark: {str(e)}")
            return False
    
    def render_page(self, page_number: int, zoom: float = 1.0) -> Optional[PILImage.Image]:
        """Render a single page as an image"""
        if not self.current_path or page_number < 1 or page_number > self.get_page_count():
            return None

        images = convert_from_path(self.current_path, first_page=page_number, last_page=page_number)
        if images:
            return images[0]
        return None

    def close_pdf(self):
        """Close current PDF and clear data"""
        if self.file_stream:
            self.file_stream.close()
            self.file_stream = None

        self.current_pdf = None
        self.current_pages = []
        self.current_path = None