"""
Simple test script to verify API endpoints
Run after starting the server: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:8111"


def test_health():
    """Test health endpoint"""
    print("Testing /health...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")


def test_root():
    """Test root endpoint"""
    print("Testing /...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_opportunities():
    """Test opportunities endpoint"""
    print("Testing /api/opportunities...")
    response = requests.get(f"{BASE_URL}/api/opportunities?limit=5")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} opportunities")
    if data:
        print(f"First opportunity: {json.dumps(data[0], indent=2)}\n")


def test_no_sip_increase():
    """Test no SIP increase endpoint"""
    print("Testing /api/opportunities/no-sip-increase...")
    response = requests.get(f"{BASE_URL}/api/opportunities/no-sip-increase?limit=5")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} clients without SIP increase\n")


def test_failed_sips():
    """Test failed SIPs endpoint"""
    print("Testing /api/opportunities/failed-sips...")
    response = requests.get(f"{BASE_URL}/api/opportunities/failed-sips?limit=5")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} clients with failed SIPs\n")


def test_high_value_inactive():
    """Test high value inactive endpoint"""
    print("Testing /api/opportunities/high-value-inactive...")
    response = requests.get(f"{BASE_URL}/api/opportunities/high-value-inactive?limit=5")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} high-value inactive clients\n")


def test_stats():
    """Test statistics endpoint"""
    print("Testing /api/opportunities/stats...")
    response = requests.get(f"{BASE_URL}/api/opportunities/stats")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Statistics: {json.dumps(data, indent=2)}\n")


def test_agents():
    """Test agents endpoint"""
    print("Testing /api/agents...")
    response = requests.get(f"{BASE_URL}/api/agents")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Found {len(data)} agents")
    if data:
        print(f"Top agent: {json.dumps(data[0], indent=2)}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Wealthy Partner Dashboard API - Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_health()
        test_root()
        test_opportunities()
        test_no_sip_increase()
        test_failed_sips()
        test_high_value_inactive()
        test_stats()
        test_agents()
        
        print("=" * 60)
        print("✅ All tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API")
        print("   Make sure the server is running: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
