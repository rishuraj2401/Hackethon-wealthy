#!/usr/bin/env python3
"""
Simple test to verify Gemini API is working
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

print("\n" + "="*60)
print("🧪 GEMINI API - Hello Test")
print("="*60 + "\n")

# Load environment
# load_dotenv()
# api_key = os.getenv('GOOGLE_API_KEY')
api_key="AIzaSyA44KTejygzE3PCYhvXEe_2ZUJ0ibd38Hg"
# genai.configure(api_key=GOOGLE_API_KEY)
print("1. Checking API Key...")
if api_key:
    print(f"   ✅ API Key found: {api_key[:20]}...{api_key[-10:]}")
else:
    print("   ❌ No API key found in .env file!")
    print("   Add this to .env file:")
    print("   GOOGLE_API_KEY=your_api_key_here")
    exit(1)

print("\n2. Configuring Gemini...")
try:
    genai.configure(api_key=api_key)
    print("   ✅ Gemini configured")
except Exception as e:
    print(f"   ❌ Configuration failed: {e}")
    exit(1)

print("\n3. Creating model...")
try:
    model = genai.GenerativeModel('gemini-2.5-flash')
    print("   ✅ Model created")
except Exception as e:
    print(f"   ❌ Model creation failed: {e}")
    exit(1)

print("\n4. Sending test message...")
try:
    response = model.generate_content("Say hello and tell me you're working!")
    print(f"   ✅ Response received!\n")
    print("="*60)
    print("🤖 GEMINI SAYS:")
    print("="*60)
    print(response.text)
    print("="*60)
except Exception as e:
    print(f"   ❌ Request failed: {e}")
    exit(1)

print("\n✅ SUCCESS! Gemini API is working!\n")