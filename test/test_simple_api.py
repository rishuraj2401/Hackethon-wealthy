"""
Simple test for Google AI API Key setup
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_key():
    """Test Google AI API key setup"""
    
    print("=" * 60)
    print("🧪 TESTING GOOGLE AI API KEY")
    print("=" * 60)
    
    # Check if API key is set
    api_key = os.getenv('GOOGLE_API_KEY')
    
    if not api_key or api_key == 'your-api-key-here':
        print("\n❌ ERROR: GOOGLE_API_KEY not set in .env file")
        print("\n📋 Steps to fix:")
        print("   1. Create a file named '.env' in your project root")
        print("   2. Add this line: GOOGLE_API_KEY=your-actual-key")
        print("   3. Get your key from: https://makersuite.google.com/app/apikey")
        print("\n📄 Example .env file:")
        print("   GOOGLE_API_KEY=AIzaSyD...")
        print("   DATABASE_URL=postgresql://...")
        return False
    
    print(f"\n✅ API Key found: {api_key[:20]}...{api_key[-10:]}")
    
    try:
        # Configure the API
        print("\n🔄 Configuring Google AI...")
        genai.configure(api_key=api_key)
        print("   ✅ Configuration successful!")
        
        # Test with simple generation
        print("\n🤖 Loading Gemini model...")
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        print("   ✅ Model loaded!")
        
        # Test generation
        print("\n💬 Testing generation...")
        response = model.generate_content("Say 'Hello from Gemini!' in exactly 4 words")
        print(f"   Response: {response.text}")
        print("   ✅ Generation successful!")
        
        # Test JSON mode
        print("\n🔧 Testing JSON output...")
        json_model = genai.GenerativeModel(
            'models/gemini-2.5-flash',
            generation_config={"response_mime_type": "application/json"}
        )
        
        json_prompt = """
        Return a JSON with:
        {
            "status": "success",
            "message": "API is working"
        }
        """
        response = json_model.generate_content(json_prompt)
        print(f"   JSON Response: {response.text}")
        print("   ✅ JSON mode working!")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED! Your API key is working.")
        print("=" * 60)
        
        print("\n💡 Next steps:")
        print("   1. Start server: uvicorn app.main:app --reload")
        print("   2. Test agent: python test_gemini_agent.py")
        print("   3. Or test via browser: http://localhost:8000")
        
        print("\n📊 Rate Limits (Free Tier):")
        print("   • 15 requests per minute")
        print("   • 1 million tokens per minute")
        print("   • 1,500 requests per day")
        print("   💡 Perfect for development!")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ ERROR: {str(e)}")
        print("=" * 60)
        
        error_str = str(e).lower()
        
        if "api key not valid" in error_str or "invalid" in error_str:
            print("\n🔑 API Key Issue:")
            print("   ❌ Your API key is invalid")
            print("\n   Solutions:")
            print("   1. Get a new key: https://makersuite.google.com/app/apikey")
            print("   2. Make sure you copied the full key")
            print("   3. Check for extra spaces in .env file")
            
        elif "quota" in error_str or "rate limit" in error_str:
            print("\n⏱️ Rate Limit Issue:")
            print("   ❌ You've hit the rate limit")
            print("\n   Solutions:")
            print("   1. Wait a few minutes and try again")
            print("   2. Upgrade to paid tier for higher limits")
            
        elif "not found" in error_str or "404" in error_str:
            print("\n🔍 Model Not Found:")
            print("   ❌ The model might not be available")
            print("\n   Solutions:")
            print("   1. Try: gemini-1.5-flash or gemini-1.5-pro")
            print("   2. Check if model is available in your region")
            
        else:
            print(f"\n💥 Unexpected error:")
            print(f"   {str(e)}")
            print("\n   Check:")
            print("   1. Internet connection")
            print("   2. API key is correct")
            print("   3. google-generativeai is installed: pip install google-generativeai")
        
        return False

if __name__ == "__main__":
    success = test_api_key()
    exit(0 if success else 1)
