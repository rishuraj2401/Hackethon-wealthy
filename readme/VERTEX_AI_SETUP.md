# 🚀 Vertex AI Setup Guide

## 📦 Step 1: Install Dependencies

```bash
pip install google-cloud-aiplatform
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

---

## 🔑 Step 2: Authentication Setup

### **Option A: Service Account Key (Recommended for Development)**

1. **Create a Service Account** in Google Cloud Console:
   - Go to: https://console.cloud.google.com/iam-admin/serviceaccounts
   - Click "Create Service Account"
   - Name: `vertex-ai-agent`
   - Grant roles:
     - ✅ Vertex AI User
     - ✅ Service Account Token Creator

2. **Download JSON Key:**
   - Click on the service account
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key" → "JSON"
   - Save the file as `vertex-ai-key.json` in your project root

3. **Set Environment Variable:**

**On macOS/Linux:**
```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/vertex-ai-key.json"
```

**On Windows:**
```cmd
set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\vertex-ai-key.json
```

**Or add to your `.env` file:**
```bash
GOOGLE_APPLICATION_CREDENTIALS=/Users/rishurajsinha/Desktop/wealthy/Hackethon/vertex-ai-key.json
VERTEX_PROJECT_ID=your-gcp-project-id
VERTEX_LOCATION=us-central1
```

---

### **Option B: Application Default Credentials (ADC)**

```bash
# Login to Google Cloud
gcloud auth application-default login

# Set your project
gcloud config set project YOUR_PROJECT_ID
```

---

## 🌍 Step 3: Get Your Project Details

### **Find Your Project ID:**

1. Go to: https://console.cloud.google.com/
2. Look at the top of the page - your project ID is shown
3. Or run:
   ```bash
   gcloud config get-value project
   ```

### **Choose Your Region:**

For **India/Asia**:
- `asia-south1` (Mumbai)
- `asia-southeast1` (Singapore)

For **US**:
- `us-central1` (Iowa)
- `us-east4` (Virginia)

For **Europe**:
- `europe-west1` (Belgium)
- `europe-west4` (Netherlands)

Full list: https://cloud.google.com/vertex-ai/docs/general/locations

---

## 📝 Step 4: Update Your `.env` File

Create/update `.env` in your project root:

```bash
# Vertex AI Configuration
VERTEX_PROJECT_ID=wealthy-dashboard-123456
VERTEX_LOCATION=asia-south1

# Service Account (if using Option A)
GOOGLE_APPLICATION_CREDENTIALS=/Users/rishurajsinha/Desktop/wealthy/Hackethon/vertex-ai-key.json

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/wealthy_dashboard

# Optional
DEBUG=True
```

---

## ✅ Step 5: Enable Vertex AI API

1. Go to: https://console.cloud.google.com/apis/library/aiplatform.googleapis.com
2. Click "Enable"
3. Wait 1-2 minutes for activation

Or via command line:
```bash
gcloud services enable aiplatform.googleapis.com
```

---

## 🧪 Step 6: Test Your Setup

Create `test_vertex_ai.py`:

```python
import vertexai
from vertexai.generative_models import GenerativeModel
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize Vertex AI
PROJECT_ID = os.getenv('VERTEX_PROJECT_ID')
LOCATION = os.getenv('VERTEX_LOCATION', 'us-central1')

print(f"Project ID: {PROJECT_ID}")
print(f"Location: {LOCATION}")

vertexai.init(project=PROJECT_ID, location=LOCATION)

# Create model
model = GenerativeModel('gemini-1.5-flash')

# Test
response = model.generate_content("Say hello in 3 words")
print(f"\n✅ Response: {response.text}")
```

Run:
```bash
python test_vertex_ai.py
```

Expected output:
```
Project ID: your-project-id
Location: asia-south1
✅ Response: Hello there, friend!
```

---

## 🚀 Step 7: Run Your Agent

```bash
# Start your FastAPI server
uvicorn app.main:app --reload

# Test the agent
python test_gemini_agent.py
```

---

## 🔧 Troubleshooting

### **Error: "Could not automatically determine credentials"**
- ✅ Check `GOOGLE_APPLICATION_CREDENTIALS` path is correct
- ✅ Or run `gcloud auth application-default login`

### **Error: "Permission denied"**
- ✅ Add "Vertex AI User" role to your service account
- ✅ Wait 5 minutes for permissions to propagate

### **Error: "API not enabled"**
- ✅ Enable Vertex AI API (see Step 5)
- ✅ Check billing is enabled on your project

### **Error: "Location not supported"**
- ✅ Use `us-central1` or check supported locations
- ✅ Gemini 1.5 Flash is available in most regions

---

## 💡 Cost Comparison

### **Vertex AI Pricing (Gemini 1.5 Flash):**
- Input: $0.000125 per 1K characters
- Output: $0.000375 per 1K characters
- **~60% cheaper than Google AI Studio for production**

### **Free Tier:**
- Pay-as-you-go (no subscription)
- First requests are extremely cheap (~$0.001 per call for your use case)

---

## 🎯 Available Models

In `agent.py`, you can use:

```python
# Fast and cheap (Recommended)
model = GenerativeModel('gemini-1.5-flash')

# More powerful
model = GenerativeModel('gemini-1.5-pro')

# Experimental (if available in your region)
model = GenerativeModel('gemini-2.0-flash-exp')
```

---

## 📚 Useful Links

- Vertex AI Console: https://console.cloud.google.com/vertex-ai
- Documentation: https://cloud.google.com/vertex-ai/docs
- Pricing: https://cloud.google.com/vertex-ai/pricing
- Model Garden: https://console.cloud.google.com/vertex-ai/model-garden

---

## ✨ Done!

Your agent is now using **Vertex AI** instead of the standard Gemini API! 🎉
