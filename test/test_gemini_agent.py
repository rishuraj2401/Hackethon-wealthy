#!/usr/bin/env python3
"""
Test script for Gemini Wealth Intelligence Agent
Fetches data from your APIs and tests the agent
"""
import requests
import json
from agent import generate_dashboard_insight

BASE_URL = "http://localhost:8111"

def fetch_api_data(agent_external_id=None):
    """Fetch data from all 4 opportunity APIs"""
    
    print("📊 Fetching data from APIs...")
    
    # 1. Portfolio Review Opportunities
    print("  - Portfolio Review Data...")
    portfolio_url = f"{BASE_URL}/api/portfolio/review-opportunities"
    portfolio_params = {}
    if agent_external_id:
        portfolio_params['agent_external_id'] = agent_external_id
    
    portfolio_response = requests.get(portfolio_url, params=portfolio_params)
    portfolio_data = portfolio_response.json() if portfolio_response.status_code == 200 else {}
    
    # 2. Stagnant SIPs
    print("  - Stagnant SIP Data...")
    stagnant_url = f"{BASE_URL}/api/opportunities/stagnant-sips"
    stagnant_params = {"min_months": 6, "limit": 2}
    if agent_external_id:
        stagnant_params['agent_external_id'] = agent_external_id
    
    stagnant_response = requests.get(stagnant_url, params=stagnant_params)
    stagnant_data = stagnant_response.json() if stagnant_response.status_code == 200 else {}
    
    # 3. Stopped SIPs
    print("  - Stopped SIP Data...")
    stopped_url = f"{BASE_URL}/api/opportunities/stopped-sips"
    stopped_params = {"min_success_count": 3, "min_inactive_months": 2, "limit": 2}
    if agent_external_id:
        stopped_params['agent_external_id'] = agent_external_id
    
    stopped_response = requests.get(stopped_url, params=stopped_params)
    stopped_data = stopped_response.json() if stopped_response.status_code == 200 else {}
    
    # 4. Insurance Gaps
    print("  - Insurance Gap Data...")
    insurance_url = f"{BASE_URL}/api/insurance/opportunities/coverage-gaps"
    insurance_params = {"min_mf_value": 500000, "limit": 2}
    if agent_external_id:
        insurance_params['agent_external_id'] = agent_external_id
    
    insurance_response = requests.get(insurance_url, params=insurance_params)
    insurance_data = insurance_response.json() if insurance_response.status_code == 200 else {}
    
    print("✅ Data fetched successfully!\n")
    return {
        'portfolio': portfolio_data,
        'stagnant': stagnant_data,
        'stopped': stopped_data,
        'insurance': insurance_data
    }


def test_agent_basic():
    """Test agent with all data (no agent filter)"""
    print("\n" + "="*80)
    print("TEST 1: Gemini Agent - All Clients Analysis")
    print("="*80 + "\n")
    
    # Fetch data
    data = fetch_api_data()
    print(data)
    return
    # Show data summary
    print("📈 Data Summary:")
    print(f"  - Portfolio Opportunities: {data['portfolio'].get('total_clients', 0)} clients")
    print(f"  - Stagnant SIPs: {data['stagnant'].get('total_stagnant_sips', 0)} SIPs")
    print(f"  - Stopped SIPs: {data['stopped'].get('total_stopped_clients', 0)} clients")
    print(f"  - Insurance Gaps: {data['insurance'].get('total_opportunities', 0)} opportunities")
    print("\n🤖 Calling Gemini Agent...\n")
    
    # Call agent
    result = generate_dashboard_insight(
        portfolio_data=data['portfolio'],
        stagnant_data=data['stagnant'],
        stopped_data=data['stopped'],
        insurance_data=data['insurance']
    )
    
    # Display results
    print("="*80)
    print("🎯 GEMINI AGENT OUTPUT")
    print("="*80)
    
    # Hero Dashboard
    hero = result.get('dashboard_hero', {})
    print(f"\n💰 Total Opportunity Value: {hero.get('formatted_value', 'N/A')}")
    print(f"\n📊 Executive Summary:")
    print(f"   {hero.get('executive_summary', 'N/A')}")
    
    breakdown = hero.get('opportunity_breakdown', {})
    print(f"\n💼 Breakdown:")
    print(f"   - Insurance: {breakdown.get('insurance', 'N/A')}")
    print(f"   - SIP Recovery: {breakdown.get('sip_recovery', 'N/A')}")
    print(f"   - Portfolio Rebalancing: {breakdown.get('portfolio_rebalancing', 'N/A')}")
    
    # Top Focus Clients
    focus_clients = result.get('top_focus_clients', [])
    print(f"\n🎯 Top {len(focus_clients)} Focus Clients:")
    
    for i, client in enumerate(focus_clients, 1):
        print(f"\n  {i}. {client.get('client_name', 'Unknown')} (ID: {client.get('user_id', 'N/A')})")
        print(f"     💰 Impact: {client.get('total_impact_value', 'N/A')}")
        print(f"     🏷️  Tags: {', '.join(client.get('tags', []))}")
        print(f"     📝 Pitch: {client.get('pitch_hook', 'N/A')}")
    
    # Save to file
    with open('gemini_agent_output.json', 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n✅ Full output saved to: gemini_agent_output.json")
    print("="*80 + "\n")
    
    return result


def test_agent_by_agent(agent_external_id):
    """Test agent with specific agent's data"""
    print("\n" + "="*80)
    print(f"TEST 2: Gemini Agent - Agent {agent_external_id}")
    print("="*80 + "\n")
    
    # Fetch filtered data
    data = fetch_api_data(agent_external_id=agent_external_id)
    print(data)
    # return
    
    print("📈 Data Summary for this Agent:")
    print(f"  - Portfolio Opportunities: {data['portfolio'].get('total_clients', 0)}")
    print(f"  - Stagnant SIPs: {data['stagnant'].get('total_stagnant_sips', 0)}")
    print(f"  - Stopped SIPs: {data['stopped'].get('total_stopped_clients', 0)}")
    print(f"  - Insurance Gaps: {data['insurance'].get('total_opportunities', 0)}")
    print("\n🤖 Calling Gemini Agent...\n")
    
    # Call agent
    result = generate_dashboard_insight(
        portfolio_data=data['portfolio'],
        stagnant_data=data['stagnant'],
        stopped_data=data['stopped'],
        insurance_data=data['insurance']
    )
    
    # Quick summary
    hero = result.get('dashboard_hero', {})
    print(f"💰 Opportunity Value: {hero.get('formatted_value', 'N/A')}")
    print(f"📊 Summary: {hero.get('executive_summary', 'N/A')}")
    print(f"🎯 Focus Clients: {len(result.get('top_focus_clients', []))}")
    
    # Save
    filename = f"gemini_agent_output_{agent_external_id}.json"
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"\n✅ Output saved to: {filename}")
    print("="*80 + "\n")
    
    return result


if __name__ == "__main__":
    print("\n" + "="*80)
    print("🤖 GEMINI WEALTH INTELLIGENCE AGENT - TEST SUITE")
    print("="*80)
    print("\nPrerequisites:")
    print("  1. API server running: uvicorn app.main:app --reload --port 8111")
    print("  2. GOOGLE_API_KEY set in .env file")
    print("  3. Database populated with data")
    
    input("\nPress Enter to start testing...")
    
    # Test 1: All data
    # test_agent_basic()
    
    # Test 2: Specific agent (optional)
    # Uncomment and add agent ID:
    test_agent_by_agent("ag_v49teQwebZsmeXzzYN2GPN")
    
    print("\n✅ All tests complete!")