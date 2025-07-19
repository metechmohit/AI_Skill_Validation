#!/usr/bin/env bash
# exit on error
set -o errexit

# Install the python dependencies
pip install -r requirements.txt

# NOTE: We don't need to run migrations or other setup for this simple app
echo "Build complete."
