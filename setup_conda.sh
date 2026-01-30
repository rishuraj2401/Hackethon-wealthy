#!/bin/bash

# Setup script for Wealthy Dashboard API using Conda

echo "🚀 Setting up Wealthy Partner Dashboard with Conda..."

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "❌ Error: conda is not installed"
    echo "   Please install Anaconda or Miniconda first"
    echo "   Visit: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Create conda environment
echo "📦 Creating conda environment 'wealthy-dashboard'..."
conda env create -f environment.yml

echo ""
echo "✅ Conda environment created!"
echo ""
echo "To activate the environment, run:"
echo "  conda activate wealthy-dashboard"
echo ""
echo "Then start the application with:"
echo "  ./run.sh"
