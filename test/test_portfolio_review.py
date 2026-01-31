#!/usr/bin/env python3
"""
Test script for Portfolio Review Opportunities API
"""
import requests
import json

# Base URL
BASE_URL = "http://localhost:8111"

def test_portfolio_review_all():
    """Test portfolio review for all agents"""
    print("\n" + "="*80)
    print("Testing: Portfolio Review - All Clients")
    print("="*80)
    
    url = f"{BASE_URL}/api/portfolio/review-opportunities"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success! Status: {response.status_code}")
        print(f"\nSummary:")
        print(f"  - Total Clients: {data.get('total_clients')}")
        print(f"  - Total Underperforming Schemes: {data.get('total_underperforming_schemes')}")
        print(f"  - Total Value Underperforming: ₹{data.get('total_value_underperforming'):,.2f}")
        
        if data.get('clients'):
            print(f"\n📊 Top 3 Clients by Underperforming Value:")
            for i, client in enumerate(data['clients'][:3], 1):
                print(f"\n  {i}. {client['client_name']} (ID: {client['user_id']})")
                print(f"     Agent: {client['agent_name']} ({client['agent_external_id']})")
                print(f"     Underperforming Schemes: {client['number_of_underperforming_schemes']}")
                print(f"     Total Value: ₹{client['total_value_underperforming']:,.2f}")
                
                if client.get('underperforming_schemes'):
                    print(f"\n     Top Underperforming Schemes:")
                    for j, scheme in enumerate(client['underperforming_schemes'][:3], 1):
                        print(f"       {j}. {scheme['scheme_name']}")
                        print(f"          WPC: {scheme['wpc']}")
                        print(f"          Live XIRR: {scheme['live_xirr']}% | Benchmark: {scheme['benchmark_xirr']}%")
                        print(f"          Underperformance: {scheme['xirr_underperformance']}%")
                        print(f"          Current Value: ₹{scheme['current_value']:,.2f}")
        
        # Save full response to file
        with open('portfolio_review_response.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n📄 Full response saved to: portfolio_review_response.json")
        
    else:
        print(f"\n❌ Error! Status: {response.status_code}")
        print(f"Response: {response.text}")


def test_portfolio_review_by_agent(agent_external_id):
    """Test portfolio review filtered by specific agent"""
    print("\n" + "="*80)
    print(f"Testing: Portfolio Review - Agent {agent_external_id}")
    print("="*80)
    
    url = f"{BASE_URL}/api/portfolio/review-opportunities"
    params = {"agent_external_id": agent_external_id}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success! Status: {response.status_code}")
        print(f"\nSummary for Agent {agent_external_id}:")
        print(f"  - Total Clients: {data.get('total_clients')}")
        print(f"  - Total Underperforming Schemes: {data.get('total_underperforming_schemes')}")
        print(f"  - Total Value Underperforming: ₹{data.get('total_value_underperforming'):,.2f}")
        
        if data.get('clients'):
            print(f"\n📊 All Clients:")
            for i, client in enumerate(data['clients'], 1):
                print(f"\n  {i}. {client['client_name']} (ID: {client['user_id']})")
                print(f"     Underperforming Schemes: {client['number_of_underperforming_schemes']}")
                print(f"     Total Value: ₹{client['total_value_underperforming']:,.2f}")
        
        # Save to file
        filename = f"portfolio_review_agent_{agent_external_id}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n📄 Full response saved to: {filename}")
        
    else:
        print(f"\n❌ Error! Status: {response.status_code}")
        print(f"Response: {response.text}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("Portfolio Review Opportunities API - Test Suite")
    print("="*80)
    print("\nMake sure the API server is running on http://localhost:8111")
    print("Start it with: uvicorn app.main:app --reload --port 8111")
    
    # Test 1: All clients
    # test_portfolio_review_all()
    
    # Test 2: Filter by specific agent (uncomment and add agent ID)
    agent_id = "ag_DBpVTiu6Z3iQdBXZ8XiMDE"
    test_portfolio_review_by_agent(agent_id)
    
    print("\n" + "="*80)
    print("✅ Testing Complete!")
    print("="*80 + "\n")
