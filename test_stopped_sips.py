#!/usr/bin/env python3
"""
Test script for Stopped SIP Opportunities API
"""
import requests
import json

# Base URL
BASE_URL = "http://localhost:8111"

def test_stopped_sips_all():
    """Test stopped SIPs for all agents"""
    print("\n" + "="*80)
    print("Testing: Stopped SIP Opportunities - All Agents")
    print("="*80)
    
    url = f"{BASE_URL}/api/opportunities/stopped-sips"
    params = {
        "min_success_count": 3,
        "min_inactive_months": 2,
        "limit": 100
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success! Status: {response.status_code}")
        print(f"\nSummary:")
        print(f"  - Total Clients with Stopped SIPs: {data.get('total_stopped_clients')}")
        print(f"  - Total Active SIPs Affected: {data.get('total_active_sips_affected')}")
        print(f"  - Total Lifetime Investment: ₹{data.get('total_lifetime_investment'):,.2f}")
        print(f"  - Average Days Inactive: {data.get('average_days_inactive')} days")
        
        if data.get('opportunities'):
            print(f"\n📊 Top 10 Most Critical Cases (Longest Inactive):")
            for i, opp in enumerate(data['opportunities'][:10], 1):
                print(f"\n  {i}. Client: {opp.get('user_name') or 'N/A'} (ID: {opp['user_id']})")
                print(f"     Agent: {opp.get('agent_name') or 'N/A'} ({opp.get('agent_external_id') or 'N/A'})")
                print(f"     Active SIPs: {opp['active_sips']} / {opp['total_sips']} total")
                print(f"     Past Successes: {opp['max_success_count']} transactions")
                print(f"     Lifetime Investment: ₹{opp.get('lifetime_success_amount', 0):,.2f}")
                print(f"     Last Success: {opp.get('last_success_date')}")
                print(f"     Days Inactive: {opp.get('days_since_any_success')} days ({opp.get('months_since_success')} months)")
                print(f"     ⚠️  Status: Payment stopped for {opp.get('months_since_success')} months!")
        
        # Save full response to file
        with open('stopped_sips_response.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n📄 Full response saved to: stopped_sips_response.json")
        
    else:
        print(f"\n❌ Error! Status: {response.status_code}")
        print(f"Response: {response.text}")


def test_stopped_sips_by_agent(agent_external_id):
    """Test stopped SIPs filtered by specific agent"""
    print("\n" + "="*80)
    print(f"Testing: Stopped SIP Opportunities - Agent {agent_external_id}")
    print("="*80)
    
    url = f"{BASE_URL}/api/opportunities/stopped-sips"
    params = {
        "agent_external_id": agent_external_id,
        "min_success_count": 3,
        "min_inactive_months": 2,
        "limit": 100
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success! Status: {response.status_code}")
        print(f"\nSummary for Agent {agent_external_id}:")
        print(f"  - Total Clients: {data.get('total_stopped_clients')}")
        print(f"  - Active SIPs Affected: {data.get('total_active_sips_affected')}")
        print(f"  - Total Lifetime Investment: ₹{data.get('total_lifetime_investment'):,.2f}")
        print(f"  - Average Days Inactive: {data.get('average_days_inactive')} days")
        
        if data.get('opportunities'):
            print(f"\n📊 All Stopped SIPs for this Agent:")
            for i, opp in enumerate(data['opportunities'], 1):
                print(f"\n  {i}. Client: {opp.get('user_name') or 'N/A'}")
                print(f"     Active SIPs: {opp['active_sips']}")
                print(f"     Lifetime: ₹{opp.get('lifetime_success_amount', 0):,.2f}")
                print(f"     Inactive: {opp.get('months_since_success')} months")
        
        # Save to file
        filename = f"stopped_sips_agent_{agent_external_id.replace('/', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n📄 Full response saved to: {filename}")
        
    else:
        print(f"\n❌ Error! Status: {response.status_code}")
        print(f"Response: {response.text}")


def test_stopped_sips_different_thresholds():
    """Test stopped SIPs with different threshold configurations"""
    print("\n" + "="*80)
    print("Testing: Stopped SIP Opportunities - Different Thresholds")
    print("="*80)
    
    configs = [
        {"min_success_count": 3, "min_inactive_months": 1, "label": "1+ month inactive (3+ successes)"},
        {"min_success_count": 3, "min_inactive_months": 2, "label": "2+ months inactive (3+ successes)"},
        {"min_success_count": 5, "min_inactive_months": 3, "label": "3+ months inactive (5+ successes)"},
    ]
    
    for config in configs:
        print(f"\n--- {config['label']} ---")
        url = f"{BASE_URL}/api/opportunities/stopped-sips"
        params = {
            "min_success_count": config["min_success_count"],
            "min_inactive_months": config["min_inactive_months"],
            "limit": 10
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Clients Affected: {data.get('total_stopped_clients')}")
            print(f"  Active SIPs: {data.get('total_active_sips_affected')}")
            print(f"  Lifetime Investment: ₹{data.get('total_lifetime_investment'):,.2f}")
            print(f"  Avg Days Inactive: {data.get('average_days_inactive')} days")
        else:
            print(f"  ❌ Error! Status: {response.status_code}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("Stopped SIP Opportunities API - Test Suite")
    print("="*80)
    print("\nMake sure the API server is running on http://localhost:8111")
    print("Start it with: uvicorn app.main:app --reload --port 8111")
    
    # Test 1: All stopped SIPs
    test_stopped_sips_all()
    
    # Test 2: Different thresholds
    test_stopped_sips_different_thresholds()
    
    # Test 3: Filter by specific agent (uncomment and add agent external ID)
    # Example: agent_external_id = "ag_DBpVTiu6Z3iQdBXZ8XiMDE"
    # test_stopped_sips_by_agent(agent_external_id)
    
    print("\n" + "="*80)
    print("✅ Testing Complete!")
    print("="*80 + "\n")
