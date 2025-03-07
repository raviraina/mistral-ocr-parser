#!/usr/bin/env python3
"""
Batch processing example demonstrating how to process multiple PDF files.
"""

import os
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Import the batch processing function from the package
from mistral_ocr import batch_process_pdfs

# Load environment variables from .env file
load_dotenv()


def main():
    """
    Main function demonstrating batch processing of PDF files.
    """
    # Default directories
    default_input_dir = "examples/example_pdfs"
    default_output_dir = "examples/output"

    parser = argparse.ArgumentParser(
        description="Batch process PDF documents using Mistral's OCR API"
    )
    parser.add_argument(
        "--input-dir",
        "-i",
        default=default_input_dir,
        help=f"Directory containing PDF files to process (default: {default_input_dir})",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        default=default_output_dir,
        help=f"Directory to save the output markdown files (default: {default_output_dir})",
    )
    parser.add_argument(
        "--api-key",
        help="Mistral API key (if not provided, will use MISTRAL_API_KEY environment variable)",
    )
    parser.add_argument(
        "--file-pattern",
        "-p",
        default="*.pdf",
        help="Glob pattern for matching PDF files (default: *.pdf)",
    )

    args = parser.parse_args()

    try:
        # Get API key from environment variable if not provided
        api_key = args.api_key or os.getenv("MISTRAL_API_KEY")

        if not api_key:
            print(
                "Error: MISTRAL_API_KEY environment variable not set and no API key provided."
            )
            print(
                "Please set your Mistral API key in the .env file, as an environment variable, or use the --api-key option."
            )
            return 1

        # Create output directory if it doesn't exist
        Path(args.output_dir).mkdir(parents=True, exist_ok=True)

        # List available PDF files
        pdf_files = list(Path(args.input_dir).glob(args.file_pattern))
        print(f"Found {len(pdf_files)} PDF files to process:")
        for pdf_file in pdf_files:
            print(f"  - {pdf_file.name}")

        # Process PDF files
        output_files = batch_process_pdfs(
            args.input_dir, args.output_dir, api_key, args.file_pattern
        )

        if output_files:
            print(f"\nSuccessfully processed {len(output_files)} PDF files")
            print(f"Output files saved to: {args.output_dir}")
            for output_file in output_files:
                print(f"  - {output_file}")
        else:
            print(
                f"No PDF files found in {args.input_dir} matching pattern '{args.file_pattern}'"
            )
            print(
                f"Please make sure the example PDF files exist in the {args.input_dir} directory."
            )
            return 1

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
