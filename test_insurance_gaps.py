#!/usr/bin/env python3
"""
Test script for Insurance Coverage Gap Opportunities API
"""
import requests
import json

# Base URL
BASE_URL = "http://localhost:8111"

def test_insurance_gaps_all():
    """Test insurance gaps for all agents"""
    print("\n" + "="*80)
    print("Testing: Insurance Coverage Gap Opportunities - All Agents")
    print("="*80)
    
    url = f"{BASE_URL}/api/insurance/opportunities/coverage-gaps"
    params = {
        "min_mf_value": 500000,
        "min_age": 30,
        "limit": 100
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success! Status: {response.status_code}")
        print(f"\nSummary:")
        print(f"  - Total Opportunities: {data.get('total_opportunities')}")
        print(f"  - No Insurance: {data.get('no_insurance_count')} clients")
        print(f"  - Low Coverage: {data.get('low_coverage_count')} clients")
        print(f"  - Total Opportunity Value: ₹{data.get('total_opportunity_value'):,.2f}")
        print(f"  - Total MF Value at Risk: ₹{data.get('total_mf_value_at_risk'):,.2f}")
        print(f"  - Average Age: {data.get('average_age')} years")
        
        if data.get('opportunities'):
            print(f"\n📊 Top 10 Highest Opportunity Value:")
            for i, opp in enumerate(data['opportunities'][:10], 1):
                status_emoji = "🚫" if opp['insurance_status'] == 'NO_INSURANCE' else "⚠️"
                print(f"\n  {i}. {status_emoji} Client: {opp.get('user_name') or 'N/A'} (ID: {opp['user_id']})")
                print(f"     Agent: {opp.get('agent_name') or 'N/A'} ({opp.get('agent_external_id') or 'N/A'})")
                print(f"     Age: {opp.get('age')} years")
                print(f"     MF Portfolio Value: ₹{opp.get('mf_current_value', 0):,.2f}")
                print(f"     Current Premium: ₹{opp['total_premium']:,.2f}")
                print(f"     Expected Premium: ₹{opp['expected_premium']:,.2f}")
                print(f"     Coverage: {opp.get('coverage_percentage', 0):.1f}%")
                print(f"     Status: {opp['insurance_status']}")
                print(f"     💰 Opportunity Value: ₹{opp['premium_opportunity_value']:,.2f}")
        
        # Save full response to file
        with open('insurance_gaps_response.json', 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n📄 Full response saved to: insurance_gaps_response.json")
        
    else:
        print(f"\n❌ Error! Status: {response.status_code}")
        print(f"Response: {response.text}")


def test_insurance_gaps_by_agent(agent_external_id):
    """Test insurance gaps filtered by specific agent"""
    print("\n" + "="*80)
    print(f"Testing: Insurance Coverage Gaps - Agent {agent_external_id}")
    print("="*80)
    
    url = f"{BASE_URL}/api/insurance/opportunities/coverage-gaps"
    params = {
        "agent_external_id": agent_external_id,
        "min_mf_value": 500000,
        "min_age": 30,
        "limit": 100
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n✅ Success! Status: {response.status_code}")
        print(f"\nSummary for Agent {agent_external_id}:")
        print(f"  - Total Opportunities: {data.get('total_opportunities')}")
        print(f"  - No Insurance: {data.get('no_insurance_count')}")
        print(f"  - Low Coverage: {data.get('low_coverage_count')}")
        print(f"  - Total Opportunity: ₹{data.get('total_opportunity_value'):,.2f}")
        print(f"  - MF Value at Risk: ₹{data.get('total_mf_value_at_risk'):,.2f}")
        
        if data.get('opportunities'):
            print(f"\n📊 All Opportunities for this Agent:")
            for i, opp in enumerate(data['opportunities'], 1):
                status = "NO INSURANCE" if opp['insurance_status'] == 'NO_INSURANCE' else "LOW COVERAGE"
                print(f"\n  {i}. {opp.get('user_name') or 'N/A'} - {status}")
                print(f"     Age: {opp.get('age')} | MF: ₹{opp.get('mf_current_value', 0):,.0f}")
                print(f"     Opportunity: ₹{opp['premium_opportunity_value']:,.2f}")
        
        # Save to file
        filename = f"insurance_gaps_agent_{agent_external_id.replace('/', '_')}.json"
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n📄 Full response saved to: {filename}")
        
    else:
        print(f"\n❌ Error! Status: {response.status_code}")
        print(f"Response: {response.text}")


def test_insurance_gaps_different_thresholds():
    """Test with different MF value thresholds"""
    print("\n" + "="*80)
    print("Testing: Insurance Coverage Gaps - Different MF Thresholds")
    print("="*80)
    
    thresholds = [
        {"mf_value": 500000, "label": "₹5 Lakhs+"},
        {"mf_value": 1000000, "label": "₹10 Lakhs+"},
        {"mf_value": 2000000, "label": "₹20 Lakhs+"},
    ]
    
    for config in thresholds:
        print(f"\n--- {config['label']} MF Portfolio ---")
        url = f"{BASE_URL}/api/insurance/opportunities/coverage-gaps"
        params = {
            "min_mf_value": config["mf_value"],
            "min_age": 30,
            "limit": 10
        }
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  Total Opportunities: {data.get('total_opportunities')}")
            print(f"  No Insurance: {data.get('no_insurance_count')}")
            print(f"  Low Coverage: {data.get('low_coverage_count')}")
            print(f"  Opportunity Value: ₹{data.get('total_opportunity_value'):,.2f}")
            print(f"  MF at Risk: ₹{data.get('total_mf_value_at_risk'):,.2f}")
        else:
            print(f"  ❌ Error! Status: {response.status_code}")


if __name__ == "__main__":
    print("\n" + "="*80)
    print("Insurance Coverage Gap Opportunities API - Test Suite")
    print("="*80)
    print("\nMake sure the API server is running on http://localhost:8111")
    print("Start it with: uvicorn app.main:app --reload --port 8111")
    
    # Test 1: All insurance gaps
    # test_insurance_gaps_all()
    
    # Test 2: Different MF thresholds
    # test_insurance_gaps_different_thresholds()
    
    # Test 3: Filter by specific agent (uncomment and add agent external ID)
    agent_external_id = "ag_orcFbFRQDJ9aLUNAfpW7K3"
    test_insurance_gaps_by_agent(agent_external_id)
    
    print("\n" + "="*80)
    print("✅ Testing Complete!")
    print("="*80 + "\n")
