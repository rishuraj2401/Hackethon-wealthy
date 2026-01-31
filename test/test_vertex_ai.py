"""
Test script to verify Vertex AI setup
"""
import vertexai
from vertexai.generative_models import GenerativeModel, GenerationConfig
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_vertex_ai():
    """Test Vertex AI connection and basic generation"""
    
    print("=" * 60)
    print("🧪 TESTING VERTEX AI SETUP")
    print("=" * 60)
    
    # Get credentials from environment
    PROJECT_ID = os.getenv('VERTEX_PROJECT_ID')
    LOCATION = os.getenv('VERTEX_LOCATION', 'us-central1')
    CREDENTIALS_PATH = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    
    print(f"\n📋 Configuration:")
    print(f"   Project ID: {PROJECT_ID}")
    print(f"   Location: {LOCATION}")
    print(f"   Credentials: {CREDENTIALS_PATH}")
    
    if not PROJECT_ID:
        print("\n❌ ERROR: VERTEX_PROJECT_ID not set in .env file")
        print("   Please add: VERTEX_PROJECT_ID=your-project-id")
        return False
    
    try:
        # Initialize Vertex AI
        print(f"\n🔄 Initializing Vertex AI...")
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        print("   ✅ Vertex AI initialized successfully!")
        
        # Create model
        print(f"\n🤖 Loading Gemini model...")
        model = GenerativeModel('gemini-1.5-flash')
        print("   ✅ Model loaded!")
        
        # Test with simple prompt
        print(f"\n💬 Testing generation...")
        response = model.generate_content("Say 'Hello from Vertex AI!' in exactly 5 words")
        print(f"   Response: {response.text}")
        print("   ✅ Generation successful!")
        
        # Test with JSON output
        print(f"\n🔧 Testing JSON mode...")
        generation_config = GenerationConfig(
            temperature=0.2,
            response_mime_type="application/json"
        )
        
        json_prompt = """
        Generate a simple JSON with these fields:
        {
            "status": "success",
            "message": "Vertex AI is working",
            "timestamp": "current_time"
        }
        """
        
        response = model.generate_content(
            json_prompt,
            generation_config=generation_config
        )
        print(f"   JSON Response: {response.text}")
        print("   ✅ JSON mode working!")
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED! Vertex AI is ready to use.")
        print("=" * 60)
        print("\n💡 Next steps:")
        print("   1. Run your FastAPI server: uvicorn app.main:app --reload")
        print("   2. Test the agent: python test_gemini_agent.py")
        print("   3. Or test via API: curl http://localhost:8000/")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print(f"❌ ERROR: {str(e)}")
        print("=" * 60)
        
        print("\n🔧 Troubleshooting:")
        
        if "Could not automatically determine credentials" in str(e):
            print("   ❌ Authentication issue")
            print("   Solutions:")
            print("   1. Set GOOGLE_APPLICATION_CREDENTIALS in .env")
            print("   2. Or run: gcloud auth application-default login")
            
        elif "Permission denied" in str(e) or "403" in str(e):
            print("   ❌ Permission issue")
            print("   Solutions:")
            print("   1. Add 'Vertex AI User' role to service account")
            print("   2. Enable Vertex AI API in console")
            print("   3. Check billing is enabled")
            
        elif "not found" in str(e) or "404" in str(e):
            print("   ❌ API not enabled or project not found")
            print("   Solutions:")
            print("   1. Enable Vertex AI API:")
            print("      gcloud services enable aiplatform.googleapis.com")
            print("   2. Check VERTEX_PROJECT_ID is correct")
            
        else:
            print(f"   {str(e)}")
        
        print("\n📚 See VERTEX_AI_SETUP.md for detailed setup instructions")
        return False

if __name__ == "__main__":
    test_vertex_ai()
