#!/usr/bin/env python3
"""
Run examples for the Mistral OCR package.

This script provides a simple interface to run the example scripts
from the examples directory.
"""

import os
import sys
import argparse
import importlib.util
from pathlib import Path

def list_examples():
    """List all available examples."""
    examples_dir = Path("examples")
    if not examples_dir.exists() or not examples_dir.is_dir():
        print("Error: examples directory not found.")
        return []
    
    examples = []
    for file in examples_dir.glob("*.py"):
        if file.name != "__init__.py":
            examples.append(file.stem)
    
    return sorted(examples)

def run_example(example_name):
    """Run a specific example by name."""
    example_path = Path(f"examples/{example_name}.py")
    if not example_path.exists():
        print(f"Error: Example '{example_name}' not found.")
        return False
    
    print(f"Running example: {example_name}")
    print("-" * 50)
    
    # Load and run the example module
    spec = importlib.util.spec_from_file_location(example_name, example_path)
    example_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(example_module)
    
    # Run the main function if it exists
    if hasattr(example_module, "main"):
        example_module.main()
    else:
        print(f"Warning: Example '{example_name}' does not have a main() function.")
    
    print("-" * 50)
    print(f"Example '{example_name}' completed.")
    return True

def main():
    """Main function to parse arguments and run examples."""
    parser = argparse.ArgumentParser(description="Run Mistral OCR examples")
    parser.add_argument("example", nargs="?", help="Name of the example to run (without .py extension)")
    parser.add_argument("--list", "-l", action="store_true", help="List all available examples")
    
    args = parser.parse_args()
    
    # Add the current directory to the Python path
    sys.path.insert(0, os.path.abspath("."))
    
    if args.list:
        examples = list_examples()
        if examples:
            print("Available examples:")
            for example in examples:
                print(f"  - {example}")
        else:
            print("No examples found.")
        return 0
    
    if not args.example:
        examples = list_examples()
        if not examples:
            print("No examples found.")
            return 1
        
        print("Available examples:")
        for example in examples:
            print(f"  - {example}")
        
        print("\nRun an example with: python run_examples.py <example_name>")
        return 0
    
    success = run_example(args.example)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main()) 