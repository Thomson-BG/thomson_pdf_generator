# Thomson PDF Generator

A comprehensive PDF converter, viewer, editor, and signing tool that works entirely offline without external APIs or converters.

## Features

- **File Conversion**: Convert various formats (.txt, .doc, .docx, .xlsx) to PDF
- **PDF Viewer**: Open and view PDF documents with navigation and search
- **PDF Editor**: Edit PDF content, add annotations, and modify documents  
- **Digital Signing**: Sign PDF documents with digital certificates
- **Offline Processing**: All operations happen locally on your device
- **Modern UI**: Professional, polished interface built with CustomTkinter

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

## Supported File Formats

### Input Formats
- Text files (.txt)
- Microsoft Word (.doc, .docx)  
- Microsoft Excel (.xlsx)
- Images (.png, .jpg, .jpeg, .gif, .bmp)

### Output Format
- PDF (.pdf)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Thomson-BG/thomson_pdf_generator.git
cd thomson_pdf_generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

## Usage

1. **Convert Files**: Use the Converter tab to select and convert files to PDF
2. **View PDFs**: Use the Viewer tab to open and view PDF documents  
3. **Edit PDFs**: Use the Editor tab to modify PDF content with annotations
4. **Sign PDFs**: Use the Signer tab to digitally sign PDF documents

## Testing

Run the test suite to verify functionality:
```bash
python tests/test_core.py
```

## Project Structure

```
thomson_pdf_generator/
├── core/              # Core functionality modules
├── gui/               # User interface components  
├── utils/             # Utility functions
├── tests/             # Test modules
├── main.py           # Application entry point
├── requirements.txt  # Dependencies
└── README.md        # This file
```

## Requirements

- Python 3.8+
- See `requirements.txt` for complete dependency list

## License

MIT License - see LICENSE file for details.

---

**Thomson PDF Generator** - Professional PDF processing made simple.