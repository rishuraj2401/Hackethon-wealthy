# Wealthy Partner Dashboard - Backend API

A FastAPI-based backend service for identifying selling opportunities in client SIP portfolios. This dashboard helps advisors/distributors identify clients who need intervention, have upsell opportunities, or require portfolio reviews.

## Features

### 🎯 Opportunity Identification

The system analyzes SIP data to identify three key types of selling opportunities:

1. **No SIP Increase Opportunities**
   - Identifies clients who haven't increased their SIP for 12+ months
   - Tracks expected vs. actual increments based on increment period (6M/1Y)
   - Calculates potential increase based on configured increment percentage

2. **Failed SIP Transactions**
   - Flags clients with significant failed transaction amounts
   - Highlights mandate renewal or payment issue resolution needs
   - Calculates failure rates to prioritize interventions

3. **High-Value Inactive Clients**
   - Identifies clients with high invested amounts (₹100K+) who are inactive
   - Perfect for upsell/cross-sell opportunities (insurance, new products)
   - Prioritizes by total invested amount and inactivity period

## Tech Stack

- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Relational database
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation and settings management
- **Docker** - Containerization for PostgreSQL

## Project Structure

```
Hackethon/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── database.py        # Database connection
│   ├── models.py          # SQLAlchemy models
│   ├── schemas.py         # Pydantic schemas
│   ├── main.py            # FastAPI application
│   └── services.py        # Business logic
├── scripts/
│   ├── __init__.py
│   └── import_data.py     # Data import script
├── docker-compose.yml     # PostgreSQL container
├── requirements.txt       # Python dependencies
├── .gitignore
└── README.md
```

## Setup Instructions

### 1. Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Git

### 2. Clone and Setup

```bash
cd /Users/rishurajsinha/Desktop/wealthy/Hackethon

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Start PostgreSQL

```bash
# Start PostgreSQL using Docker Compose
docker-compose up -d

# Verify PostgreSQL is running
docker-compose ps
```

### 4. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env if needed (default values should work with docker-compose)
```

### 5. Import Data

```bash
# Import SIP data from JSON file
python scripts/import_data.py /Users/rishurajsinha/Downloads/query_result_2026-01-30T06_19_15.12414166Z.json
```

### 6. Run the Application

