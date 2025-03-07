"""
Utility functions for the Mistral OCR PDF parser.
"""

from pathlib import Path
from typing import Optional, List
from tqdm import tqdm

from .parser import MistralOCRParser


def batch_process_pdfs(
    input_dir: str,
    output_dir: str,
    api_key: Optional[str] = None,
    file_pattern: str = "*.pdf",
) -> List[str]:
    """
    Process multiple PDF files in a directory using Mistral's OCR API.

    Args:
        input_dir: Directory containing PDF files to process.
        output_dir: Directory to save the output markdown files.
        api_key: Optional Mistral API key.
        file_pattern: Glob pattern for matching PDF files.

    Returns:
        A list of paths to the generated markdown files.
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)

    # Find all PDF files in the input directory
    pdf_files = list(input_dir.glob(file_pattern))

    if not pdf_files:
        print(f"No PDF files found in {input_dir} matching pattern '{file_pattern}'")
        return []

    print(f"Found {len(pdf_files)} PDF files to process")

    # Initialize the parser
    parser = MistralOCRParser(api_key=api_key)

    # Process each PDF file
    output_files = []

    for pdf_file in tqdm(pdf_files, desc="Processing PDFs"):
        try:
            # Generate output file path
            output_file = output_dir / f"{pdf_file.stem}.md"

            # Parse the PDF
            parser.parse_pdf(pdf_file, output_file)

            output_files.append(str(output_file))

        except Exception as e:
            print(f"Error processing {pdf_file}: {e}")

    return output_files
