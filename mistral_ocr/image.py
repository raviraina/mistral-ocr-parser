"""
Image processing functionality for the Mistral OCR PDF parser.
"""

import base64
import json
import io
from typing import Dict, Any
from PIL import Image


def generate_image_description(image_base64: str, client) -> Dict[str, Any]:
    """
    Generate a detailed description of an image using Mistral.
    
    Args:
        image_base64: Base64-encoded image data.
        client: Mistral client instance.
        
    Returns:
        A dictionary containing the image description and metadata.
    """
    try:
        # Decode the base64 image
        image_data = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(image_data))
        
        # Generate a description using Mistral
        response = client.chat(
            model="mistral-large-latest",
            messages=[
                {"role": "system", "content": "You are an expert at analyzing and describing images in detail. Provide a comprehensive description of the image and extract structured metadata about its content."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Describe this image in detail. Include what type of image it is (chart, graph, photograph, diagram, etc.), what it depicts, and any key elements. Also provide structured metadata about the image content."},
                    {"type": "image", "image_url": {"url": f"data:image/png;base64,{image_base64}"}}
                ]}
            ],
            response_format={"type": "json_object"}
        )
        
        # Parse the response
        result = json.loads(response.choices[0].message.content)
        
        # Ensure the result has the expected structure
        if not isinstance(result, dict):
            result = {
                "description": "An image from the document",
                "metadata": {
                    "type": "Unknown",
                    "dimensions": f"{image.width}x{image.height}"
                }
            }
        
        # Add image dimensions if not present
        if "metadata" not in result:
            result["metadata"] = {}
        
        if "dimensions" not in result["metadata"]:
            result["metadata"]["dimensions"] = f"{image.width}x{image.height}"
        
        return result
    
    except Exception as e:
        print(f"Error generating image description: {e}")
        return {
            "description": "An image from the document",
            "metadata": {
                "type": "Unknown"
            }
        } 