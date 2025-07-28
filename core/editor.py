"""
PDF editor for Thomson PDF Generator
Advanced PDF editing capabilities including annotations and text modifications
"""
import os
from pathlib import Path
from typing import List, Optional, Dict, Any, Tuple
import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.colors import Color
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import io


class PDFEditor:
    """Handles advanced PDF editing operations"""
    
    def __init__(self):
        self.current_pdf_path = None
        self.annotations = []
        self.styles = getSampleStyleSheet()
    
    def add_text_annotation(self, pdf_path: str, page_number: int, x: float, y: float, 
                           text: str, font_size: int = 12, color: str = "black",
                           output_path: str = None) -> bool:
        """
        Add text annotation to a PDF page
        
        Args:
            pdf_path: Path to input PDF
            page_number: Page number (1-based)
            x, y: Position coordinates
            text: Text to add
            font_size: Font size for text
            color: Text color
            output_path: Path for output PDF (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(pdf_path):
                return False
            
            if output_path is None:
                output_path = pdf_path
            
            # Create annotation overlay
            annotation_buffer = io.BytesIO()
            c = canvas.Canvas(annotation_buffer, pagesize=letter)
            
            # Set text properties
            color_obj = getattr(colors, color.lower(), colors.black)
            c.setFillColor(color_obj)
            c.setFont("Helvetica", font_size)
            
            # Add text at specified position
            c.drawString(x, y, text)
            c.save()
            
            # Read original PDF
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                
                # Process each page
                for i, page in enumerate(pdf_reader.pages):
                    if i == page_number - 1:  # Target page
                        # Apply annotation
                        annotation_buffer.seek(0)
                        annotation_pdf = PyPDF2.PdfReader(annotation_buffer)
                        annotation_page = annotation_pdf.pages[0]
                        page.merge_page(annotation_page)
                    
                    pdf_writer.add_page(page)
                
                # Write output
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"Error adding text annotation: {str(e)}")
            return False
    
    def add_shape_annotation(self, pdf_path: str, page_number: int, shape_type: str,
                           coordinates: List[float], color: str = "red", 
                           line_width: float = 1.0, output_path: str = None) -> bool:
        """
        Add shape annotation (rectangle, circle, line) to a PDF page
        
        Args:
            pdf_path: Path to input PDF
            page_number: Page number (1-based)
            shape_type: Type of shape ("rectangle", "circle", "line")
            coordinates: List of coordinates [x1, y1, x2, y2]
            color: Shape color
            line_width: Line width
            output_path: Path for output PDF (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(pdf_path) or len(coordinates) < 4:
                return False
            
            if output_path is None:
                output_path = pdf_path
            
            # Create shape overlay
            shape_buffer = io.BytesIO()
            c = canvas.Canvas(shape_buffer, pagesize=letter)
            
            # Set shape properties
            color_obj = getattr(colors, color.lower(), colors.red)
            c.setStrokeColor(color_obj)
            c.setLineWidth(line_width)
            
            x1, y1, x2, y2 = coordinates[:4]
            
            # Draw shape based on type
            if shape_type.lower() == "rectangle":
                c.rect(x1, y1, x2 - x1, y2 - y1, fill=0)
            elif shape_type.lower() == "circle":
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
                radius = min(abs(x2 - x1), abs(y2 - y1)) / 2
                c.circle(center_x, center_y, radius, fill=0)
            elif shape_type.lower() == "line":
                c.line(x1, y1, x2, y2)
            
            c.save()
            
            # Read original PDF
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                
                # Process each page
                for i, page in enumerate(pdf_reader.pages):
                    if i == page_number - 1:  # Target page
                        # Apply shape annotation
                        shape_buffer.seek(0)
                        shape_pdf = PyPDF2.PdfReader(shape_buffer)
                        shape_page = shape_pdf.pages[0]
                        page.merge_page(shape_page)
                    
                    pdf_writer.add_page(page)
                
                # Write output
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"Error adding shape annotation: {str(e)}")
            return False
    
    def highlight_text(self, pdf_path: str, page_number: int, coordinates: List[float],
                      color: str = "yellow", output_path: str = None) -> bool:
        """
        Add highlight annotation to text area
        
        Args:
            pdf_path: Path to input PDF
            page_number: Page number (1-based)
            coordinates: List of coordinates [x1, y1, x2, y2] for highlight area
            color: Highlight color
            output_path: Path for output PDF (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(pdf_path) or len(coordinates) < 4:
                return False
            
            if output_path is None:
                output_path = pdf_path
            
            # Create highlight overlay
            highlight_buffer = io.BytesIO()
            c = canvas.Canvas(highlight_buffer, pagesize=letter)
            
            # Set highlight properties (semi-transparent)
            color_obj = getattr(colors, color.lower(), colors.yellow)
            c.setFillColor(color_obj)
            c.setStrokeColor(color_obj)
            
            x1, y1, x2, y2 = coordinates[:4]
            
            # Draw highlight rectangle
            c.rect(x1, y1, x2 - x1, y2 - y1, fill=1, stroke=0)
            c.save()
            
            # Read original PDF
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                
                # Process each page
                for i, page in enumerate(pdf_reader.pages):
                    if i == page_number - 1:  # Target page
                        # Apply highlight
                        highlight_buffer.seek(0)
                        highlight_pdf = PyPDF2.PdfReader(highlight_buffer)
                        highlight_page = highlight_pdf.pages[0]
                        page.merge_page(highlight_page)
                    
                    pdf_writer.add_page(page)
                
                # Write output
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"Error adding highlight: {str(e)}")
            return False
    
    def insert_image(self, pdf_path: str, page_number: int, image_path: str,
                    x: float, y: float, width: float = None, height: float = None,
                    output_path: str = None) -> bool:
        """
        Insert image into PDF page
        
        Args:
            pdf_path: Path to input PDF
            page_number: Page number (1-based)
            image_path: Path to image file
            x, y: Position coordinates
            width, height: Image dimensions (optional)
            output_path: Path for output PDF (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(pdf_path) or not os.path.exists(image_path):
                return False
            
            if output_path is None:
                output_path = pdf_path
            
            # Create image overlay
            image_buffer = io.BytesIO()
            c = canvas.Canvas(image_buffer, pagesize=letter)
            
            # Draw image
            if width and height:
                c.drawImage(image_path, x, y, width=width, height=height)
            else:
                c.drawImage(image_path, x, y)
            
            c.save()
            
            # Read original PDF
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                
                # Process each page
                for i, page in enumerate(pdf_reader.pages):
                    if i == page_number - 1:  # Target page
                        # Apply image
                        image_buffer.seek(0)
                        image_pdf = PyPDF2.PdfReader(image_buffer)
                        image_page = image_pdf.pages[0]
                        page.merge_page(image_page)
                    
                    pdf_writer.add_page(page)
                
                # Write output
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"Error inserting image: {str(e)}")
            return False
    
    def rotate_page(self, pdf_path: str, page_number: int, rotation: int,
                   output_path: str = None) -> bool:
        """
        Rotate a specific page
        
        Args:
            pdf_path: Path to input PDF
            page_number: Page number (1-based)
            rotation: Rotation angle (90, 180, 270 degrees)
            output_path: Path for output PDF (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(pdf_path):
                return False
            
            if output_path is None:
                output_path = pdf_path
            
            # Read original PDF
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                
                # Process each page
                for i, page in enumerate(pdf_reader.pages):
                    if i == page_number - 1:  # Target page
                        page.rotate(rotation)
                    pdf_writer.add_page(page)
                
                # Write output
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"Error rotating page: {str(e)}")
            return False
    
    def delete_page(self, pdf_path: str, page_number: int, output_path: str = None) -> bool:
        """
        Delete a specific page from PDF
        
        Args:
            pdf_path: Path to input PDF
            page_number: Page number to delete (1-based)
            output_path: Path for output PDF (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(pdf_path):
                return False
            
            if output_path is None:
                output_path = pdf_path
            
            # Read original PDF
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                
                # Add all pages except the one to delete
                for i, page in enumerate(pdf_reader.pages):
                    if i != page_number - 1:  # Skip target page
                        pdf_writer.add_page(page)
                
                # Write output
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"Error deleting page: {str(e)}")
            return False
    
    def insert_blank_page(self, pdf_path: str, page_number: int, 
                         page_size: Tuple[float, float] = None,
                         output_path: str = None) -> bool:
        """
        Insert a blank page at specified position
        
        Args:
            pdf_path: Path to input PDF
            page_number: Position to insert page (1-based)
            page_size: Page size tuple (width, height)
            output_path: Path for output PDF (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(pdf_path):
                return False
            
            if output_path is None:
                output_path = pdf_path
            
            if page_size is None:
                page_size = letter
            
            # Create blank page
            blank_buffer = io.BytesIO()
            c = canvas.Canvas(blank_buffer, pagesize=page_size)
            c.save()
            
            blank_buffer.seek(0)
            blank_pdf = PyPDF2.PdfReader(blank_buffer)
            blank_page = blank_pdf.pages[0]
            
            # Read original PDF
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                
                # Insert blank page at specified position
                for i, page in enumerate(pdf_reader.pages):
                    if i == page_number - 1:  # Insert position
                        pdf_writer.add_page(blank_page)
                    pdf_writer.add_page(page)
                
                # If inserting at the end
                if page_number > len(pdf_reader.pages):
                    pdf_writer.add_page(blank_page)
                
                # Write output
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"Error inserting blank page: {str(e)}")
            return False
    
    def crop_page(self, pdf_path: str, page_number: int, coordinates: List[float],
                 output_path: str = None) -> bool:
        """
        Crop a page to specified dimensions
        
        Args:
            pdf_path: Path to input PDF
            page_number: Page number (1-based)
            coordinates: Crop coordinates [left, bottom, right, top]
            output_path: Path for output PDF (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(pdf_path) or len(coordinates) < 4:
                return False
            
            if output_path is None:
                output_path = pdf_path
            
            # Read original PDF
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pdf_writer = PyPDF2.PdfWriter()
                
                # Process each page
                for i, page in enumerate(pdf_reader.pages):
                    if i == page_number - 1:  # Target page
                        # Set crop box
                        left, bottom, right, top = coordinates
                        page.cropbox.lower_left = (left, bottom)
                        page.cropbox.upper_right = (right, top)
                    
                    pdf_writer.add_page(page)
                
                # Write output
                with open(output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
            
            return True
            
        except Exception as e:
            print(f"Error cropping page: {str(e)}")
            return False