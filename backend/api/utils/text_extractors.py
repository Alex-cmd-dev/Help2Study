"""
TEXT EXTRACTION UTILITIES - The "Document Readers" Toolbox

This module contains utility functions for extracting text from different file formats.
These are PURE FUNCTIONS - they take a file path and return text, with no side effects.

EDUCATIONAL NOTE:
We extracted these functions from geminiapi.py into a separate utility module.
This is an example of the "Single Responsibility Principle" - each function
does ONE thing and does it well.

WHY SEPARATE THESE FUNCTIONS:
1. REUSABILITY: Can be used by other parts of the app (maybe for file preview?)
2. TESTABILITY: Easy to test - just pass a file path, check the text output
3. MAINTAINABILITY: If PDF parsing changes, update only this file
4. CLARITY: geminiapi.py can focus on AI logic, not file format details

CONCEPTS: Pure Functions, Utility Functions, Single Responsibility Principle
RELATED: geminiapi.py (uses these functions), file_validators.py (validates before extraction)
"""

import PyPDF2
import docx2txt


def pdf_to_text(file_path):
    """
    Extract text content from a PDF file.

    PURE FUNCTION: Same input always produces same output, no side effects

    Args:
        file_path (str): Absolute path to the PDF file

    Returns:
        str: Extracted text from all pages

    Raises:
        ValueError: If PDF cannot be read or is corrupted

    EXAMPLE:
        text = pdf_to_text("/path/to/document.pdf")
        print(text)  # "Chapter 1: Introduction..."

    EDUCATIONAL NOTE:
    PyPDF2 is a library for reading PDF files. It:
    - Opens the file in binary mode ("rb")
    - Creates a PdfReader object
    - Iterates through pages
    - Extracts text from each page

    WHY BINARY MODE ("rb"):
    PDFs contain binary data (images, fonts, etc.), not just text.
    Reading in binary mode preserves this data structure.
    """
    try:
        text = ""
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            # Loop through all pages and extract text
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text()
        return text
    except Exception as e:
        # Re-raise with more context for debugging
        raise ValueError(f"Failed to read PDF file: {str(e)}")


def docx_to_text(file_path):
    """
    Extract text content from a DOCX (Microsoft Word) file.

    PURE FUNCTION: Same input always produces same output, no side effects

    Args:
        file_path (str): Absolute path to the DOCX file

    Returns:
        str: Extracted text from the document

    Raises:
        ValueError: If DOCX cannot be read or is corrupted

    EXAMPLE:
        text = docx_to_text("/path/to/essay.docx")
        print(text)  # "My Essay\n\nThis is the content..."

    EDUCATIONAL NOTE:
    docx2txt is a library specifically for .docx files (Word 2007+).
    It extracts:
    - Body text
    - Headers and footers
    - Tables
    But NOT:
    - Images (returns as placeholders)
    - Formatting (bold, italic, etc.)

    WHY NOT JUST .doc FILES:
    .doc (old Word format) is binary, .docx is XML-based.
    This library only works with the newer XML format.
    """
    try:
        text = docx2txt.process(file_path)
        return text
    except Exception as e:
        raise ValueError(f"Failed to read DOCX file: {str(e)}")


def txt_to_text(file_path):
    """
    Read content from a plain text file.

    PURE FUNCTION: Same input always produces same output, no side effects

    Args:
        file_path (str): Absolute path to the TXT file

    Returns:
        str: File contents

    Raises:
        ValueError: If file cannot be read or encoding is wrong

    EXAMPLE:
        text = txt_to_text("/path/to/notes.txt")
        print(text)  # "My notes from class..."

    EDUCATIONAL NOTE:
    Plain text files are the simplest - just characters!

    ENCODING:
    - encoding="utf-8": Handles international characters (é, 中, etc.)
    - Without it, might fail on non-ASCII characters
    - UTF-8 is the standard for web and modern applications
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        raise ValueError(f"Failed to read text file: {str(e)}")


def extract_text_from_file(file_path, mime_type):
    """
    Smart dispatcher function - routes to the correct extractor based on file type.

    This is a FACADE PATTERN - provides a simple interface to complex subsystems.
    Instead of calling pdf_to_text() or docx_to_text() directly, you call this!

    Args:
        file_path (str): Absolute path to the file
        mime_type (str): MIME type of the file (e.g., "application/pdf")

    Returns:
        str: Extracted text

    Raises:
        ValueError: If file type is unsupported

    EXAMPLE:
        text = extract_text_from_file("/path/to/file.pdf", "application/pdf")

    EDUCATIONAL NOTE - MIME TYPES:
    MIME types tell us what kind of file we're dealing with:
    - application/pdf → PDF file
    - text/plain → Plain text file
    - application/vnd.openxmlformats-officedocument.wordprocessingml.document → DOCX

    WHY USE MIME TYPE INSTEAD OF FILE EXTENSION:
    - More reliable (extension can be wrong)
    - Standard across web applications
    - Set by the browser during upload

    DESIGN PATTERN - FACADE:
    This function hides the complexity of choosing the right extractor.
    The caller doesn't need to know about PyPDF2 or docx2txt!

    FUTURE ENHANCEMENT:
    You could add more extractors here:
    - .pptx files (presentations)
    - .xlsx files (spreadsheets)
    - .epub files (ebooks)
    Just add the function and update this dispatcher!
    """
    if mime_type == "application/pdf":
        return pdf_to_text(file_path)
    elif mime_type == "text/plain":
        return txt_to_text(file_path)
    elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return docx_to_text(file_path)
    else:
        raise ValueError(f"Unsupported file type: {mime_type}")


"""
NEXT STEPS FOR LEARNING:

Once you're comfortable with these utilities, explore:

1. FILE VALIDATORS: Create utils/file_validators.py
   - Check file size before processing
   - Validate MIME type matches extension
   - Scan for malicious content

2. TESTING: Create tests/test_text_extractors.py
   - Test each function with sample files
   - Test error cases (corrupted files, wrong format)
   - Mock file system for faster tests

3. ADVANCED PATTERNS: Learn about
   - Strategy Pattern (different extractors as strategies)
   - Factory Pattern (create extractors dynamically)
   - Decorator Pattern (add features like caching)

See ADVANCED_PATTERNS.md for detailed explanations!
"""
