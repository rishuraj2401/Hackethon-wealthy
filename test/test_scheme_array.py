"""
Quick test to verify scheme_name is now an array in stagnant SIPs
"""
import requests
import json

BASE_URL = "http://localhost:8111"
AGENT_EXTERNAL_ID = "ag_v49teQwebZsmeXzzYN2GPN"

def test_stagnant_sips_scheme_array():
    """Test that scheme_name is now an array"""
    
    print("=" * 80)
    print("🧪 Testing Stagnant SIPs - Scheme Name Array Format")
    print("=" * 80)
    
    url = f"{BASE_URL}/api/opportunities/stagnant-sips"
    params = {"agent_external_id": AGENT_EXTERNAL_ID}
    
    print(f"\n📡 Calling: {url}")
    print(f"📋 Parameters: {params}\n")
    
    try:
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if 'opportunities' in data and len(data['opportunities']) > 0:
            print(f"✅ Found {len(data['opportunities'])} stagnant SIPs\n")
            
            # Check first few records
            for idx, opp in enumerate(data['opportunities'][:3], 1):
                print(f"Record {idx}:")
                print(f"  User: {opp.get('user_name', 'Unknown')}")
                print(f"  Scheme Name Type: {type(opp.get('scheme_name'))}")
                print(f"  Scheme Name Value: {opp.get('scheme_name')}")
                
                # Verify it's a list
                scheme_name = opp.get('scheme_name')
                if scheme_name is None:
                    print(f"  ⚠️  Scheme name is None (filtered out)")
                elif isinstance(scheme_name, list):
                    print(f"  ✅ Scheme name is an array with {len(scheme_name)} item(s)")
                    for i, name in enumerate(scheme_name, 1):
                        print(f"     {i}. {name}")
                else:
                    print(f"  ❌ ERROR: Scheme name is NOT an array, it's a {type(scheme_name)}")
                print()
        else:
            print("⚠️  No stagnant SIPs found")
        
        print("=" * 80)
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

if __name__ == "__main__":
    test_stagnant_sips_scheme_array()
