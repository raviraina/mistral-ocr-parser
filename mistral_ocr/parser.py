"""
Core parser functionality for the Mistral OCR PDF parser.
"""

import os
import json
import argparse
from pathlib import Path
from typing import Optional, Union, Any

from dotenv import load_dotenv
from tqdm import tqdm

from mistralai import Mistral, DocumentURLChunk

from .image import generate_image_description

# Load environment variables from .env file
load_dotenv()


class MistralOCRParser:
    """
    A class for parsing PDF documents using Mistral's OCR API and generating
    structured markdown output with detailed image descriptions.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the MistralOCRParser with the provided API key.

        Args:
            api_key: Mistral API key. If not provided, it will be read from the MISTRAL_API_KEY environment variable.
        """
        self.api_key = api_key or os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either as an argument or as the MISTRAL_API_KEY environment variable."
            )
        self.client = Mistral(api_key=self.api_key)

    def parse_pdf(
        self, pdf_path: Union[str, Path], output_path: Optional[Union[str, Path]] = None
    ) -> str:
        """
        Parse a PDF document using Mistral's OCR API and generate structured markdown output.

        Args:
            pdf_path: Path to the PDF file to parse.
            output_path: Optional path to save the output markdown file.

        Returns:
            A string containing the structured markdown output.
        """
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        print(f"Processing PDF: {pdf_path}")

        # Upload the PDF file to Mistral
        uploaded_file = self._upload_file(pdf_path)

        # Get a signed URL for the uploaded file
        signed_url = self._get_signed_url(uploaded_file.id)

        # Process the PDF with Mistral OCR
        ocr_response = self._process_ocr(signed_url.url)

        # Parse the OCR response and generate markdown
        markdown_output = self._generate_markdown(ocr_response)

        # Save the output if a path is provided
        if output_path:
            output_path = Path(output_path)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(markdown_output)
            print(f"Output saved to: {output_path}")

        return markdown_output

    def _upload_file(self, file_path: Path):
        """
        Upload a file to Mistral.

        Args:
            file_path: Path to the file to upload.

        Returns:
            The uploaded file object.
        """
        print("Uploading file to Mistral...")
        uploaded_file = self.client.files.upload(
            file={
                "file_name": file_path.stem,
                "content": file_path.read_bytes(),
            },
            purpose="ocr",
        )
        return uploaded_file

    def _get_signed_url(self, file_id: str):
        """
        Get a signed URL for an uploaded file.

        Args:
            file_id: ID of the uploaded file.

        Returns:
            The signed URL object.
        """
        print("Getting signed URL...")
        signed_url = self.client.files.get_signed_url(file_id=file_id, expiry=1)
        return signed_url

    def _process_ocr(self, document_url: str):
        """
        Process a document with Mistral OCR.

        Args:
            document_url: URL of the document to process.

        Returns:
            The OCR response.
        """
        print("Processing document with Mistral OCR...")

        # Using the correct parameters based on the Colab notebook
        ocr_response = self.client.ocr.process(
            document=DocumentURLChunk(document_url=document_url),
            model="mistral-ocr-latest",
            include_image_base64=True,
        )
        return ocr_response

    def _generate_markdown(self, ocr_response):
        """
        Generate structured markdown from the OCR response.

        Args:
            ocr_response: The OCR response from Mistral.

        Returns:
            A string containing the structured markdown output.
        """
        print("Generating markdown output...")

        # Parse the OCR response
        response_dict = json.loads(ocr_response.json())

        # Check if the response contains pages with markdown content
        if hasattr(ocr_response, "pages") and len(ocr_response.pages) > 0:
            # If the response has pages with markdown, use that directly
            return ocr_response.pages[0].markdown

        # Check if the response contains markdown content
        if "markdown" in response_dict:
            return response_dict["markdown"]

        # If not, extract content blocks and generate markdown
        blocks = response_dict.get("blocks", [])

        # Generate markdown
        markdown_parts = []

        for block in tqdm(blocks, desc="Processing blocks"):
            block_type = block.get("type")

            if block_type == "text":
                # Add text content
                markdown_parts.append(block.get("text", ""))
                markdown_parts.append("\n\n")

            elif block_type == "image":
                # Process image block
                image_data = block.get("image", {})
                image_base64 = image_data.get("base64", "")

                if image_base64:
                    # Generate image description using Mistral
                    image_description = generate_image_description(
                        image_base64, self.client
                    )

                    # Add image with description to markdown
                    markdown_parts.append(
                        f"![Image]({image_data.get('url', 'image_placeholder.png')})\n"
                    )
                    markdown_parts.append(
                        f"*Image Description: {image_description['description']}*\n\n"
                    )

                    # Add image metadata if available
                    if image_description.get("metadata"):
                        markdown_parts.append("**Image Metadata:**\n")
                        for key, value in image_description["metadata"].items():
                            markdown_parts.append(f"- {key}: {value}\n")
                        markdown_parts.append("\n")

        return "".join(markdown_parts)


def parse_pdf(
    pdf_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    api_key: Optional[str] = None,
) -> str:
    """
    Parse a PDF document using Mistral's OCR API.

    Args:
        pdf_path: Path to the PDF file.
        output_path: Path to save the output markdown file. If not provided,
                    the output will be saved in the same directory as the PDF file.
        api_key: Optional Mistral API key.

    Returns:
        The path to the generated markdown file.
    """
    parser = MistralOCRParser(api_key=api_key)
    return parser.parse_pdf(pdf_path, output_path)


def main():
    """
    Main function for command-line usage.
    """
    parser = argparse.ArgumentParser(
        description="Parse PDF documents using Mistral's OCR API"
    )
    parser.add_argument(
        "--input", "-i", required=True, help="Path to the input PDF file"
    )
    parser.add_argument("--output", "-o", help="Path to save the output markdown file")
    parser.add_argument(
        "--api-key",
        help="Mistral API key (if not provided, will use MISTRAL_API_KEY environment variable)",
    )

    args = parser.parse_args()

    try:
        parse_pdf(args.input, args.output, args.api_key)
    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
