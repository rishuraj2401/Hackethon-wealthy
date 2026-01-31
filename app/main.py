from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from app.database import get_db
from app import schemas
from app import services
from agent import generate_dashboard_insight

app = FastAPI(
    title="Wealthy Partner Dashboard API",
    description="API for identifying selling opportunities in client portfolios (SIP + Insurance + Portfolio Analysis)",
    version="3.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "message": "Wealthy Partner Dashboard API",
        "version": "3.0.0",
        "modules": {
            "sip": "Systematic Investment Plan opportunities",
            "insurance": "Insurance coverage and gap analysis",
            "portfolio": "Portfolio holdings and fund performance analysis"
        },
        "endpoints": {
            "sip_opportunities": {
                "all": "/api/opportunities",
                "no_increase": "/api/opportunities/no-sip-increase",
                "failed": "/api/opportunities/failed-sips",
                "inactive": "/api/opportunities/high-value-inactive",
                "stagnant": "/api/opportunities/stagnant-sips",
                "stopped": "/api/opportunities/stopped-sips",
                "stats": "/api/opportunities/stats"
            },
            "insurance_opportunities": {
                "gaps": "/api/insurance/opportunities/gaps",
                "no_coverage": "/api/insurance/opportunities/no-coverage",
                "coverage_gaps": "/api/insurance/opportunities/coverage-gaps",
                "stats": "/api/insurance/stats"
            },
            "portfolio_opportunities": {
                "all": "/api/portfolio/opportunities",
                "underperforming": "/api/portfolio/opportunities/underperforming",
                "low_rated": "/api/portfolio/opportunities/low-rated",
                "concentration": "/api/portfolio/opportunities/concentration",
                "review": "/api/portfolio/review-opportunities",
                "stats": "/api/portfolio/stats"
            },
            "clients": {
                "sips": "/api/clients/{user_id}/sips",
                "insurance": "/api/clients/{user_id}/insurance",
                "portfolio": "/api/clients/{user_id}/portfolio"
            },
            "ai_insights": {
                "dashboard": "/api/ai/dashboard-insights"
            },
            "users": {
                "all": "/api/users",
                "by_id": "/api/users/{user_id}",
                "high_value": "/api/users/high-value/list",
                "by_age": "/api/users/age-range/list",
                "stats": "/api/users/stats"
            },
            "agents": "/api/agents"
        }
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/api/opportunities", response_model=List[schemas.OpportunityClient])
def get_all_opportunities(
    agent_id: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all selling opportunities across all categories"""
    return services.get_all_opportunities(db, agent_id=agent_id, limit=limit)


@app.get("/api/opportunities/no-sip-increase", response_model=List[schemas.OpportunityClient])
def get_no_sip_increase_opportunities(
    agent_id: Optional[str] = None,
    min_months: int = Query(12, ge=1),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get clients who haven't increased their SIP for specified months or more.
    This identifies clients who may be ready for an investment increase.
    """
    return services.get_no_sip_increase_clients(db, agent_id=agent_id, min_months=min_months, limit=limit)


@app.get("/api/opportunities/failed-sips", response_model=List[schemas.OpportunityClient])
def get_failed_sip_opportunities(
    agent_id: Optional[str] = None,
    min_failed_amount: float = Query(5000.0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get clients with failed SIP transactions requiring intervention.
    These clients may need mandate renewal or payment resolution.
    """
    return services.get_failed_sip_clients(db, agent_id=agent_id, min_failed_amount=min_failed_amount, limit=limit)


@app.get("/api/opportunities/high-value-inactive", response_model=List[schemas.OpportunityClient])
def get_high_value_inactive_opportunities(
    agent_id: Optional[str] = None,
    min_invested_amount: float = Query(100000.0, ge=0),
    min_inactive_days: int = Query(60, ge=1),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get high-value clients who have been inactive for a while.
    These are upsell/cross-sell opportunities for additional products.
    """
    return services.get_high_value_inactive_clients(
        db, agent_id=agent_id, min_invested_amount=min_invested_amount,
        min_inactive_days=min_inactive_days, limit=limit
    )


@app.get("/api/opportunities/stagnant-sips", response_model=schemas.StagnantSIPResponse)
def get_stagnant_sip_opportunities(
    agent_id: Optional[str] = Query(None, description="Filter by internal agent ID"),
    agent_external_id: Optional[str] = Query(None, description="Filter by external agent ID (preferred)"),
    min_months: int = Query(6, ge=1, description="Minimum months of stagnation"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get stagnant SIP opportunities - SIPs that haven't increased and have step-up disabled.
    
    A SIP is considered "stagnant" when:
    - It is currently active (is_active = true)
    - It was created more than min_months ago (default: 6 months)
    - It has NO step-up configured:
      - increment_amount is NULL or 0
      - increment_percentage is NULL or 0
    
    These represent opportunities to:
    - Enable step-up/increment features
    - Increase SIP amounts manually
    - Review and optimize investment strategy
    
    Query Parameters:
    - agent_id: Optional filter by internal agent ID
    - agent_external_id: Optional filter by external agent ID (preferred, e.g., ag_xyz123)
    - min_months: Minimum months since creation (default: 6)
    - limit: Maximum number of results (default: 100)
    
    Note: If both agent_id and agent_external_id are provided, agent_external_id takes precedence
    
    Returns:
    - total_stagnant_sips: Total count of stagnant SIPs
    - total_clients_affected: Number of unique clients with stagnant SIPs
    - total_sip_value: Sum of all stagnant SIP amounts
    - opportunities: List of stagnant SIP details sorted by months stagnant (oldest first)
    """
    return services.get_stagnant_sip_opportunities(
        db, agent_id=agent_id, agent_external_id=agent_external_id, 
        min_months=min_months, limit=limit
    )


@app.get("/api/opportunities/stopped-sips", response_model=schemas.StoppedSIPResponse)
def get_stopped_sip_opportunities(
    agent_external_id: Optional[str] = Query(None, description="Filter by external agent ID"),
    min_success_count: int = Query(3, ge=1, description="Minimum successful transactions required"),
    min_inactive_months: int = Query(2, ge=1, description="Minimum months since last success"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get stopped SIP opportunities - Active SIPs that haven't had successful payments recently.
    
    A SIP is considered "stopped" when:
    - User has had at least min_success_count successful transactions (default: 3)
      - This confirms they were previously active and engaged
    - Last successful payment was more than min_inactive_months ago (default: 2 months)
    - User still has at least one active SIP in the system
    - Records are not deleted
    
    These typically indicate:
    - Payment failures (insufficient funds, card expired, etc.)
    - Expired or cancelled mandates
    - Bank account issues
    - User-initiated pauses or stops
    
    Intervention opportunities:
    - Mandate renewal
    - Payment method update
    - Re-engagement campaigns
    - Understanding reasons for stopping
    
    Query Parameters:
    - agent_external_id: Optional filter by external agent ID (e.g., ag_xyz123)
    - min_success_count: Minimum past successful transactions (default: 3)
    - min_inactive_months: Minimum months without success (default: 2)
    - limit: Maximum number of results (default: 100)
    
    Returns:
    - total_stopped_clients: Number of clients with stopped SIPs
    - total_active_sips_affected: Total count of active SIPs that are stopped
    - total_lifetime_investment: Sum of all lifetime investments
    - average_days_inactive: Average days since last successful payment
    - opportunities: List sorted by days inactive (most critical first)
    """
    return services.get_stopped_sip_opportunities(
        db, agent_external_id=agent_external_id,
        min_success_count=min_success_count,
        min_inactive_months=min_inactive_months,
        limit=limit
    )


@app.get("/api/opportunities/stats", response_model=schemas.OpportunityStats)
def get_opportunity_stats(
    agent_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get statistics about selling opportunities"""
    return services.get_opportunity_statistics(db, agent_id=agent_id)


@app.get("/api/agents", response_model=List[dict])
def get_agents(db: Session = Depends(get_db)):
    """Get list of all agents/advisors"""
    return services.get_all_agents(db)


@app.get("/api/clients/{user_id}/sips", response_model=List[schemas.SIPRecordResponse])
def get_client_sips(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get all SIP records for a specific client"""
    return services.get_client_sip_records(db, user_id)


# ==================== Insurance Endpoints ====================

@app.get("/api/insurance/opportunities/gaps", response_model=List[schemas.InsuranceOpportunity])
def get_insurance_gap_opportunities(
    agent_id: Optional[str] = None,
    min_premium_gap: float = Query(10000.0, ge=0),
    min_opportunity_score: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get clients with insurance coverage gaps.
    These clients are paying less premium than their baseline expectation based on wealth.
    """
    return services.get_insurance_gap_opportunities(
        db, agent_id=agent_id, min_premium_gap=min_premium_gap,
        min_opportunity_score=min_opportunity_score, limit=limit
    )


@app.get("/api/insurance/opportunities/no-coverage", response_model=List[schemas.InsuranceOpportunity])
def get_no_insurance_opportunities(
    agent_id: Optional[str] = None,
    min_mf_value: float = Query(1000000.0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get high-value MF clients with NO insurance coverage.
    These are the highest priority cross-sell opportunities.
    """
    return services.get_no_insurance_clients(
        db, agent_id=agent_id, min_mf_value=min_mf_value, limit=limit
    )


@app.get("/api/insurance/stats")
def get_insurance_statistics(
    agent_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get insurance portfolio statistics"""
    return services.get_insurance_statistics(db, agent_id=agent_id)


@app.get("/api/insurance/opportunities/coverage-gaps", response_model=schemas.InsuranceGapResponse)
def get_insurance_coverage_gaps(
    agent_external_id: Optional[str] = Query(None, description="Filter by external agent ID"),
    min_mf_value: float = Query(500000.0, ge=0, description="Minimum MF portfolio value"),
    min_age: int = Query(30, ge=18, le=100, description="Minimum age for NO_INSURANCE flag"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of results"),
    db: Session = Depends(get_db)
):
    """
    Get insurance coverage gap opportunities for high-value clients.
    
    This endpoint identifies clients with significant mutual fund investments who have
    inadequate or no insurance coverage, representing cross-sell opportunities.
    
    Coverage Assessment Logic:
    
    1. Target Audience:
       - Clients with MF portfolio > min_mf_value (default: ₹5 lakhs)
       - Must have date of birth in system for age calculation
    
    2. Expected Premium Calculation (as % of MF current value):
       - Age < 30: 0.05% of MF value
       - Age 30-39: 0.1% of MF value
       - Age 40-49: 0.2% of MF value
       - Age 50+: 0.3% of MF value
    
    3. Insurance Status:
       - NO_INSURANCE: Zero premium paid and age >= min_age
       - LOW_COVERAGE: Current premium < expected premium
       - COVERED: Adequate coverage (not returned)
    
    4. Opportunity Value:
       - Gap between expected and actual premium
       - Represents potential additional premium revenue
    
    Use Cases:
    - Cross-selling insurance to wealthy MF investors
    - Identifying underinsured clients
    - Portfolio risk management
    - Agent commission opportunities
    
    Query Parameters:
    - agent_external_id: Optional filter by external agent ID
    - min_mf_value: Minimum MF value to qualify (default: ₹500,000)
    - min_age: Minimum age for NO_INSURANCE classification (default: 30)
    - limit: Maximum results (default: 100)
    
    Returns:
    - total_opportunities: Count of clients with gaps
    - no_insurance_count: Clients with zero coverage
    - low_coverage_count: Clients with insufficient coverage
    - total_opportunity_value: Sum of all premium gaps
    - total_mf_value_at_risk: Total MF value of uncovered/underinsured clients
    - average_age: Average age of opportunity clients
    - opportunities: List sorted by opportunity value (highest first)
    """
    return services.get_insurance_gap_opportunities(
        db, agent_external_id=agent_external_id,
        min_mf_value=min_mf_value,
        min_age=min_age,
        limit=limit
    )


@app.get("/api/clients/{user_id}/insurance", response_model=List[schemas.InsuranceRecordResponse])
def get_client_insurance(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get all insurance records for a specific client"""
    return services.get_client_insurance_records(db, user_id)


# ==================== User Endpoints ====================

@app.get("/api/users", response_model=List[schemas.UserResponse])
def get_all_users(
    agent_id: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """Get all users with pagination"""
    return services.get_all_users(db, agent_id=agent_id, limit=limit, offset=offset)


@app.get("/api/users/{user_id}", response_model=schemas.UserResponse)
def get_user(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific user by user_id"""
    user = services.get_user_by_id(db, user_id)
    if not user:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/api/users/high-value/list", response_model=List[schemas.UserResponse])
def get_high_value_users(
    min_value: float = Query(1000000.0, ge=0),
    agent_id: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get high-value users based on portfolio value"""
    return services.get_high_value_users(db, min_value=min_value, agent_id=agent_id, limit=limit)


@app.get("/api/users/age-range/list", response_model=List[schemas.UserResponse])
def get_users_by_age(
    min_age: int = Query(25, ge=18, le=100),
    max_age: int = Query(70, ge=18, le=100),
    agent_id: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get users within a specific age range (based on mock DOB)"""
    return services.get_users_by_age_range(db, min_age=min_age, max_age=max_age, agent_id=agent_id, limit=limit)


@app.get("/api/users/stats")
def get_user_statistics(
    agent_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get user and portfolio statistics"""
    return services.get_user_statistics(db, agent_id=agent_id)


# ==================== Portfolio Endpoints ====================

@app.get("/api/portfolio/opportunities", response_model=List[schemas.PortfolioOpportunity])
def get_all_portfolio_opportunities(
    user_id: Optional[str] = None,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all portfolio optimization opportunities (underperforming, low-rated, concentrated)"""
    return services.get_all_portfolio_opportunities(db, user_id=user_id, limit=limit)


@app.get("/api/portfolio/opportunities/underperforming", response_model=List[schemas.PortfolioOpportunity])
def get_underperforming_funds(
    user_id: Optional[str] = None,
    min_current_value: float = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get underperforming mutual funds with negative alpha or XIRR performance.
    These funds are underperforming their benchmarks and should be reviewed.
    """
    return services.get_underperforming_funds(db, user_id=user_id, min_current_value=min_current_value, limit=limit)


@app.get("/api/portfolio/opportunities/low-rated", response_model=List[schemas.PortfolioOpportunity])
def get_low_rated_funds(
    user_id: Optional[str] = None,
    max_rating: float = Query(3.0, ge=0, le=5.0),
    min_current_value: float = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get low-rated funds (rating below threshold).
    Consider switching these to higher-rated alternatives.
    """
    return services.get_low_rated_funds(db, user_id=user_id, max_rating=max_rating, min_current_value=min_current_value, limit=limit)


@app.get("/api/portfolio/opportunities/concentration", response_model=List[schemas.PortfolioOpportunity])
def get_concentration_opportunities(
    user_id: Optional[str] = None,
    min_concentration: float = Query(25.0, ge=0, le=100),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Get portfolios with high concentration in single funds.
    These may need rebalancing for better diversification.
    """
    return services.get_portfolio_rebalancing_opportunities(db, user_id=user_id, min_concentration=min_concentration, limit=limit)


@app.get("/api/portfolio/stats")
def get_portfolio_statistics(
    user_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get portfolio statistics including performance metrics"""
    return services.get_portfolio_statistics(db, user_id=user_id)


@app.get("/api/clients/{user_id}/portfolio", response_model=List[schemas.PortfolioHoldingResponse])
def get_client_portfolio(
    user_id: str,
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all portfolio holdings for a specific client"""
    return services.get_user_portfolio_holdings(db, user_id, limit=limit)


@app.get("/api/portfolio/review-opportunities", response_model=schemas.PortfolioReviewResponse)
def get_portfolio_review_opportunities(
    agent_external_id: Optional[str] = Query(None, description="Filter by agent's external ID"),
    db: Session = Depends(get_db)
):
    """
    Get portfolio review opportunities - underperforming schemes grouped by clients.
    
    This endpoint identifies schemes where live_xirr < benchmark_xirr (underperforming).
    
    Results are grouped by client showing:
    - Number of underperforming schemes per client
    - Total value of underperforming schemes per client
    - Client details (name, ID)
    - List of underperforming schemes with details:
      - Scheme WPC
      - Scheme name
      - Live XIRR
      - Benchmark XIRR
      - XIRR underperformance (difference)
      - Current value
      - Benchmark name
      - Category
      - AMC name
    
    Query Parameters:
    - agent_external_id: Optional filter to show only clients of a specific agent
    
    Returns:
    - total_clients: Number of clients with underperforming schemes
    - total_underperforming_schemes: Total count of underperforming schemes
    - total_value_underperforming: Total value across all underperforming schemes
    - clients: List of clients with their underperforming schemes
    """
    return services.get_portfolio_review_opportunities(db, agent_external_id=agent_external_id)


# Helper functions to optimize data before sending to AI
def _get_attr(obj, key, default=0):
    """Safely get attribute from dict or Pydantic model"""
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _optimize_portfolio_data(data: dict, limit: int = 10) -> dict:
    """Limit portfolio data to top clients by value"""
    if 'clients' in data:
        # Sort by total underperforming value and limit
        clients = data['clients']
        if len(clients) > limit:
            clients = sorted(
                clients,
                key=lambda x: _get_attr(x, 'total_value_underperforming', 0),
                reverse=True
            )[:limit]
        data['clients'] = clients
    return data


def _optimize_sip_data(data: dict, limit: int = 15) -> dict:
    """Limit SIP opportunities to top by value/impact"""
    if 'opportunities' in data:
        opps = data['opportunities']
        if len(opps) > limit:
            # For stagnant: prioritize by current_sip amount
            # For stopped: prioritize by lifetime_success_amount
            if opps and hasattr(opps[0], 'current_sip'):
                opps = sorted(opps, key=lambda x: _get_attr(x, 'current_sip', 0), reverse=True)[:limit]
            else:
                opps = sorted(opps, key=lambda x: _get_attr(x, 'lifetime_success_amount', 0), reverse=True)[:limit]
        data['opportunities'] = opps
    return data


def _optimize_insurance_data(data: dict, limit: int = 20) -> dict:
    """Limit insurance opportunities to top by gap amount"""
    if 'opportunities' in data:
        opps = data['opportunities']
        if len(opps) > limit:
            opps = sorted(
                opps,
                key=lambda x: _get_attr(x, 'premium_gap', 0),
                reverse=True
            )[:limit]
        data['opportunities'] = opps
    return data


@app.get("/api/ai/dashboard-insights", response_model=Dict[str, Any])
async def get_ai_dashboard_insights(
    agent_external_id: Optional[str] = Query(None, description="Filter by agent external ID"),
    agent_id: Optional[str] = Query(None, description="Filter by agent ID"),
    db: Session = Depends(get_db)
):
    """
    🤖 AI-Powered Dashboard Insights
    
    Fetches data from all 4 opportunity APIs and uses Gemini AI to generate:
    - Total opportunity value calculation
    - Top 10 focus clients ranked by complexity and value
    - Executive summary and pitch hooks
    
    **Parameters:**
    - agent_external_id: Filter opportunities by agent external ID
    - agent_id: Filter opportunities by agent ID (optional)
    
    **Returns:**
    - dashboard_hero: Overall metrics and opportunity breakdown
    - top_focus_clients: Top 10 clients with detailed drill-down
    
    **Data Sources (fetched internally):**
    1. Portfolio Review Opportunities (underperforming schemes)
    2. Stagnant SIP Opportunities (no step-up configured)
    3. Stopped SIP Opportunities (no payments in >2 months)
    4. Insurance Coverage Gaps (low/no insurance)
    """
    try:
        import asyncio
        from concurrent.futures import ThreadPoolExecutor
        from app.database import SessionLocal
        
        # Helper to run service with its own DB session
        def run_with_db(service_func, *args):
            db_session = SessionLocal()
            try:
                return service_func(db_session, *args)
            finally:
                db_session.close()
        
        # Use thread pool for blocking database operations
        loop = asyncio.get_event_loop()
        executor = ThreadPoolExecutor(max_workers=4)
        
        # Fetch data from all 4 APIs in parallel with separate DB sessions
        portfolio_task = loop.run_in_executor(
            executor,
            run_with_db,
            services.get_portfolio_review_opportunities,
            agent_external_id
        )
        
        stagnant_task = loop.run_in_executor(
            executor,
            run_with_db,
            services.get_stagnant_sip_opportunities,
            agent_id,
            agent_external_id,
            6
        )
        
        stopped_task = loop.run_in_executor(
            executor,
            run_with_db,
            services.get_stopped_sip_opportunities,
            agent_external_id,
            3,
            2
        )
        
        insurance_task = loop.run_in_executor(
            executor,
            run_with_db,
            services.get_insurance_gap_opportunities,
            agent_external_id,
            500000
        )
        
        # Wait for all data fetching to complete in parallel
        portfolio_data, stagnant_sips_data, stopped_sips_data, insurance_gaps_data = await asyncio.gather(
            portfolio_task, stagnant_task, stopped_task, insurance_task
        )
        
        # Optimize data before sending to AI - limit to top opportunities
        optimized_portfolio = _optimize_portfolio_data(portfolio_data)
        optimized_stagnant = _optimize_sip_data(stagnant_sips_data, limit=15)
        optimized_stopped = _optimize_sip_data(stopped_sips_data, limit=15)
        optimized_insurance = _optimize_insurance_data(insurance_gaps_data, limit=20)
        
        # Call AI agent with optimized data (run in executor to not block)
        ai_response = await loop.run_in_executor(
            executor,
            generate_dashboard_insight,
            optimized_portfolio,
            optimized_stagnant,
            optimized_stopped,
            optimized_insurance
        )
        
        # Add metadata with both original and optimized counts
        return {
            **ai_response,
            "metadata": {
                "agent_external_id": agent_external_id,
                "agent_id": agent_id,
                "data_summary": {
                    "portfolio_opportunities": {
                        "total": len(portfolio_data.get("clients", [])),
                        "analyzed": len(optimized_portfolio.get("clients", []))
                    },
                    "stagnant_sips": {
                        "total": len(stagnant_sips_data.get("opportunities", [])),
                        "analyzed": len(optimized_stagnant.get("opportunities", []))
                    },
                    "stopped_sips": {
                        "total": len(stopped_sips_data.get("opportunities", [])),
                        "analyzed": len(optimized_stopped.get("opportunities", []))
                    },
                    "insurance_gaps": {
                        "total": len(insurance_gaps_data.get("opportunities", [])),
                        "analyzed": len(optimized_insurance.get("opportunities", []))
                    }
                },
                "optimization_note": "Data limited to top opportunities for faster AI processing"
            }
        }
        
    except Exception as e:
        # Return error with fallback structure
        return {
            "dashboard_hero": {
                "total_opportunity_value": 0,
                "formatted_value": "Error",
                "executive_summary": f"Error generating insights: {str(e)}",
                "opportunity_breakdown": {
                    "insurance": "0",
                    "sip_recovery": "0",
                    "portfolio_rebalancing": "0"
                }
            },
            "top_focus_clients": [],
            "error": str(e),
            "metadata": {
                "agent_external_id": agent_external_id,
                "agent_id": agent_id,
                "status": "error"
            }
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8111)
