#!/usr/bin/env python3
"""
Test cases for the image processing functionality.
"""

import unittest
from unittest.mock import patch, MagicMock
import base64
import json
from io import BytesIO
from PIL import Image

from mistral_ocr.image import generate_image_description


class TestImageProcessing(unittest.TestCase):
    """
    Test cases for the image processing functionality.
    """
    
    def setUp(self):
        """
        Set up test environment.
        """
        # Create a simple test image
        self.test_image = Image.new('RGB', (100, 100), color='red')
        buffer = BytesIO()
        self.test_image.save(buffer, format="PNG")
        self.test_image_bytes = buffer.getvalue()
        self.test_image_base64 = base64.b64encode(self.test_image_bytes).decode('utf-8')
        
        # Mock client response
        self.mock_response = MagicMock()
        self.mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content=json.dumps({
                        "description": "A red square image",
                        "metadata": {
                            "type": "Graphic",
                            "dimensions": "100x100",
                            "content": "Solid red color"
                        }
                    })
                )
            )
        ]
    
    def test_generate_image_description_success(self):
        """
        Test successful image description generation.
        """
        # Mock client
        mock_client = MagicMock()
        mock_client.chat.return_value = self.mock_response
        
        # Call the function
        result = generate_image_description(self.test_image_base64, mock_client)
        
        # Verify
        mock_client.chat.assert_called_once()
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
            MagicMock(
                message=MagicMock(
                    content="Not a JSON string"
                )
            )
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
        # Mock client with response missing metadata
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [
            MagicMock(
                message=MagicMock(
                    content=json.dumps({
                        "description": "A red square image"
                    })
                )
            )
        ]
        mock_client.chat.return_value = mock_response
        
        # Call the function
        result = generate_image_description(self.test_image_base64, mock_client)
        
        # Verify metadata is added
        self.assertEqual(result["description"], "A red square image")
        self.assertIn("metadata", result)
        self.assertIn("dimensions", result["metadata"])


if __name__ == "__main__":
    unittest.main() 