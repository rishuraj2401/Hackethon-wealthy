# Conda Environment Setup Guide

## Quick Setup with Conda

### Step 1: Create Conda Environment

```bash
cd /Users/rishurajsinha/Desktop/wealthy/Hackethon

# Create conda environment from environment.yml
conda env create -f environment.yml
```

This will create a conda environment named `wealthy-dashboard` with all dependencies.

### Step 2: Activate the Environment

```bash
conda activate wealthy-dashboard
```

### Step 3: Verify Installation

```bash
# Check Python version
python --version

# Check uvicorn is installed
uvicorn --version

# Check FastAPI is available
python -c "import fastapi; print('FastAPI version:', fastapi.__version__)"
```

### Step 4: Start PostgreSQL

```bash
docker-compose up -d
```

### Step 5: Import Data

```bash
python scripts/import_data.py /Users/rishurajsinha/Downloads/query_result_2026-01-30T06_19_15.12414166Z.json
```

### Step 6: Start the API Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8111
```

Or use the startup script:
```bash
./run.sh
```

## Alternative: One-Command Setup

```bash
# Run the setup script
./setup_conda.sh

# Then activate and run
conda activate wealthy-dashboard
./run.sh
```

## Managing the Conda Environment

### Update Dependencies

If you add new packages to `environment.yml`:

```bash
# Update existing environment
conda env update -f environment.yml --prune
```

### Remove Environment

```bash
conda deactivate
conda env remove -n wealthy-dashboard
```

### List Installed Packages

```bash
conda activate wealthy-dashboard
conda list
```

### Export Current Environment

```bash
# Export with exact versions
conda env export > environment_frozen.yml

# Export without builds (more portable)
conda env export --no-builds > environment_portable.yml
```

## Troubleshooting

### Issue: "conda: command not found"

**Solution**: Install Miniconda or Anaconda

```bash
# Download Miniconda installer for macOS
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh

# Install Miniconda
bash Miniconda3-latest-MacOSX-arm64.sh

# Follow the prompts, then restart your terminal
```

### Issue: "CondaValueError: prefix already exists"

**Solution**: Remove and recreate the environment

```bash
conda env remove -n wealthy-dashboard
conda env create -f environment.yml
```

### Issue: "uvicorn: command not found" even after conda activation

**Solution**: Ensure the environment is properly activated

```bash
# Deactivate and reactivate
conda deactivate
conda activate wealthy-dashboard

# Verify uvicorn is in the PATH
which uvicorn

# Should show: /path/to/miniconda3/envs/wealthy-dashboard/bin/uvicorn
```

### Issue: Import errors when running the app

**Solution**: Ensure you're in the project directory and environment is activated

```bash
cd /Users/rishurajsinha/Desktop/wealthy/Hackethon
conda activate wealthy-dashboard
python -c "from app.main import app; print('OK')"
```

## Benefits of Conda

✅ **Isolated Environment**: Completely separate from system Python  
✅ **Cross-platform**: Works on macOS, Linux, Windows  
✅ **Package Management**: Handles both Python and non-Python dependencies  
✅ **Version Control**: Pin exact versions for reproducibility  
✅ **Easy Sharing**: Share `environment.yml` with team members  

## Running in Production

For production deployment, you can:

1. **Use Docker** (recommended):
```dockerfile
FROM continuumio/miniconda3
COPY environment.yml .
RUN conda env create -f environment.yml
SHELL ["conda", "run", "-n", "wealthy-dashboard", "/bin/bash", "-c"]
COPY . /app
WORKDIR /app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8111"]
```

2. **Export requirements.txt** from conda:
```bash
conda activate wealthy-dashboard
pip list --format=freeze > requirements.txt
```

## Quick Reference

```bash
# Create environment
conda env create -f environment.yml

# Activate environment
conda activate wealthy-dashboard

# Deactivate environment
conda deactivate

# List all environments
conda env list

# Update environment
conda env update -f environment.yml

# Remove environment
conda env remove -n wealthy-dashboard

# Export environment
conda env export > environment.yml
```

## Next Steps

Once your conda environment is set up and activated:

1. ✅ Start PostgreSQL: `docker-compose up -d`
2. ✅ Import data: `python scripts/import_data.py <json_file>`
3. ✅ Start API: `uvicorn app.main:app --reload --port 8111`
4. ✅ Visit: http://localhost:8111/docs

Happy coding! 🚀
