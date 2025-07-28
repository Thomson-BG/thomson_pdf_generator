"""
Test script for Thomson PDF Generator core functionality
Tests the conversion and PDF handling capabilities without GUI
"""
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import sys
sys.path.append('.')

from core.converter import FileConverter
from core.pdf_handler import PDFHandler
from core.editor import PDFEditor
from core.signer import PDFSigner
from utils.file_utils import FileUtils


def test_file_utils():
    """Test file utility functions"""
    print("Testing File Utils...")
    
    # Test supported file detection
    assert FileUtils.is_supported_file("test.txt") == True
    assert FileUtils.is_supported_file("test.docx") == True
    assert FileUtils.is_supported_file("test.pdf") == True
    assert FileUtils.is_supported_file("test.xyz") == False
    
    # Test file type detection
    assert FileUtils.get_file_type("test.txt") == "text/plain"
    assert FileUtils.get_file_type("test.pdf") == "application/pdf"
    
    # Test filename safety
    assert FileUtils.get_safe_filename("test<>file.txt") == "test__file.txt"
    
    # Test PDF extension
    assert FileUtils.ensure_pdf_extension("test") == "test.pdf"
    assert FileUtils.ensure_pdf_extension("test.pdf") == "test.pdf"
    
    print("✓ File Utils tests passed")


def test_converter():
    """Test file converter functionality"""
    print("Testing File Converter...")
    
    converter = FileConverter()
    
    # Create a test text file
    test_dir = Path("/tmp/pdf_test")
    test_dir.mkdir(exist_ok=True)
    
    test_txt = test_dir / "test.txt"
    with open(test_txt, 'w') as f:
        f.write("This is a test document.\nLine 2\nLine 3")
    
    output_pdf = test_dir / "test_output.pdf"
    
    # Test text to PDF conversion
    success = converter.convert_to_pdf(str(test_txt), str(output_pdf))
    
    if success and output_pdf.exists():
        print("✓ Text to PDF conversion successful")
        print(f"  Output size: {output_pdf.stat().st_size} bytes")
    else:
        print("✗ Text to PDF conversion failed")
        return False
    
    return True


def test_pdf_handler():
    """Test PDF handler functionality"""
    print("Testing PDF Handler...")
    
    # First ensure we have a PDF to test with
    if not test_converter():
        return False
    
    handler = PDFHandler()
    test_pdf = Path("/tmp/pdf_test/test_output.pdf")
    
    if handler.open_pdf(str(test_pdf)):
        print("✓ PDF opened successfully")
        
        # Test basic info
        page_count = handler.get_page_count()
        print(f"  Pages: {page_count}")
        
        if page_count > 0:
            page_text = handler.get_page_text(1)
            print(f"  Page 1 text length: {len(page_text)} characters")
            
            # Test search
            results = handler.search_text("test")
            print(f"  Search results for 'test': {len(results)} found")
        
        info = handler.get_pdf_info()
        print(f"  PDF info: {info.get('filename', 'Unknown')}")
        
        print("✓ PDF Handler tests passed")
        return True
    else:
        print("✗ Failed to open PDF")
        return False


def test_signer():
    """Test PDF signing functionality"""
    print("Testing PDF Signer...")
    
    signer = PDFSigner()
    
    # Test certificate generation
    if signer.generate_self_signed_certificate(
        common_name="Test User",
        email="test@example.com",
        organization="Test Org"
    ):
        print("✓ Certificate generated successfully")
        
        cert_info = signer.get_certificate_info()
        print(f"  Certificate for: {cert_info.get('common_name', 'Unknown')}")
        
        # Test certificate loading status
        if signer.is_certificate_loaded():
            print("✓ Certificate is loaded and ready")
            return True
        else:
            print("✗ Certificate not properly loaded")
            return False
    else:
        print("✗ Failed to generate certificate")
        return False


def test_editor():
    """Test PDF editor functionality"""
    print("Testing PDF Editor...")
    
    # We'll just test that the editor can be instantiated
    editor = PDFEditor()
    print("✓ PDF Editor initialized")
    
    return True


def create_sample_files():
    """Create sample files for testing"""
    print("Creating sample files...")
    
    test_dir = Path("/tmp/pdf_test")
    test_dir.mkdir(exist_ok=True)
    
    # Create various test files
    files = {
        "sample.txt": "This is a sample text file.\nIt has multiple lines.\nFor PDF conversion testing.",
        "README.txt": "Thomson PDF Generator Test Files\n\nThis directory contains test files for the PDF generator."
    }
    
    for filename, content in files.items():
        filepath = test_dir / filename
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"  Created: {filename}")
    
    print(f"✓ Sample files created in {test_dir}")


def main():
    """Run all tests"""
    print("Thomson PDF Generator - Core Functionality Tests")
    print("=" * 50)
    
    try:
        # Create test environment
        create_sample_files()
        
        # Run tests
        tests = [
            test_file_utils,
            test_converter,
            test_pdf_handler,
            test_editor,
            test_signer
        ]
        
        passed = 0
        total = len(tests)
        
        for test_func in tests:
            try:
                if test_func():
                    passed += 1
                print()
            except Exception as e:
                print(f"✗ Test {test_func.__name__} failed with error: {e}")
                import traceback
                traceback.print_exc()
                print()
        
        print("=" * 50)
        print(f"Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! Core functionality is working correctly.")
            return 0
        else:
            print("⚠️  Some tests failed. Please check the output above.")
            return 1
            
    except Exception as e:
        print(f"Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())