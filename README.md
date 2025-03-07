# Mistral OCR

A lightweight Python library for parsing PDF documents using Mistral's OCR API, extracting text content while maintaining document structure, and converting images into structured markdown sections with detailed descriptions.

[![Tests](https://github.com/raviraina/mistral-ocr-parser/actions/workflows/tests.yml/badge.svg)](https://github.com/raviraina/mistral-ocr-parser/actions/workflows/tests.yml)
[![PyPI version](https://badge.fury.io/py/mistral-ocr-parser.svg)](https://badge.fury.io/py/mistral-ocr-parser)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- PDF document parsing with Mistral OCR
- Text extraction with preserved formatting
- Image extraction with detailed descriptions
- Structured markdown output
- Support for complex document layouts
- Batch processing capabilities
- Structured OCR with schema validation
- Language detection and topic extraction

## Installation

### From PyPI

```bash
pip install mistral-ocr-parser
```

### From Source

```bash
git clone https://github.com/raviraina/mistral-ocr-parser.git
cd mistral-ocr-parser
pip install -e .
```

## Quick Start

### Set up your API key

Create a `.env` file in your project directory:

```
MISTRAL_API_KEY=your_api_key_here
```

Or set it as an environment variable:

```bash
export MISTRAL_API_KEY=your_api_key_here
```

### Basic Usage

```python
from mistral_ocr import parse_pdf

# Parse a PDF file
result = parse_pdf("path/to/your/document.pdf")

# Save the result to a markdown file
with open("output.md", "w") as f:
    f.write(result)
```

### Command Line Interface

```bash
# Process a single PDF
mistral-ocr --input document.pdf --output result.md

# Process multiple PDFs
mistral-ocr-batch --input-dir pdfs/ --output-dir outputs/
```

### Structured OCR

```python
from mistral_ocr import structured_ocr
from mistralai import Mistral

# Initialize Mistral client
client = Mistral(api_key="your_api_key_here")

# Process an image with structured OCR
result = structured_ocr("path/to/your/image.png", client)

# Access structured data
print(f"File name: {result['file_name']}")
print(f"Topics: {result['topics']}")
print(f"Languages: {result['languages']}")
print(f"OCR Contents: {result['ocr_contents']}")
```

## Running Examples

The repository includes example scripts that demonstrate how to use the library. You can run these examples using the `run_examples.py` script:

```bash
# List all available examples
python run_examples.py --list

# Run a specific example
python run_examples.py simple_example
```

Available examples:
- `simple_example`: Demonstrates basic PDF parsing
- `batch_processing`: Shows how to process multiple PDFs in batch
- `image_example`: Demonstrates processing an image with structured OCR

## Example Output

### PDF Parsing

The output is a markdown file that preserves the document structure and includes detailed descriptions of images:

```markdown
# Document Title

## Section 1

This is the text content of section 1.

![Image Description](image_placeholder.png)
*Image Description: A graph showing the relationship between X and Y variables. The graph has a positive slope indicating a direct correlation.*

**Image Metadata:**
- Type: Graph
- Dimensions: 500x300
- Content: Statistical data visualization
- Key Elements: X-axis (Time), Y-axis (Value), Trend line

## Section 2

This is the text content of section 2.
```

### Structured OCR

The structured OCR output is a JSON object with the following structure:

```json
{
    "file_name": "receipt.png",
    "topics": ["receipt", "transaction", "purchase"],
    "languages": ["English"],
    "ocr_contents": {
        "store": {
            "name": "GROCERY STORE",
            "address": "123 Main Street, Anytown, USA",
            "phone": "555-123-4567"
        },
        "date": "2023-05-15",
        "time": "14:30",
        "items": [
            {
                "name": "Milk",
                "quantity": 1,
                "price": 3.99
            },
            {
                "name": "Bread",
                "quantity": 2,
                "price": 2.49
            }
        ],
        "subtotal": 8.97,
        "tax": 0.72,
        "total": 9.69,
        "payment": {
            "method": "Credit Card",
            "card": "VISA ****1234"
        }
    }
}
```

## Advanced Usage

### Batch Processing

```python
from mistral_ocr import batch_process_pdfs

# Process multiple PDF files
output_files = batch_process_pdfs(
    input_dir="pdfs/",
    output_dir="outputs/",
    file_pattern="*.pdf"
)
```

### Custom API Key

```python
from mistral_ocr import MistralOCRParser

# Initialize the parser with a custom API key
parser = MistralOCRParser(api_key="your_api_key_here")

# Parse a PDF file
result = parser.parse_pdf("document.pdf", "output.md")
```

### Image Processing

```python
from mistral_ocr import process_image_ocr
from mistralai import Mistral

# Initialize Mistral client
client = Mistral(api_key="your_api_key_here")

# Process an image with OCR
ocr_result = process_image_ocr("image.png", client)

# Extract markdown content
markdown_content = ocr_result.pages[0].markdown
```

## Development

### Project Structure

```
mistral-ocr/
├── .github/workflows/        # GitHub CI/CD workflows
├── examples/                 # Example scripts
├── mistral_ocr/              # Main package directory
│   ├── __init__.py           # Package initialization
│   ├── parser.py             # Core parser functionality
│   ├── image.py              # Image processing functionality
│   └── utils.py              # Utility functions
├── tests/                    # Test directory
├── run_examples.py           # Script to run examples
└── run_tests.py              # Script to run tests
```

### Setup

1. Clone the repository
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

### Running Tests

You can run the test suite using the `run_tests.py` script:

```bash
# Run all tests
python run_tests.py

# Run tests with verbose output
python run_tests.py --verbose

# Run tests with coverage report
python run_tests.py --coverage

# Run a specific test file
python run_tests.py --file tests/test_parser.py
```

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

This project uses the Mistral OCR API for document processing. For more information about Mistral's OCR capabilities, visit [Mistral AI's documentation](https://docs.mistral.ai/capabilities/document/). 