```bash
# Start FastAPI server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

## API Endpoints

### Core Endpoints

#### 1. Get All Opportunities
```http
GET /api/opportunities?agent_id={agent_id}&limit=100
```
Returns combined opportunities from all categories.

#### 2. No SIP Increase Opportunities
```http
GET /api/opportunities/no-sip-increase?agent_id={agent_id}&min_months=12&limit=100
```
Returns clients who haven't increased SIP for specified months.

**Parameters:**
- `agent_id` (optional): Filter by specific agent
- `min_months` (default: 12): Minimum months since last increase
- `limit` (default: 100): Maximum results to return

**Response:**
```json
[
  {
    "user_id": "135",
    "agent_id": "4220",
    "agent_external_id": "ag_Z2qZxPAKSbVLkJBRC2eZZF",
    "opportunity_type": "No SIP Increase",
    "opportunity_description": "Client hasn't increased SIP for 18 months...",
    "current_sip_amount": 5500.0,
    "potential_increase": 550.0,
    "last_activity_date": "January 5, 2026",
    "days_since_activity": 25,
    "total_invested": 283000.0,
    "risk_score": 3.0
  }
]
```

#### 3. Failed SIP Opportunities
```http
GET /api/opportunities/failed-sips?agent_id={agent_id}&min_failed_amount=5000&limit=100
```
Returns clients with failed transactions.

**Parameters:**
- `agent_id` (optional): Filter by specific agent
- `min_failed_amount` (default: 5000): Minimum failed amount threshold
- `limit` (default: 100): Maximum results to return

#### 4. High-Value Inactive Clients
```http
GET /api/opportunities/high-value-inactive?agent_id={agent_id}&min_invested_amount=100000&min_inactive_days=60&limit=100
```
Returns high-value clients who are inactive.

**Parameters:**
- `agent_id` (optional): Filter by specific agent
- `min_invested_amount` (default: 100000): Minimum invested amount
- `min_inactive_days` (default: 60): Minimum days of inactivity
- `limit` (default: 100): Maximum results to return

#### 5. Opportunity Statistics
```http
GET /api/opportunities/stats?agent_id={agent_id}
```
Returns aggregated statistics about opportunities.

**Response:**
```json
{
  "total_opportunities": 150,
  "total_potential_revenue": 2500000.0,
  "breakdown_by_type": {
    "no_sip_increase": {
      "count": 50,
      "potential_revenue": 500000.0
    },
    "failed_sips": {
      "count": 60,
      "potential_revenue": 1500000.0
    },
    "high_value_inactive": {
      "count": 40,
      "potential_revenue": 500000.0
    }
  }
}
```

### Utility Endpoints

#### 6. Get All Agents
```http
GET /api/agents
```
Returns list of all agents with their statistics.

#### 7. Get Client SIP Records
```http
GET /api/clients/{user_id}
```
Returns all SIP records for a specific client.

## Use Cases

### For Advisors/Distributors

1. **Daily Opportunity Review**
   - Check `/api/opportunities/stats` for overview
   - Review top opportunities from each category
   - Prioritize by risk_score and potential_increase

2. **Client Intervention Planning**
   - Use `/api/opportunities/failed-sips` to identify clients needing immediate help
   - Contact clients with mandate or payment issues

3. **Upsell Campaign**
   - Query `/api/opportunities/high-value-inactive` for clients ≥ ₹1L invested
   - Reach out with portfolio review or insurance products

4. **SIP Increment Campaign**
   - Use `/api/opportunities/no-sip-increase` for clients ready to increase investment
   - Target clients with 12+ months stability

### For Management

1. **Performance Dashboard**
   - Monitor opportunities across all agents
   - Track potential revenue by opportunity type
   - Identify top-performing agents

2. **Team Allocation**
   - Distribute opportunities based on agent capacity
   - Assign high-value opportunities to senior advisors

## Database Schema

### SIP Records Table

The `sip_records` table stores all SIP transaction data with the following key fields:

- **Identifiers**: uid, sip_meta_id, user_id, goal_id
- **Agent Info**: agent_id, agent_external_id, member_id
- **SIP Details**: amount, scheme_name, goal_name, start_date, end_date
- **Increment Config**: increment_percentage, increment_amount, increment_period
- **Financial Tracking**: success_amount, failed_amount, pending_amount
- **Status**: is_active, current_sip_status, sip_sales_status
- **Activity**: first_success_order_date, latest_success_order_date

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Database Management

```bash
# Reset database (drops all tables)
docker-compose down -v
docker-compose up -d

# Re-import data
python scripts/import_data.py <path_to_json>
```

### Adding New Opportunity Types

1. Add new function in `app/services.py`
2. Add new endpoint in `app/main.py`
3. Update statistics aggregation
4. Document in README

## Deployment

### Production Considerations

1. **Environment Variables**
   - Set strong PostgreSQL password
   - Use environment-specific DATABASE_URL
   - Disable DEBUG mode

2. **Security**
   - Add authentication/authorization
   - Implement rate limiting
   - Use HTTPS in production
   - Restrict CORS origins

3. **Performance**
   - Add database indexes on frequently queried fields
   - Implement caching (Redis)
   - Use connection pooling
   - Add pagination for large result sets

4. **Monitoring**
   - Add logging (structured logs)
   - Implement health checks
   - Set up error tracking (Sentry)
   - Monitor database performance

## Future Enhancements

- [ ] Add user authentication and authorization
- [ ] Implement real-time notifications for new opportunities
- [ ] Add email/SMS integration for client outreach
- [ ] Create agent performance analytics
- [ ] Build frontend dashboard
- [ ] Add more opportunity types (insurance gaps, portfolio rebalancing)
- [ ] Implement ML-based opportunity scoring
- [ ] Add export functionality (CSV, PDF reports)

## Support

For issues or questions:
- Create an issue in the repository
- Contact the development team

## License

Proprietary - Wealthy Platform
