# Thomson PDF Generator

A comprehensive, production-ready PDF converter, viewer, editor, and signing tool built with Python. All processing happens locally on your device without requiring external APIs or internet connectivity.

![Thomson PDF Generator](https://img.shields.io/badge/Version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## 🚀 Features

### 📄 File Conversion
- **Supported Input Formats**: TXT, DOC, DOCX, XLSX, PNG, JPG, JPEG, GIF, BMP
- **Output**: High-quality PDF documents
- **Batch Processing**: Convert multiple files simultaneously
- **Smart Formatting**: Preserves document structure and formatting

### 📖 PDF Viewer
- **Full Navigation**: Page-by-page browsing with jump-to-page functionality
- **Text Search**: Find and highlight text within documents
- **Document Info**: View metadata, properties, and document statistics
- **Zoom & View**: Optimized text display for easy reading

### ✏️ PDF Editor
- **Text Annotations**: Add custom text with configurable fonts and colors
- **Shape Tools**: Insert rectangles, circles, and lines
- **Highlighting**: Highlight important text sections
- **Page Operations**: Rotate, delete, crop, and insert pages
- **Image Insertion**: Add images to PDF documents

### 🔐 Digital Signatures
- **Certificate Generation**: Create self-signed certificates
- **Certificate Management**: Load, save, and manage digital certificates
- **PDF Signing**: Digitally sign documents with custom positioning
- **Signature Verification**: Verify existing digital signatures

### 🎨 Modern Interface
- **Tabbed Layout**: Organized workflow with dedicated tabs for each function
- **Professional Design**: Clean, modern UI with CustomTkinter theming
- **Dark/Light Themes**: Toggle between appearance modes
- **Responsive Layout**: Adaptable interface for different screen sizes

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- Tkinter (usually comes with Python)

### Method 1: Clone and Install
```bash
# Clone the repository
git clone https://github.com/Thomson-BG/thomson_pdf_generator.git
cd thomson_pdf_generator

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

### Method 2: Direct Installation
```bash
# Install directly from source
pip install git+https://github.com/Thomson-BG/thomson_pdf_generator.git

# Run the application
thomson-pdf-generator
```

### Method 3: Local Development
```bash
# For development/testing
git clone https://github.com/Thomson-BG/thomson_pdf_generator.git
cd thomson_pdf_generator
pip install -e .
```

## 🖥️ Usage

### Quick Start
1. **Launch the Application**
   ```bash
   python main.py
   ```

2. **Convert Files to PDF**
   - Go to the "Converter" tab
   - Click "Add Files" or drag & drop files
   - Select output directory
   - Click "Convert to PDF"

3. **View PDF Documents**
   - Go to the "Viewer" tab
   - Click "Open PDF" to load a document
   - Use navigation controls to browse pages
   - Use the search function to find text

4. **Edit PDF Documents**
   - Go to the "Editor" tab
   - Open a PDF for editing
   - Use tools on the left to add annotations
   - Save your changes

5. **Sign PDF Documents**
   - Go to the "Signer" tab
   - Generate or load a digital certificate
   - Select a PDF to sign
   - Configure signature options
   - Click "Sign PDF"

### Advanced Features

#### Batch Conversion
- Add multiple files of different types
- Choose to combine into single PDF or convert individually
- Monitor conversion progress in real-time

#### PDF Manipulation
- **Merge PDFs**: Combine multiple PDF files into one
- **Split PDFs**: Divide a PDF into multiple files
- **Extract Pages**: Save specific pages as new PDF
- **Add Watermarks**: Brand your documents

#### Certificate Management
- Generate self-signed certificates for personal use
- Load existing certificates from PEM/CRT files
- Save certificates for future use
- View detailed certificate information

## 🔧 Configuration

### Supported File Types
- **Text Files**: `.txt`
- **Microsoft Word**: `.doc`, `.docx`
- **Microsoft Excel**: `.xlsx`
- **Images**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`
- **PDF Files**: `.pdf` (for viewing/editing)

### System Requirements
- **RAM**: Minimum 512MB, Recommended 1GB+
- **Storage**: 100MB for application + space for processed files
- **OS**: Windows 7+, macOS 10.12+, Linux (any modern distribution)

## 🧪 Testing

Run the test suite to verify functionality:

```bash
# Run core functionality tests
python tests/test_core.py

# Test specific modules
python -m pytest tests/ -v
```

## 🛠️ Development

### Project Structure
```
thomson_pdf_generator/
├── core/                   # Core functionality modules
│   ├── converter.py       # File conversion logic
│   ├── pdf_handler.py     # PDF operations
│   ├── editor.py          # PDF editing features
│   └── signer.py          # Digital signature handling
├── gui/                   # User interface components
│   ├── main_window.py     # Main application window
│   ├── converter_tab.py   # File conversion interface
│   ├── viewer_tab.py      # PDF viewer interface
│   ├── editor_tab.py      # PDF editor interface
│   └── signer_tab.py      # Digital signature interface
├── utils/                 # Utility modules
│   ├── file_utils.py      # File handling utilities
│   └── ui_utils.py        # UI helper functions
├── tests/                 # Test modules
└── main.py               # Application entry point
```

### Key Dependencies
- **GUI Framework**: CustomTkinter (modern tkinter theming)
- **PDF Processing**: ReportLab, PyPDF2
- **Document Handling**: python-docx, openpyxl
- **Image Processing**: Pillow
- **Digital Signatures**: cryptography
- **Text Processing**: chardet

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/Thomson-BG/thomson_pdf_generator/issues)
- **Discussions**: Join the community discussions
- **Documentation**: Check the [Wiki](https://github.com/Thomson-BG/thomson_pdf_generator/wiki) for detailed guides

## 🏆 Acknowledgments

- Built with Python and the amazing open-source ecosystem
- CustomTkinter for modern GUI theming
- ReportLab for professional PDF generation
- The Python community for excellent libraries and tools

## 🔄 Version History

- **v1.0.0** (2025) - Initial release with full feature set
  - Complete file conversion capabilities
  - PDF viewing and navigation
  - PDF editing with annotations
  - Digital signature support
  - Modern GUI interface
  - Comprehensive testing

---

**Thomson PDF Generator** - Transform, View, Edit, and Sign PDFs with Confidence

Made with ❤️ by Thomson-BG