"""
File utilities for Thomson PDF Generator
Handles file operations, validation, and type detection
"""
import os
import mimetypes
from pathlib import Path
from typing import List, Optional, Tuple
import chardet


class FileUtils:
    """Utility class for file operations"""
    
    # Supported file extensions for conversion
    SUPPORTED_EXTENSIONS = {
        '.txt': 'text/plain',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.pdf': 'application/pdf'
    }
    
    @staticmethod
    def is_supported_file(file_path: str) -> bool:
        """Check if file type is supported for conversion"""
        try:
            extension = Path(file_path).suffix.lower()
            return extension in FileUtils.SUPPORTED_EXTENSIONS
        except Exception:
            return False
    
    @staticmethod
    def get_file_type(file_path: str) -> Optional[str]:
        """Get MIME type of file"""
        try:
            extension = Path(file_path).suffix.lower()
            return FileUtils.SUPPORTED_EXTENSIONS.get(extension)
        except Exception:
            return None
    
    @staticmethod
    def validate_file_exists(file_path: str) -> bool:
        """Check if file exists and is readable"""
        try:
            return os.path.isfile(file_path) and os.access(file_path, os.R_OK)
        except Exception:
            return False
    
    @staticmethod
    def get_safe_filename(filename: str) -> str:
        """Generate a safe filename by removing/replacing invalid characters"""
        invalid_chars = '<>:"/\\|?*'
        safe_name = filename
        for char in invalid_chars:
            safe_name = safe_name.replace(char, '_')
        return safe_name
    
    @staticmethod
    def ensure_pdf_extension(filename: str) -> str:
        """Ensure filename has .pdf extension"""
        if not filename.lower().endswith('.pdf'):
            return f"{filename}.pdf"
        return filename
    
    @staticmethod
    def detect_text_encoding(file_path: str) -> str:
        """Detect text file encoding"""
        try:
            with open(file_path, 'rb') as file:
                raw_data = file.read()
                result = chardet.detect(raw_data)
                return result.get('encoding', 'utf-8') or 'utf-8'
        except Exception:
            return 'utf-8'
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes"""
        try:
            return os.path.getsize(file_path)
        except Exception:
            return 0
    
    @staticmethod
    def create_backup_filename(original_path: str) -> str:
        """Create a backup filename for the original file"""
        path = Path(original_path)
        timestamp = int(os.path.getmtime(original_path))
        return str(path.parent / f"{path.stem}_backup_{timestamp}{path.suffix}")