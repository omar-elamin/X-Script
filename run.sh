#!/bin/bash

# Default environment name
DEFAULT_ENV="xscript"

# Use the provided environment name or the default
ENV_NAME=${1:-$DEFAULT_ENV}

echo "Activating conda environment: $ENV_NAME"

# Activate the conda environment
# Try different methods of activating conda
if command -v conda &> /dev/null; then
    # If conda is directly available
    conda activate $ENV_NAME || { echo "Failed to activate environment $ENV_NAME"; exit 1; }
elif [ -f ~/miniconda3/etc/profile.d/conda.sh ]; then
    # If conda is installed via miniconda3
    . ~/miniconda3/etc/profile.d/conda.sh
    conda activate $ENV_NAME || { echo "Failed to activate environment $ENV_NAME"; exit 1; }
elif [ -f ~/anaconda3/etc/profile.d/conda.sh ]; then
    # If conda is installed via anaconda3
    . ~/anaconda3/etc/profile.d/conda.sh
    conda activate $ENV_NAME || { echo "Failed to activate environment $ENV_NAME"; exit 1; }
else
    echo "Could not find conda. Please make sure conda is installed and properly configured."
    exit 1
fi

echo "Starting the application..."
npm start 