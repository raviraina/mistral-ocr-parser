"""
Mistral OCR PDF Parser

A library for parsing PDF documents using Mistral's OCR API, extracting text content
while maintaining document structure, and converting images into structured markdown
sections with detailed descriptions.
"""

__version__ = "0.1.0"

from .parser import MistralOCRParser, parse_pdf
from .utils import batch_process_pdfs
from .image import (
    generate_image_description, 
    process_image_ocr, 
    structured_ocr,
    Language,
    StructuredOCR
)

__all__ = [
    "MistralOCRParser", 
    "parse_pdf", 
    "batch_process_pdfs",
    "generate_image_description",
    "process_image_ocr",
    "structured_ocr",
    "Language",
    "StructuredOCR"
] 