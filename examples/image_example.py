#!/usr/bin/env python3
"""
Image example demonstrating how to process images with Mistral OCR.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

from mistralai import Mistral

# Import the structured OCR functionality from the package
from mistral_ocr import structured_ocr, process_image_ocr

# Load environment variables from .env file
load_dotenv()


def main():
    """
    Main function demonstrating how to process an image with Mistral OCR.
    """
    # Path to the example image file
    image_path = Path("examples/example_images/receipt.png")

    # Path to save the output markdown file
    output_path = Path("examples/output/receipt_output.md")
    output_json_path = Path("examples/output/receipt_structured.json")

    # Create output directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Process the image and generate markdown
    try:
        # Get API key from environment variable
        api_key = os.getenv("MISTRAL_API_KEY")

        if not api_key:
            print("Error: MISTRAL_API_KEY environment variable not set.")
            print(
                "Please set your Mistral API key in the .env file or as an environment variable."
            )
            return 1

        # Initialize Mistral client
        client = Mistral(api_key=api_key)

        print(f"Processing image: {image_path}")

        # First, process the image with basic OCR to get markdown
        print("Step 1: Basic OCR processing...")
        ocr_response = process_image_ocr(image_path, client)

        # Extract markdown content
        if hasattr(ocr_response, "pages") and len(ocr_response.pages) > 0:
            markdown_output = ocr_response.pages[0].markdown
        elif hasattr(ocr_response, "json"):
            response_dict = json.loads(ocr_response.json())
            markdown_output = response_dict.get("markdown", "")
        else:
            markdown_output = "No markdown content available."

        # Save the markdown output
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_output)

        print(f"Basic OCR output saved to: {output_path}")

        # Print a preview of the markdown output
        preview_length = min(500, len(markdown_output))
        print(
            f"\nPreview of the markdown output:\n{'-' * 40}\n{markdown_output[:preview_length]}..."
        )

        # Now, process the image with structured OCR
        print("\nStep 2: Structured OCR processing...")
        structured_result = structured_ocr(image_path, client)

        # Save the structured output as JSON
        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(structured_result, f, indent=4)

        print(f"Structured OCR output saved to: {output_json_path}")

        # Print a preview of the structured output
        json_string = json.dumps(structured_result, indent=4)
        preview_length = min(500, len(json_string))
        print(
            f"\nPreview of the structured output:\n{'-' * 40}\n{json_string[:preview_length]}..."
        )

    except FileNotFoundError:
        print(f"Error: Image file not found: {image_path}")
        print("Please make sure the example image file exists.")
    except Exception as e:
        print(f"Error: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
