#!/usr/bin/env python3
"""
Run tests for the Mistral OCR package.

This script provides a simple interface to run the test suite
with various options.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def run_tests(verbose=False, coverage=False, test_file=None):
    """
    Run the test suite with the specified options.
    
    Args:
        verbose: Whether to run tests in verbose mode.
        coverage: Whether to generate a coverage report.
        test_file: Specific test file to run (optional).
    
    Returns:
        The exit code from the test run.
    """
    # Add the current directory to the Python path
    sys.path.insert(0, os.path.abspath("."))
    
    # Build the pytest command
    cmd = ["pytest"]
    
    if verbose:
        cmd.append("-v")
    
    if coverage:
        cmd.extend(["--cov=mistral_ocr", "--cov-report=term", "--cov-report=html"])
    
    if test_file:
        test_path = Path(test_file)
        if not test_path.exists():
            print(f"Error: Test file '{test_file}' not found.")
            return 1
        cmd.append(str(test_path))
    else:
        cmd.append("tests/")
    
    # Print the command being run
    print(f"Running: {' '.join(cmd)}")
    print("-" * 50)
    
    # Run the tests
    result = subprocess.run(cmd)
    
    # Print coverage report location if generated
    if coverage:
        print("-" * 50)
        print("Coverage report generated in htmlcov/index.html")
    
    return result.returncode

def main():
    """Main function to parse arguments and run tests."""
    parser = argparse.ArgumentParser(description="Run Mistral OCR tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Run tests in verbose mode")
    parser.add_argument("--coverage", "-c", action="store_true", help="Generate a coverage report")
    parser.add_argument("--file", "-f", help="Run a specific test file")
    
    args = parser.parse_args()
    
    return run_tests(verbose=args.verbose, coverage=args.coverage, test_file=args.file)

if __name__ == "__main__":
    sys.exit(main()) 