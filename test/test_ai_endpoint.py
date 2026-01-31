"""
Test the AI Dashboard Insights API endpoint
"""
import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8111"
AGENT_EXTERNAL_ID = "ag_v49teQwebZsmeXzzYN2GPN"

def test_ai_dashboard_endpoint():
    """Test the AI dashboard insights endpoint"""
    
    print("=" * 80)
    print("🤖 TESTING AI DASHBOARD INSIGHTS API")
    print("=" * 80)
    
    # Build the URL
    url = f"{BASE_URL}/api/ai/dashboard-insights"
    params = {"agent_external_id": AGENT_EXTERNAL_ID,
    "limit": 3}
    
    print(f"\n📡 Calling: {url}")
    print(f"📋 Parameters: {params}")
    print("\n⏳ Fetching data and generating insights... (this may take 10-30 seconds)")
    
    try:
        # Make the request
        response = requests.get(url, params=params, timeout=160)
        response.raise_for_status()
        
        data = response.json()
        
        print("\n" + "=" * 80)
        print("✅ SUCCESS! AI Generated Insights:")
        print("=" * 80)
        
        # Display dashboard hero metrics
        if "dashboard_hero" in data:
            hero = data["dashboard_hero"]
            print(f"\n💰 Total Opportunity Value: {hero.get('formatted_value', 'N/A')}")
            print(f"📊 Executive Summary:")
            print(f"   {hero.get('executive_summary', 'N/A')}")
            
            if "opportunity_breakdown" in hero:
                breakdown = hero["opportunity_breakdown"]
                print(f"\n💡 Opportunity Breakdown:")
                print(f"   • Insurance: {breakdown.get('insurance', 'N/A')}")
                print(f"   • SIP Recovery: {breakdown.get('sip_recovery', 'N/A')}")
                print(f"   • Portfolio Rebalancing: {breakdown.get('portfolio_rebalancing', 'N/A')}")
        
        # Display top focus clients
        if "top_focus_clients" in data:
            clients = data["top_focus_clients"]
            print(f"\n🎯 Top Focus Clients: {len(clients)}")
            
            for idx, client in enumerate(clients[:5], 1):  # Show top 5
                print(f"\n   {idx}. {client.get('client_name', 'Unknown')}")
                print(f"      • Impact Value: {client.get('total_impact_value', 'N/A')}")
                print(f"      • Tags: {', '.join(client.get('tags', []))}")
                print(f"      • Hook: {client.get('pitch_hook', 'N/A')[:100]}...")
        
        # Display metadata
        if "metadata" in data:
            meta = data["metadata"]
            print(f"\n📈 Data Summary:")
            if "data_summary" in meta:
                summary = meta["data_summary"]
                
                # Handle both old and new format
                def get_count(item):
                    if isinstance(item, dict):
                        return f"{item.get('analyzed', 0)} analyzed (of {item.get('total', 0)} total)"
                    return str(item)
                
                print(f"   • Portfolio Opportunities: {get_count(summary.get('portfolio_opportunities', 0))}")
                print(f"   • Stagnant SIPs: {get_count(summary.get('stagnant_sips', 0))}")
                print(f"   • Stopped SIPs: {get_count(summary.get('stopped_sips', 0))}")
                print(f"   • Insurance Gaps: {get_count(summary.get('insurance_gaps', 0))}")
                
                if "optimization_note" in meta:
                    print(f"\n💡 {meta['optimization_note']}")
        
        # Save full response to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ai_dashboard_response_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        
        print(f"\n💾 Full response saved to: {filename}")
        print("=" * 80)
        
        return True
        
    except requests.exceptions.Timeout:
        print("\n❌ ERROR: Request timed out (>60 seconds)")
        print("   The AI agent might be taking too long to process.")
        print("   Try again or check if the Gemini API is responding.")
        return False
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API")
        print("   Make sure the server is running:")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8111")
        return False
        
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ ERROR: HTTP {e.response.status_code}")
        print(f"   {e.response.text}")
        return False
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        return False


if __name__ == "__main__":
    print("\n🚀 Starting AI Dashboard API Test...\n")
    
    # Test the endpoint
    success = test_ai_dashboard_endpoint()
    
    if success:
        print("\n✅ Test completed successfully!")
        print("\n💡 You can now integrate this endpoint into your frontend:")
        print(f"   GET {BASE_URL}/api/ai/dashboard-insights?agent_external_id={AGENT_EXTERNAL_ID}")
    else:
        print("\n❌ Test failed. Please check the errors above.")
    
    exit(0 if success else 1)
