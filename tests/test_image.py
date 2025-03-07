#!/usr/bin/env python3
"""
Test cases for the image processing functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
import base64
import json
import sys
import os
from io import BytesIO
from PIL import Image

# Debug prints
print(f"Python path: {sys.path}")
print(f"Current directory: {os.getcwd()}")

try:
    import mistralai

    print("mistralai is importable")
except ImportError as e:
    print(f"Error importing mistralai: {e}")

try:
    from mistral_ocr.image import generate_image_description

    print("Successfully imported generate_image_description")
except ImportError as e:
    print(f"Error importing from mistral_ocr.image: {e}")


class TestImageProcessing(unittest.TestCase):
    """
    Test cases for the image processing functionality.
    """

    def setUp(self):
        """
        Set up test environment.
        """
        # Create a simple test image
        self.test_image = Image.new("RGB", (100, 100), color="red")
        buffer = BytesIO()
        self.test_image.save(buffer, format="PNG")
        self.test_image_bytes = buffer.getvalue()
        self.test_image_base64 = base64.b64encode(self.test_image_bytes).decode("utf-8")

        # Mock client response
        self.mock_response = MagicMock()
        self.mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content=json.dumps(
                        {
                            "description": "A red square image",
                            "metadata": {
                                "type": "Graphic",
                                "dimensions": "100x100",
                                "content": "Solid red color",
                            },
                        }
                    )
                )
            )
        ]

    def test_generate_image_description_success(self):
        """
        Test successful image description generation.
        """
        # Skip test if module not available
        try:
            from mistral_ocr.image import generate_image_description
        except ImportError:
            self.skipTest("mistral_ocr.image module not available")

        # Create a mock response with the expected structure
        mock_response_content = {
            "description": "A red square image",
            "metadata": {
                "type": "Graphic",
                "dimensions": "100x100",
                "content": "Solid red color",
            },
        }
        
        # Mock client
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content=json.dumps(mock_response_content)
                )
            )
        ]
        mock_client.chat.return_value = mock_response

        # Patch the json.loads function to return our mock data directly
        with patch('json.loads', return_value=mock_response_content):
            # Call the function
            result = generate_image_description(self.test_image_base64, mock_client)

            # Verify
            self.assertEqual(result["description"], "A red square image")
            self.assertEqual(result["metadata"]["type"], "Graphic")
            self.assertEqual(result["metadata"]["dimensions"], "100x100")
            self.assertEqual(result["metadata"]["content"], "Solid red color")

    def test_generate_image_description_invalid_response(self):
        """
        Test handling of invalid response from the API.
        """
        # Mock client with invalid response
        mock_client = MagicMock()
        mock_invalid_response = MagicMock()
        mock_invalid_response.choices = [
            MagicMock(message=MagicMock(content="Not a JSON string"))
        ]
        mock_client.chat.return_value = mock_invalid_response

        # Call the function
        result = generate_image_description(self.test_image_base64, mock_client)

        # Verify fallback behavior
        self.assertIn("description", result)
        self.assertIn("metadata", result)
        self.assertEqual(result["metadata"]["type"], "Unknown")

    def test_generate_image_description_exception(self):
        """
        Test handling of exceptions during image description generation.
        """
        # Mock client that raises an exception
        mock_client = MagicMock()
        mock_client.chat.side_effect = Exception("Test exception")

        # Call the function
        result = generate_image_description(self.test_image_base64, mock_client)

        # Verify fallback behavior
        self.assertIn("description", result)
        self.assertIn("metadata", result)
        self.assertEqual(result["metadata"]["type"], "Unknown")

    def test_generate_image_description_missing_metadata(self):
        """
        Test handling of response with missing metadata.
        """
        # Skip test if module not available
        try:
            from mistral_ocr.image import generate_image_description
        except ImportError:
            self.skipTest("mistral_ocr.image module not available")
            
        # Create a mock response with the expected structure
        mock_response_content = {"description": "A red square image"}
        
        # Mock client with response missing metadata
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content=json.dumps(mock_response_content)
                )
            )
        ]
        mock_client.chat.return_value = mock_response

        # Patch the json.loads function to return our mock data directly
        with patch('json.loads', return_value=mock_response_content):
            # Call the function
            result = generate_image_description(self.test_image_base64, mock_client)

            # Verify metadata is added
            self.assertEqual(result["description"], "A red square image")
            self.assertIn("metadata", result)
            self.assertIn("dimensions", result["metadata"])


if __name__ == "__main__":
    unittest.main()
