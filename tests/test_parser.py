#!/usr/bin/env python3
"""
Test cases for the Mistral OCR PDF parser.
"""

import os
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from mistral_ocr import MistralOCRParser, parse_pdf


class TestMistralOCRParser(unittest.TestCase):
    """
    Test cases for the Mistral OCR PDF parser.
    """

    def setUp(self):
        """
        Set up test environment.
        """
        # Use a dummy API key for tests
        self.api_key = "test_api_key"
        self.test_pdf_path = Path("tests/data/test.pdf")
        self.test_output_path = Path("tests/data/test_output.md")

        # Create test data directory if it doesn't exist
        Path("tests/data").mkdir(parents=True, exist_ok=True)

        # Create a mock PDF file if it doesn't exist
        if not self.test_pdf_path.exists():
            with open(self.test_pdf_path, "wb") as f:
                f.write(b"%PDF-1.5\n%Test PDF file for testing")

    def tearDown(self):
        """
        Clean up test environment.
        """
        # Remove test files
        if self.test_pdf_path.exists():
            self.test_pdf_path.unlink()

        if self.test_output_path.exists():
            self.test_output_path.unlink()

    @patch("mistral_ocr.parser.Mistral")
    def test_parser_initialization(self, mock_mistral):
        """
        Test parser initialization.
        """
        parser = MistralOCRParser(api_key=self.api_key)
        self.assertEqual(parser.api_key, self.api_key)
        self.assertIsNotNone(parser.client)
        mock_mistral.assert_called_once_with(api_key=self.api_key)

    @patch("mistral_ocr.parser.Mistral")
    def test_parser_initialization_with_env_var(self, mock_mistral):
        """
        Test parser initialization with environment variable.
        """
        with patch.dict(os.environ, {"MISTRAL_API_KEY": "env_api_key"}):
            parser = MistralOCRParser()
            self.assertEqual(parser.api_key, "env_api_key")
            mock_mistral.assert_called_once_with(api_key="env_api_key")

    def test_parser_initialization_without_api_key(self):
        """
        Test parser initialization without API key.
        """
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                MistralOCRParser()

    @patch("mistral_ocr.parser.Mistral")
    def test_upload_file(self, mock_mistral):
        """
        Test file upload.
        """
        # Set up mock
        mock_client = MagicMock()
        mock_mistral.return_value = mock_client
        mock_upload_response = MagicMock()
        mock_client.files.upload.return_value = mock_upload_response

        # Initialize parser
        parser = MistralOCRParser(api_key=self.api_key)

        # Call upload_file
        result = parser._upload_file(self.test_pdf_path)

        # Verify
        mock_client.files.upload.assert_called_once()
        self.assertEqual(result, mock_upload_response)

    @patch("mistral_ocr.parser.Mistral")
    def test_get_signed_url(self, mock_mistral):
        """
        Test getting signed URL.
        """
        # Set up mock
        mock_client = MagicMock()
        mock_mistral.return_value = mock_client
        mock_signed_url = MagicMock()
        mock_client.files.get_signed_url.return_value = mock_signed_url

        # Initialize parser
        parser = MistralOCRParser(api_key=self.api_key)

        # Call get_signed_url
        result = parser._get_signed_url("test_file_id")

        # Verify
        mock_client.files.get_signed_url.assert_called_once_with(
            file_id="test_file_id", expiry=1
        )
        self.assertEqual(result, mock_signed_url)

    @patch("mistral_ocr.parser.Mistral")
    def test_process_ocr(self, mock_mistral):
        """
        Test OCR processing.
        """
        # Set up mock
        mock_client = MagicMock()
        mock_mistral.return_value = mock_client
        mock_ocr_response = MagicMock()
        mock_client.ocr.process.return_value = mock_ocr_response

        # Initialize parser
        parser = MistralOCRParser(api_key=self.api_key)

        # Call process_ocr
        result = parser._process_ocr("test_document_url")

        # Verify
        mock_client.ocr.process.assert_called_once()
        self.assertEqual(result, mock_ocr_response)

    @patch("mistral_ocr.parser.MistralOCRParser")
    def test_parse_pdf_function(self, mock_parser_class):
        """
        Test parse_pdf function.
        """
        # Set up mock
        mock_parser = MagicMock()
        mock_parser_class.return_value = mock_parser
        mock_parser.parse_pdf.return_value = "Test markdown output"

        # Call parse_pdf
        result = parse_pdf(self.test_pdf_path, self.test_output_path, self.api_key)

        # Verify
        mock_parser_class.assert_called_once_with(api_key=self.api_key)
        mock_parser.parse_pdf.assert_called_once_with(
            self.test_pdf_path, self.test_output_path
        )
        self.assertEqual(result, "Test markdown output")


if __name__ == "__main__":
    unittest.main()
