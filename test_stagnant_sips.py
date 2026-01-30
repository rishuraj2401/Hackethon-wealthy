#!/usr/bin/env python3
"""
Test script for Stagnant SIP Opportunities API
"""
import requests
import json

# Base URL
BASE_URL = "http://localhost:8111"

def test_stagnant_sips_all():
    """Test stagnant SIPs for all agents"""
    print("\n" + "="*80)
    print("Testing: Stagnant SIP Opportunities - All Agents")
    print("="*80)
    
    url = f"{BASE_URL}/api/opportunities/stagnant-sips"
    params = {
        "min_months": 6,
        "limit": 100
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success! Status: {response.status_code}")
        print(f"\nSummary:")
        print(f"  - Total Stagnant SIPs: {data.get('total_stagnant_sips')}")
        print(f"  - Total Clients Affected: {data.get('total_clients_affected')}")
        print(f"  - Total SIP Value: ₹{data.get('total_sip_value'):,.2f}")
        
        if data.get('opportunities'):
            print(f"\n📊 Top 10 Stagnant SIPs (Oldest First):")
            for i, opp in enumerate(data['opportunities'][:10], 1):
                print(f"\n  {i}. Client: {opp.get('user_name') or 'N/A'} (ID: {opp['user_id']})")
                print(f"     Agent: {opp.get('agent_name') or 'N/A'} (ID: {opp.get('agent_id') or 'N/A'})")
                print(f"     Scheme: {opp.get('scheme_name') or 'N/A'}")
                print(f"     Current SIP: ₹{opp['current_sip']:,.2f}")
                print(f"     Months Stagnant: {opp.get('months_stagnant')} months")
                print(f"     Created At: {opp.get('created_at')}")
                print(f"     Status: {opp.get('current_sip_status')}")
                print(f"     Step-up Configured: No (Amount: {opp.get('increment_amount') or 0}, %: {opp.get('increment_percentage') or 0})")
        
        # Save full response to file
        with open('stagnant_sips_response.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n📄 Full response saved to: stagnant_sips_response.json")
        
    else:
        print(f"\n❌ Error! Status: {response.status_code}")
        print(f"Response: {response.text}")


def test_stagnant_sips_by_agent(agent_external_id):
    """Test stagnant SIPs filtered by specific agent external ID"""
    print("\n" + "="*80)
    print(f"Testing: Stagnant SIP Opportunities - Agent {agent_external_id}")
    print("="*80)
    
    url = f"{BASE_URL}/api/opportunities/stagnant-sips"
    params = {
        "agent_external_id": agent_external_id,  # Using agent_external_id now
        "min_months": 6,
        "limit": 100
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success! Status: {response.status_code}")
        print(f"\nSummary for Agent {agent_external_id}:")
        print(f"  - Total Stagnant SIPs: {data.get('total_stagnant_sips')}")
        print(f"  - Total Clients Affected: {data.get('total_clients_affected')}")
        print(f"  - Total SIP Value: ₹{data.get('total_sip_value'):,.2f}")
        
        if data.get('opportunities'):
            print(f"\n📊 All Stagnant SIPs for this Agent:")
            for i, opp in enumerate(data['opportunities'], 1):
                print(f"\n  {i}. Client: {opp.get('user_name') or 'N/A'}")
                print(f"     Scheme: {opp.get('scheme_name') or 'N/A'}")
                print(f"     Current SIP: ₹{opp['current_sip']:,.2f}")
                print(f"     Months Stagnant: {opp.get('months_stagnant')} months")
                print(f"     Total Invested: ₹{opp.get('success_amount', 0):,.2f}")
        
        # Save to file
        filename = f"stagnant_sips_agent_{agent_external_id.replace('/', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n📄 Full response saved to: {filename}")
        
    else:
        print(f"\n❌ Error! Status: {response.status_code}")
        print(f"Response: {response.text}")


def test_stagnant_sips_different_months():
    """Test stagnant SIPs with different month thresholds"""
    print("\n" + "="*80)
    print("Testing: Stagnant SIP Opportunities - Different Month Thresholds")
    print("="*80)
    
    for months in [3, 6, 12]:
        print(f"\n--- Stagnant for {months}+ months ---")
        url = f"{BASE_URL}/api/opportunities/stagnant-sips"
        params = {
            "min_months": months,
            "limit": 10
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Total SIPs: {data.get('total_stagnant_sips')}")
            print(f"  Clients Affected: {data.get('total_clients_affected')}")
            print(f"  Total Value: ₹{data.get('total_sip_value'):,.2f}")
        else:
            print(f"  ❌ Error! Status: {response.status_code}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("Stagnant SIP Opportunities API - Test Suite")
    print("="*80)
    print("\nMake sure the API server is running on http://localhost:8111")
    print("Start it with: uvicorn app.main:app --reload --port 8111")
    
    # Test 1: All stagnant SIPs
    # test_stagnant_sips_all()
    
    # Test 2: Different month thresholds
    # test_stagnant_sips_different_months()
    
    # Test 3: Filter by specific agent external ID
    agent_external_id = "ag_YvJkGSgtTQKsYPxkTcCUCN"
    test_stagnant_sips_by_agent(agent_external_id)
    
    print("\n" + "="*80)
    print("✅ Testing Complete!")
    print("="*80 + "\n")
