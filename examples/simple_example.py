#!/usr/bin/env python3
"""
Simple example demonstrating how to use the Mistral OCR PDF parser.
"""

import os
from dotenv import load_dotenv

# Import the parser from the package
from mistral_ocr import parse_pdf

# Load environment variables from .env file
load_dotenv()

def main():
    """
    Main function demonstrating how to use the Mistral OCR PDF parser.
    """
    # Path to the PDF file to parse
    pdf_path = "example.pdf"
    
    # Path to save the output markdown file
    output_path = "example_output.md"
    
    # Parse the PDF and generate markdown
    try:
        # Get API key from environment variable
        api_key = os.getenv("MISTRAL_API_KEY")
        
        # Parse the PDF
        markdown_output = parse_pdf(pdf_path, output_path, api_key)
        
        print(f"PDF parsed successfully. Output saved to: {output_path}")
        
        # Print a preview of the output
        preview_length = min(500, len(markdown_output))
        print(f"\nPreview of the output:\n{'-' * 40}\n{markdown_output[:preview_length]}...")
        
    except FileNotFoundError:
        print(f"Error: PDF file not found: {pdf_path}")
        print("Please provide a valid PDF file path.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 