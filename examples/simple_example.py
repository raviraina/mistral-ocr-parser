#!/usr/bin/env python3
"""
Simple example demonstrating how to use the Mistral OCR PDF parser.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Import the parser from the package
from mistral_ocr import parse_pdf

# Load environment variables from .env file
load_dotenv()


def main():
    """
    Main function demonstrating how to use the Mistral OCR PDF parser.
    """
    # Path to the example PDF file
    pdf_path = Path("examples/example_pdfs/mistral7b.pdf")

    # Path to save the output markdown file
    output_path = Path("examples/output/mistral7b_output.md")

    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Parse the PDF and generate markdown
    try:
        # Get API key from environment variable
        api_key = os.getenv("MISTRAL_API_KEY")

        if not api_key:
            print("Error: MISTRAL_API_KEY environment variable not set.")
            print(
                "Please set your Mistral API key in the .env file or as an environment variable."
            )
            return 1

        print(f"Processing PDF: {pdf_path}")

        # Parse the PDF
        markdown_output = parse_pdf(pdf_path, output_path, api_key)

        print(f"PDF parsed successfully. Output saved to: {output_path}")

        # Print a preview of the output
        preview_length = min(500, len(markdown_output))
        print(
            f"\nPreview of the output:\n{'-' * 40}\n{markdown_output[:preview_length]}..."
        )

    except FileNotFoundError:
        print(f"Error: PDF file not found: {pdf_path}")
        print("Please make sure the example PDF file exists.")
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
