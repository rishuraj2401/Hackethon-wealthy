# 🏦 Wealthy Partner Intelligence Dashboard

> AI-Powered Opportunity Detection System for Wealth Advisors

A FastAPI-based backend service that identifies high-value client opportunities by analyzing SIP performance, portfolio health, and insurance coverage gaps. Powered by Google Gemini AI for intelligent insights.

---

## 📋 Table of Contents

- [System Overview](#-system-overview)
- [Architecture](#-architecture)
- [Data Sources](#-data-sources)
- [Database Schema](#-database-schema)
- [Core APIs](#-core-apis)
- [Query Logic & Calculations](#-query-logic--calculations)
- [AI Agent](#-ai-agent)
- [Setup & Installation](#-setup--installation)
- [API Reference](#-api-reference)

---

## 🎯 System Overview

This system helps wealth advisors identify actionable opportunities across their client portfolios by analyzing:

| Opportunity Type | Description | Business Impact |
|-----------------|-------------|-----------------|
| **Portfolio Review** | Underperforming mutual fund schemes | Rebalancing advisory fees |
| **Stagnant SIPs** | SIPs without step-up configured | Growth opportunity |
| **Stopped SIPs** | Active SIPs with payment failures | Churn prevention |
| **Insurance Gaps** | High-value clients with low coverage | Cross-sell opportunity |

### Key Features

- ✅ Real-time opportunity detection from production data
- ✅ AI-powered client prioritization and insights
- ✅ Async, non-blocking API architecture
- ✅ Agent-level filtering for RM dashboards
- ✅ Aggregated metrics and executive summaries

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         WEALTHY PARTNER DASHBOARD                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐     ┌──────────────────────────────────────────────────┐  │
│  │   Frontend   │────▶│              FastAPI Backend                      │  │
│  │   (Client)   │     │                (main.py)                          │  │
│  └──────────────┘     │  ┌────────────────────────────────────────────┐  │  │
│                       │  │              API Endpoints                   │  │  │
│                       │  │  • /api/portfolio/review-opportunities      │  │  │
│                       │  │  • /api/opportunities/stagnant-sips         │  │  │
│                       │  │  • /api/opportunities/stopped-sips          │  │  │
│                       │  │  • /api/insurance/opportunities/coverage-gaps│  │  │
│                       │  │  • /api/ai/dashboard-insights               │  │  │
│                       │  └────────────────────────────────────────────┘  │  │
│                       └─────────────────────┬────────────────────────────┘  │
│                                             │                                │
│                            ┌────────────────┴────────────────┐              │
│                            ▼                                 ▼               │
│                   ┌─────────────────┐              ┌─────────────────┐      │
│                   │   PostgreSQL    │              │   Gemini AI     │      │
│                   │    Database     │              │    (agent.py)   │      │
│                   │                 │              │                 │      │
│                   │  • users        │              │  • Opportunity  │      │
│                   │  • sip_records  │              │    Scoring      │      │
│                   │  • insurance_   │              │  • Client       │      │
│                   │    records      │              │    Ranking      │      │
│                   │  • portfolio_   │              │  • Executive    │      │
│                   │    holdings     │              │    Summary      │      │
│                   └─────────────────┘              └─────────────────┘      │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Data Sources

### Production Data Pipeline

Data is sourced from **Wealthy's production ClickHouse cluster** (`delta-clickhouse` / `deltamesh_fact`):

```
┌─────────────────────────────────────────────────────────────────────┐
│                    PRODUCTION DATA SOURCES                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────────┐    ┌─────────────────────────────────────┐ │
│  │  delta-clickhouse   │    │        deltamesh_fact               │ │
│  │  (Data Warehouse)   │    │      (Fact Tables Layer)            │ │
│  └──────────┬──────────┘    └──────────────┬──────────────────────┘ │
│             │                               │                        │
│             └───────────────┬───────────────┘                        │
│                             ▼                                        │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    SOURCE TABLES                              │   │
│  │                                                               │   │
│  │  ┌──────────────────────┐  ┌──────────────────────────────┐  │   │
│  │  │  sip_meta_fact       │  │  client_profile_fact         │  │   │
│  │  │  ─────────────────   │  │  ─────────────────────────   │  │   │
│  │  │  • SIP transactions  │  │  • User demographics         │  │   │
│  │  │  • Payment history   │  │  • Portfolio values          │  │   │
│  │  │  • Step-up config    │  │  • Agent assignments         │  │   │
│  │  │  • Mandate status    │  │  • Activity dates            │  │   │
│  │  └──────────────────────┘  └──────────────────────────────┘  │   │
│  │                                                               │   │
│  │  ┌──────────────────────┐  ┌──────────────────────────────┐  │   │
│  │  │insurance_transaction │  │  portfolio_holdings          │  │   │
│  │  │       _fact          │  │  (derived from MF data)      │  │   │
│  │  │  ─────────────────   │  │  ─────────────────────────   │  │   │
│  │  │  • Insurance orders  │  │  • Scheme-level positions    │  │   │
│  │  │  • Premium data      │  │  • XIRR calculations         │  │   │
│  │  │  • Policy details    │  │  • Benchmark comparisons     │  │   │
│  │  └──────────────────────┘  └──────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                             │                                        │
│                             ▼                                        │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    PostgreSQL (Local)                         │   │
│  │              Dumped & Transformed for Analysis                │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Data Mapping

| Source Table | Local Table | Key Fields Used |
|-------------|-------------|-----------------|
| `sip_meta_fact` | `sip_records` | user_id, amount, scheme_name, increment_percentage, success_count, latest_success_order_date |
| `client_profile_fact` | `users` | user_id, name, date_of_birth, mf_current_value, agent_external_id |
| `insurance_transaction_fact` | `insurance_records` | user_id, premium, premium_gap, wealth_band, insurance_type |
| Portfolio data | `portfolio_holdings` | user_id, scheme_name, live_xirr, benchmark_xirr, current_value |

---

## 🗄 Database Schema

### Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DATABASE SCHEMA                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│    ┌─────────────────┐         ┌─────────────────────────────────┐  │
│    │     USERS       │         │         SIP_RECORDS             │  │
│    │  (client_profile│◄────────│                                 │  │
│    │     _fact)      │ user_id │  • sip_meta_id (PK)            │  │
│    ├─────────────────┤         │  • user_id (FK)                │  │
│    │ • user_id (PK)  │         │  • agent_external_id           │  │
│    │ • name          │         │  • amount                      │  │
│    │ • date_of_birth │         │  • scheme_name                 │  │
│    │ • mf_current_   │         │  • increment_percentage        │  │
│    │   value         │         │  • increment_amount            │  │
│    │ • agent_external│         │  • success_count               │  │
│    │   _id           │         │  • latest_success_order_date   │  │
│    │ • agent_name    │         │  • is_active                   │  │
│    └────────┬────────┘         │  • created_at                  │  │
│             │                  └─────────────────────────────────┘  │
│             │                                                        │
│             │ user_id          ┌─────────────────────────────────┐  │
│             │                  │      INSURANCE_RECORDS          │  │
│             ├─────────────────▶│   (insurance_transaction_fact)  │  │
│             │                  │                                 │  │
│             │                  │  • source_id (PK)               │  │
│             │                  │  • user_id (FK)                 │  │
│             │                  │  • agent_external_id            │  │
│             │                  │  • premium                      │  │
│             │                  │  • premium_gap                  │  │
│             │                  │  • baseline_expected_premium    │  │
│             │                  │  • wealth_band                  │  │
│             │                  │  • insurance_type               │  │
│             │                  │  • mf_current_value             │  │
│             │                  └─────────────────────────────────┘  │
│             │                                                        │
│             │ user_id          ┌─────────────────────────────────┐  │
│             │                  │      PORTFOLIO_HOLDINGS         │  │
│             └─────────────────▶│                                 │  │
│                                │  • id (PK)                      │  │
│                                │  • user_id (FK)                 │  │
│                                │  • scheme_name                  │  │
│                                │  • wpc (Wealthy Product Code)   │  │
│                                │  • current_value                │  │
│                                │  • live_xirr                    │  │
│                                │  • benchmark_xirr               │  │
│                                │  • benchmark_name               │  │
│                                │  • category                     │  │
│                                └─────────────────────────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔌 Core APIs

### Primary Endpoints Used

| # | Endpoint | Purpose | Filter |
|---|----------|---------|--------|
| 1 | `/api/portfolio/review-opportunities` | Underperforming MF schemes | `agent_external_id` |
| 2 | `/api/opportunities/stagnant-sips` | SIPs without step-up | `agent_external_id`, `limit` |
| 3 | `/api/opportunities/stopped-sips` | SIPs with payment gaps | `agent_external_id`, `limit` |
| 4 | `/api/insurance/opportunities/coverage-gaps` | Low insurance coverage | `agent_external_id` |
| 5 | `/api/ai/dashboard-insights` | AI-aggregated insights | `agent_external_id` |

### Request/Response Flow

```
┌─────────────────────────────────────────────────────────────────────┐
│                    AI DASHBOARD INSIGHTS FLOW                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   CLIENT REQUEST                                                     │
│   GET /api/ai/dashboard-insights?agent_external_id=ag_xxx            │
│                            │                                         │
│                            ▼                                         │
│   ┌────────────────────────────────────────────────────────────┐    │
│   │              ASYNC PARALLEL DATA FETCH                      │    │
│   │                  (ThreadPoolExecutor)                       │    │
│   │                                                             │    │
│   │   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │    │
│   │   │Portfolio │  │ Stagnant │  │ Stopped  │  │Insurance │  │    │
│   │   │ Review   │  │   SIPs   │  │   SIPs   │  │   Gaps   │  │    │
│   │   └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │    │
│   │        │             │             │             │         │    │
│   │        └─────────────┴──────┬──────┴─────────────┘         │    │
│   │                             │                               │    │
│   └─────────────────────────────┼───────────────────────────────┘    │
│                                 ▼                                    │
│   ┌────────────────────────────────────────────────────────────┐    │
│   │                  DATA OPTIMIZATION                          │    │
│   │                                                             │    │
│   │   • Portfolio: Top 10 clients by value                     │    │
│   │   • Stagnant SIPs: Top 15 by amount                        │    │
│   │   • Stopped SIPs: Top 15 by lifetime value                 │    │
│   │   • Insurance: Top 20 by premium gap                       │    │
│   │                                                             │    │
│   └─────────────────────────────┬───────────────────────────────┘    │
│                                 ▼                                    │
│   ┌────────────────────────────────────────────────────────────┐    │
│   │                   GEMINI AI AGENT                           │    │
│   │                                                             │    │
│   │   Model: gemini-2.0-flash                                  │    │
│   │   Config: temperature=0.2, response_mime_type=json         │    │
│   │                                                             │    │
│   │   Tasks:                                                    │    │
│   │   1. Calculate Total Opportunity Value                     │    │
│   │   2. Rank & Select Top 10 Focus Clients                    │    │
│   │   3. Generate Executive Summary                            │    │
│   │   4. Create Client Pitch Hooks                             │    │
│   │                                                             │    │
│   └─────────────────────────────┬───────────────────────────────┘    │
│                                 ▼                                    │
│   ┌────────────────────────────────────────────────────────────┐    │
│   │                     JSON RESPONSE                           │    │
│   │                                                             │    │
│   │   {                                                         │    │
│   │     "dashboard_hero": {                                     │    │
│   │       "total_opportunity_value": 1523000,                  │    │
│   │       "formatted_value": "₹15.2 Lakhs",                    │    │
│   │       "executive_summary": "...",                          │    │
│   │       "opportunity_breakdown": {...}                       │    │
│   │     },                                                      │    │
│   │     "top_focus_clients": [...],                            │    │
│   │     "metadata": { ... }                                    │    │
│   │   }                                                         │    │
│   │                                                             │    │
│   └────────────────────────────────────────────────────────────┘    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🧮 Query Logic & Calculations

### 1. Portfolio Review Opportunities

**Goal:** Find underperforming mutual fund schemes where `live_xirr < benchmark_xirr`

```sql
-- Conceptual Query Logic
SELECT 
    ph.user_id,
    ph.scheme_name,
    ph.live_xirr,
    ph.benchmark_xirr,
    (ph.benchmark_xirr - ph.live_xirr) AS xirr_underperformance,
    ph.current_value,
    u.name AS client_name,
    u.agent_external_id
FROM portfolio_holdings ph
JOIN users u ON ph.user_id = u.user_id
WHERE 
    ph.live_xirr IS NOT NULL
    AND ph.benchmark_xirr IS NOT NULL
    AND ph.live_xirr < ph.benchmark_xirr  -- UNDERPERFORMING
    AND ph.current_value > 0
    AND u.agent_external_id = :agent_external_id  -- Agent filter
```

**Business Logic:**
- Groups schemes by client
- Calculates total underperforming value per client
- Measures XIRR gap (benchmark - actual) as underperformance indicator

---

### 2. Stagnant SIP Opportunities

**Goal:** Find SIPs active for >6 months with **no step-up configured**

```sql
-- Conceptual Query Logic
SELECT 
    sr.user_id,
    sr.scheme_name,
    sr.amount AS current_sip,
    sr.created_at,
    sr.increment_percentage,
    sr.increment_amount,
    sr.success_amount,
    u.name AS user_name
FROM sip_records sr
LEFT JOIN users u ON sr.user_id = u.user_id
WHERE 
    sr.is_active = 'true'
    AND sr.scheme_name IS NOT NULL
    AND sr.scheme_name != '[]'
    AND (sr.increment_amount = 0 OR sr.increment_amount IS NULL)
    AND (sr.increment_percentage = 0 OR sr.increment_percentage IS NULL)
    AND sr.created_at < NOW() - INTERVAL '6 months'  -- Active for 6+ months
    AND sr.agent_external_id = :agent_external_id
```

**Calculation:**
```python
# Months stagnant
months_stagnant = (current_date.year - created_at.year) * 12 + 
                  (current_date.month - created_at.month)

# Potential step-up value (if 10% step-up was applied)
potential_value = current_sip * 0.10 * 12  # Annualized
```

---

### 3. Stopped SIP Opportunities

**Goal:** Find SIPs with ≥3 successful payments but no payment in >2 months

```sql
-- Conceptual Query Logic (Aggregated by User)
SELECT 
    sr.user_id,
    sr.agent_external_id,
    MAX(sr.success_count) AS max_success_count,
    MAX(sr.latest_success_order_date) AS last_success_date,
    SUM(sr.success_amount) AS lifetime_success_amount,
    COUNT(*) AS total_sips,
    SUM(CASE WHEN sr.is_active = 'true' THEN 1 ELSE 0 END) AS active_sips,
    STRING_AGG(sr.scheme_name, ', ') AS scheme_names,
    MAX(sr.amount) AS top_scheme_amount
FROM sip_records sr
WHERE sr.deleted = 'false'
GROUP BY sr.user_id, sr.agent_external_id
HAVING 
    MAX(sr.success_count) >= 3                -- At least 3 successful payments
    AND MAX(sr.is_active) = 'true'            -- Has active SIP
    AND MAX(sr.latest_success_order_date) < NOW() - INTERVAL '2 months'  -- No recent payment
```

**Calculation:**
```python
# Days stopped
days_stopped = (current_date - last_success_date).days

# Annualized stopped value
stopped_value = monthly_sip_amount * 12
```

---

### 4. Insurance Coverage Gaps

**Goal:** Find high-value clients with low/no insurance relative to their wealth

```sql
-- Conceptual Query Logic
WITH insurance_agg AS (
    SELECT 
        user_id,
        SUM(premium) AS total_premium
    FROM insurance_records
    WHERE deleted = 'false' AND premium > 0
    GROUP BY user_id
)
SELECT 
    u.user_id,
    u.name,
    u.date_of_birth,
    u.mf_current_value,
    u.agent_external_id,
    COALESCE(ia.total_premium, 0) AS total_premium,
    -- Expected premium based on age
    CASE 
        WHEN age < 30 THEN mf_current_value * 0.0005   -- 0.05%
        WHEN age BETWEEN 30 AND 39 THEN mf_current_value * 0.001  -- 0.1%
        WHEN age BETWEEN 40 AND 49 THEN mf_current_value * 0.002  -- 0.2%
        ELSE mf_current_value * 0.003  -- 0.3%
    END AS expected_premium
FROM users u
LEFT JOIN insurance_agg ia ON u.user_id = ia.user_id
WHERE 
    u.mf_current_value >= 500000  -- High-value clients only
    AND u.agent_external_id = :agent_external_id
```

**Expected Premium Formula:**

| Age Range | Expected Premium (% of MF Value) |
|-----------|----------------------------------|
| < 30 years | 0.05% |
| 30-39 years | 0.10% |
| 40-49 years | 0.20% |
| 50+ years | 0.30% |

**Gap Calculation:**
```python
premium_gap = expected_premium - actual_premium
gap_type = "NO_INSURANCE" if actual_premium == 0 else "LOW_COVERAGE"
```

---

## 🤖 AI Agent

### Overview

The AI Agent uses **Google Gemini 2.0 Flash** to analyze all four opportunity datasets and generate:

1. **Total Opportunity Value** - Single "hero metric" for the dashboard
2. **Top 10 Focus Clients** - Prioritized by complexity and value
3. **Executive Summary** - One-line pitch for the dashboard header
4. **Client Pitch Hooks** - Context strings for each client

### Opportunity Value Calculation (AI Logic)

```
┌─────────────────────────────────────────────────────────────────────┐
│                 TOTAL OPPORTUNITY VALUE FORMULA                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  STOPPED SIPs                                                │   │
│   │  Value = Monthly Amount × 12 (Annualized)                   │   │
│   │  Example: ₹10,000/month → ₹1,20,000                         │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                              +                                       │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  STAGNANT SIPs                                               │   │
│   │  Value = Current SIP × 10% × 12 (Potential Step-up)         │   │
│   │  Example: ₹20,000/month → ₹24,000/year potential            │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                              +                                       │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  INSURANCE GAPS                                              │   │
│   │  Value = premium_gap (direct from data)                     │   │
│   │  Example: ₹50,000 gap                                       │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                              +                                       │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  PORTFOLIO UNDERPERFORMANCE                                  │   │
│   │  Value = Current Value × 1% (Advisory fee impact)           │   │
│   │  Example: ₹10L underperforming → ₹10,000                    │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                              =                                       │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │  TOTAL OPPORTUNITY VALUE (Dashboard Hero Metric)             │   │
│   └─────────────────────────────────────────────────────────────┘   │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Client Ranking Algorithm

Clients are scored by:
1. **Value** - Total opportunity amount across all categories
2. **Complexity** - Number of issue types (multiple issues = higher rank)
3. **Risk** - Stopped SIPs indicate churn risk (priority)

```python
# Scoring logic (conceptual)
client_score = (
    stopped_sip_value * 2.0 +      # High weight for churn risk
    insurance_gap * 1.5 +          # Cross-sell opportunity
    stagnant_sip_potential * 1.0 + # Growth opportunity
    portfolio_underperformance * 0.5
)

# Complexity bonus
if num_issue_types >= 3:
    client_score *= 1.5
elif num_issue_types >= 2:
    client_score *= 1.2
```

### Response Schema

```json
{
  "dashboard_hero": {
    "total_opportunity_value": 1523000,
    "formatted_value": "₹15.2 Lakhs",
    "executive_summary": "Identified ₹15.2L in potential value across 45 clients requiring immediate attention.",
    "opportunity_breakdown": {
      "insurance": "₹8.5L",
      "sip_recovery": "₹5.2L",
      "portfolio_rebalancing": "₹1.5L"
    }
  },
  "top_focus_clients": [
    {
      "user_id": "usr_abc123",
      "client_name": "Rajesh Kumar",
      "total_impact_value": "₹2.5L",
      "tags": ["Risk: Stopped SIP", "Opp: Insurance Gap"],
      "pitch_hook": "High churn risk: SIP stopped for 45 days. Also has ₹1.2L insurance coverage gap.",
      "drill_down_details": {
        "portfolio_review": { "has_issue": true, "schemes": [...] },
        "sip_health": { "stopped_sips": [...], "stagnant_sips": [...] },
        "insurance": { "has_gap": true, "gap_amount": 120000, "wealth_band": "HNI" }
      }
    }
  ],
  "metadata": {
    "agent_external_id": "ag_xxx",
    "data_summary": {
      "portfolio_opportunities": { "total": 50, "analyzed": 10 },
      "stagnant_sips": { "total": 30, "analyzed": 15 },
      "stopped_sips": { "total": 20, "analyzed": 15 },
      "insurance_gaps": { "total": 37, "analyzed": 20 }
    },
    "optimization_note": "Data limited to top opportunities for faster AI processing"
  }
}
```

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.10+
- PostgreSQL 13+
- Docker (optional, for database)
- Google AI API Key

### Installation

```bash
# Clone repository
git clone <repo-url>
cd Hackethon

# Create virtual environment
conda create -n wealthy-dashboard python=3.10
conda activate wealthy-dashboard

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your credentials
```

### Environment Variables

```bash
# .env file
DATABASE_URL=postgresql://user:password@localhost:5432/wealthy_db
GOOGLE_API_KEY=your_gemini_api_key_here
DEBUG=false
```

### Database Setup

```bash
# Start PostgreSQL (Docker)
docker-compose up -d

# Run migrations (if applicable)
alembic upgrade head

# Import data from production dump
python scripts/import_users.py
python scripts/import_data.py      # SIP records
python scripts/import_insurance.py
```

### Run Server

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8111

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8111 --workers 4
```

---

## 📖 API Reference

### Base URL
```
http://localhost:8111
```

### Endpoints

#### 1. Portfolio Review Opportunities
```http
GET /api/portfolio/review-opportunities?agent_external_id=ag_xxx
```

#### 2. Stagnant SIP Opportunities
```http
GET /api/opportunities/stagnant-sips?agent_external_id=ag_xxx&limit=10
```

#### 3. Stopped SIP Opportunities
```http
GET /api/opportunities/stopped-sips?agent_external_id=ag_xxx&limit=10
```

#### 4. Insurance Coverage Gaps
```http
GET /api/insurance/opportunities/coverage-gaps?agent_external_id=ag_xxx
```

#### 5. AI Dashboard Insights (Main API)
```http
GET /api/ai/dashboard-insights?agent_external_id=ag_xxx
```

**Response Time:** 20-40 seconds (AI processing)

---

## 📁 Project Structure

```
Hackethon/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app & endpoints
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── services.py       # Business logic & queries
│   ├── database.py       # Database connection
│   └── config.py         # Settings & env vars
├── agent.py              # Gemini AI agent
├── scripts/
│   ├── import_users.py
│   ├── import_data.py
│   └── import_insurance.py
├── requirements.txt
├── docker-compose.yml
├── .env
└── README.md
```

---

## 🔧 Performance Optimizations

| Optimization | Impact |
|-------------|--------|
| Async endpoint with ThreadPoolExecutor | Non-blocking API calls |
| Parallel database queries | 4x faster data fetching |
| Data limiting before AI call | 40-50% faster AI processing |
| Gemini Flash model | Fastest available model |
| Lower temperature (0.2) | More focused, faster responses |

---

## 📝 License

Internal use only - Wealthy.in

---

## 👥 Contributors

- Wealthy Engineering Team
- Hackathon 2026
