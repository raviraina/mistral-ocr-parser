#!/usr/bin/env python3
"""
Batch processing example demonstrating how to process multiple PDF files.
"""

import os
import argparse
from dotenv import load_dotenv

# Import the batch processing function from the package
from mistral_ocr import batch_process_pdfs

# Load environment variables from .env file
load_dotenv()

def main():
    """
    Main function demonstrating batch processing of PDF files.
    """
    parser = argparse.ArgumentParser(description="Batch process PDF documents using Mistral's OCR API")
    parser.add_argument("--input-dir", "-i", required=True, help="Directory containing PDF files to process")
    parser.add_argument("--output-dir", "-o", required=True, help="Directory to save the output markdown files")
    parser.add_argument("--api-key", help="Mistral API key (if not provided, will use MISTRAL_API_KEY environment variable)")
    parser.add_argument("--file-pattern", "-p", default="*.pdf", help="Glob pattern for matching PDF files (default: *.pdf)")
    
    args = parser.parse_args()
    
    try:
        # Get API key from environment variable if not provided
        api_key = args.api_key or os.getenv("MISTRAL_API_KEY")
        
        if not api_key:
            raise ValueError("Mistral API key is required. Please provide it as an argument or set the MISTRAL_API_KEY environment variable.")
        
        # Process PDF files
        output_files = batch_process_pdfs(
            args.input_dir,
            args.output_dir,
            api_key,
            args.file_pattern
        )
        
        if output_files:
            print(f"\nSuccessfully processed {len(output_files)} PDF files")
            print(f"Output files saved to: {args.output_dir}")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 