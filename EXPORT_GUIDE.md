# README to Word Export - Usage Guide

This document explains how to use the README to Word export functionality.

## Overview

The `export_readme_to_word.py` script converts the project's README.md file into a professionally formatted Microsoft Word document with proper styling, headers, code blocks, and tables.

## Features

- ✅ **Professional Formatting**: Clean, corporate-style formatting
- ✅ **Headers & Subheaders**: Properly styled heading hierarchy
- ✅ **Code Blocks**: Syntax-highlighted code sections with background shading
- ✅ **Tables**: Formatted tables with headers and borders
- ✅ **Inline Code**: Monospace formatting for inline code snippets
- ✅ **Document Metadata**: Auto-generated document information
- ✅ **Header & Footer**: Professional document headers and footers
- ✅ **Table of Contents Ready**: Structure suitable for TOC generation

## Prerequisites

The export functionality requires additional Python packages:

```bash
pip install python-docx==0.8.11 markdown==3.5.1 beautifulsoup4==4.12.2 lxml==4.9.3
```

Or install from the requirements file:

```bash
pip install -r requirements_export.txt
```

## Usage Methods

### Method 1: Direct Python Script

```bash
python export_readme_to_word.py
```

### Method 2: Batch Script (Windows)

Double-click `export_readme.bat` or run:

```cmd
export_readme.bat
```

### Method 3: PowerShell Script (Windows)

```powershell
.\export_readme.ps1
```

## Output

The script generates a Word document named:
`User_Authentication_System_Documentation.docx`

The document includes:
- Cover page with title
- Formatted content from README.md
- Professional styling
- Document metadata page
- Header and footer with generation date

## File Structure

```
auth_service/
├── README.md                              # Source markdown file
├── export_readme_to_word.py              # Main export script
├── requirements_export.txt               # Export dependencies
├── export_readme.bat                     # Windows batch script
├── export_readme.ps1                     # PowerShell script
└── User_Authentication_System_Documentation.docx  # Generated output
```

## Customization

To customize the export:

1. **Modify Styles**: Edit the `setup_styles()` method in `export_readme_to_word.py`
2. **Change Output Name**: Modify the `output_path` variable in the `main()` function
3. **Add Custom Sections**: Extend the `add_document_info()` method

## Error Handling

The script includes robust error handling for:
- Missing README.md file
- Style conflicts
- File permission issues
- Missing dependencies

## Generated Document Features

- **File Size**: Typically 40-50 KB
- **Format**: Microsoft Word (.docx)
- **Compatibility**: Word 2010+, LibreOffice, Google Docs
- **Layout**: Professional business document style
- **Fonts**: Calibri for text, Consolas for code

## Support

If you encounter issues:

1. Ensure all dependencies are installed
2. Check that README.md exists in the same directory
3. Verify write permissions in the output directory
4. Run the script from the correct directory

## Example Output Structure

The generated Word document will contain:

1. **Title Page**: User Authentication System
2. **Table of Contents** (can be generated in Word)
3. **Quick Start Section**
4. **Setup Instructions**
5. **API Documentation** 
6. **Testing Guide**
7. **Security Features**
8. **Deployment Information**
9. **Document Metadata Page**

This provides a professional, printable version of your API documentation suitable for:
- Client presentations
- Technical documentation packages
- Offline reference
- Project portfolios
- Compliance documentation
