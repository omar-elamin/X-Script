#!/bin/bash

# Enable error handling
set -e

# Default environment name
DEFAULT_ENV="xscript"

# Use the provided environment name or the default
if [ -z "$1" ]; then
    ENV_NAME="$DEFAULT_ENV"
else
    ENV_NAME="$1"
fi

echo "Checking conda environment: $ENV_NAME"

# Function to find conda
find_conda() {
    # Try to find conda in PATH
    if command -v conda &> /dev/null; then
        echo "Found conda in PATH"
        return 0
    fi

    # Try common conda installation paths on Mac
    local common_paths=(
        "$HOME/miniconda3/bin/conda"
        "$HOME/anaconda3/bin/conda"
        "$HOME/opt/miniconda3/bin/conda"
        "$HOME/opt/anaconda3/bin/conda"
        "/opt/miniconda3/bin/conda"
        "/opt/anaconda3/bin/conda"
    )

    for path in "${common_paths[@]}"; do
        if [ -f "$path" ]; then
            echo "Found conda at $path"
            export PATH="$(dirname "$path"):$PATH"
            return 0
        fi
    done

    echo "Could not find conda. Please make sure conda is installed and properly configured."
    return 1
}

# Find conda
find_conda || exit 1

# Check if environment exists
if ! conda env list | grep -q "^$ENV_NAME "; then
    echo "Environment $ENV_NAME does not exist. Creating it..."
    conda create -y -n "$ENV_NAME" python=3.9 || {
        echo "Failed to create environment $ENV_NAME"
        exit 1
    }
fi

# Activate the environment
# On Mac, we need to source the conda.sh script first
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$ENV_NAME" || {
    echo "Failed to activate environment $ENV_NAME"
    exit 1
}

# Install Python dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt || {
        echo "Failed to install Python dependencies"
        exit 1
    }
fi

# Check for package.json and install npm dependencies if needed
if [ -f "package.json" ]; then
    echo "Checking npm dependencies..."
    
    # Check if node_modules directory exists
    if [ ! -d "node_modules" ]; then
        echo "Installing npm dependencies..."
        npm install || {
            echo "Failed to install npm dependencies"
            exit 1
        }
    fi
fi

echo "Starting the application..."
npm start 