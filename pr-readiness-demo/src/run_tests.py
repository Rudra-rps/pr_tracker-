"""
Simple test runner - Run all tests with one command
"""

import subprocess
import sys
import os

# Change to src directory
os.chdir(os.path.dirname(__file__))

# Run the test file
sys.exit(subprocess.call([sys.executable, "test.py"]))
