# 🔑 Simple API Key Setup (Google AI Studio)

## ✅ You're using: Google AI Studio (Simple API Key)

This is the **easiest** way to get started! No complex authentication needed.

---

## 🚀 Quick Setup (2 Steps):

### **Step 1: Get Your API Key**

1. Go to: **https://makersuite.google.com/app/apikey**
2. Click "Create API Key"
3. Copy your key (looks like: `AIzaSyD...`)

### **Step 2: Add to `.env` File**

Create a file named `.env` in your project root:

```bash
# Paste your API key here
GOOGLE_API_KEY=AIzaSyDU2GGMz54JlotAMMoBPw3-CRFC11xxLWw

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/wealthy_dashboard

# Optional
DEBUG=True
```

---

## 🧪 Test Your Setup

Run this test:

```bash
python test_simple_api.py
```

Expected output:
```
✅ API Key is set
✅ Gemini API working!
Response: Hello from Gemini!
```

---

## 🎯 That's It!

Now you can use the agent:

```bash
# Start server
uvicorn app.main:app --reload

# Test agent
python test_gemini_agent.py
```

---

## 💰 Free Tier Limits

- **15 requests per minute** (RPM)
- **1 million tokens per minute** (TPM)
- **1,500 requests per day** (RPD)

**Perfect for development and testing!**

---

## 🔄 Want to Upgrade to Vertex AI Later?

See `VERTEX_AI_SETUP.md` for:
- ✅ Better rate limits
- ✅ 60% cheaper pricing
- ✅ Enterprise features
- ✅ Production-ready

But for now, **this simple setup works great!** 🎉

---

## ⚠️ Security Note

**Never commit your `.env` file to git!**

Your `.gitignore` should include:
```
.env
*.env
```

If you accidentally expose your API key:
1. Go to https://makersuite.google.com/app/apikey
2. Delete the old key
3. Create a new one
