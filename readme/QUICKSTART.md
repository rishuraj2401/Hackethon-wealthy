# Quick Start Guide

Get the Wealthy Partner Dashboard API running in 5 minutes!

## 🚀 Quick Setup

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd /Users/rishurajsinha/Desktop/wealthy/Hackethon

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt
```

### Step 2: Start PostgreSQL

```bash
# Start PostgreSQL using Docker
docker-compose up -d

# Wait a few seconds for it to be ready
sleep 5
```

### Step 3: Import Data

```bash
# Import your SIP data
python scripts/import_data.py /Users/rishurajsinha/Downloads/query_result_2026-01-30T06_19_15.12414166Z.json
```

Expected output:
```
Creating database tables...
Loading data from ...
Found XXX records to import
Imported 100 records...
Imported 200 records...
...
Import completed!
Total imported: XXX
Total skipped (duplicates): 0
```

### Step 4: Start the API Server

```bash
# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or use the startup script:
```bash
./run.sh
```

### Step 5: Test the API

Open your browser and visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **API Root**: http://localhost:8000

Or run the test script:
```bash
python test_api.py
```

## 🎯 Quick API Examples

### Get All Opportunities
```bash
curl http://localhost:8000/api/opportunities?limit=10
```

### Get Statistics
```bash
curl http://localhost:8000/api/opportunities/stats
```

### Get Clients Without SIP Increase
```bash
curl "http://localhost:8000/api/opportunities/no-sip-increase?min_months=12&limit=10"
```

### Get Failed SIP Clients
```bash
curl "http://localhost:8000/api/opportunities/failed-sips?min_failed_amount=5000&limit=10"
```

### Get High-Value Inactive Clients
```bash
curl "http://localhost:8000/api/opportunities/high-value-inactive?min_invested_amount=100000&limit=10"
```

### Filter by Agent
```bash
curl "http://localhost:8000/api/opportunities?agent_id=4220&limit=10"
```

## 📊 Understanding Opportunities

### 1. No SIP Increase
**What it means**: Clients who haven't increased their SIP despite having increment periods configured.

**Why it matters**: These clients are stable and ready for investment growth.

**Action**: Contact client to increase SIP by configured increment percentage.

**Example Response**:
```json
{
  "user_id": "135",
  "agent_id": "4220",
  "opportunity_type": "No SIP Increase",
  "opportunity_description": "Client hasn't increased SIP for 18 months. Expected 2 increments based on 6M period.",
  "current_sip_amount": 5500.0,
  "potential_increase": 550.0,
  "last_activity_date": "January 5, 2026",
  "days_since_activity": 25,
  "total_invested": 283000.0,
  "risk_score": 3.0
}
```

### 2. Failed SIP Transactions
**What it means**: Clients with significant failed transaction amounts.

**Why it matters**: Revenue is being lost due to payment/mandate issues.

**Action**: Contact client to resolve mandate or payment issues.

**Key Fields**:
- `failed_amount`: Total amount of failed transactions
- `risk_score`: Based on failure rate (higher = more urgent)

### 3. High-Value Inactive Clients
**What it means**: Clients with substantial investments (₹100K+) who haven't transacted recently.

**Why it matters**: Prime candidates for upsell/cross-sell (insurance, new funds, portfolio review).

**Action**: Schedule portfolio review, offer additional products.

**Key Fields**:
- `total_invested`: Total successful investment amount
- `days_since_activity`: Days since last transaction
- `potential_increase`: Suggested additional investment

## 🔧 Troubleshooting

### PostgreSQL Not Starting
```bash
# Check if port 5432 is already in use
lsof -i :5432

# Stop and restart
docker-compose down
docker-compose up -d
```

### Import Fails
```bash
# Check database connection
docker-compose ps

# Check logs
docker-compose logs postgres

# Verify database exists
docker exec -it wealthy_postgres psql -U postgres -d wealthy_dashboard -c "\dt"
```

### API Not Starting
```bash
# Check if port 8000 is in use
lsof -i :8000

# Install dependencies again
pip install -r requirements.txt

# Check for import errors
python -c "from app.main import app; print('OK')"
```

## 📱 Next Steps

1. **Explore the API**: Visit http://localhost:8000/docs and try different endpoints
2. **Filter by Agent**: Add `?agent_id=XXX` to any opportunity endpoint
3. **Customize Thresholds**: Adjust `min_months`, `min_failed_amount`, etc.
4. **Export Data**: Use the API responses in your CRM or dashboard
5. **Build Frontend**: Create a dashboard UI using this API

## 🎉 Success!

You now have a working opportunity identification system. The API helps you:
- ✅ Identify clients ready for SIP increases
- ✅ Find and fix failed transactions
- ✅ Discover upsell opportunities
- ✅ Prioritize by potential revenue

For detailed documentation, see [README.md](README.md)
