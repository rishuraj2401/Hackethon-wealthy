from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app import schemas
from app import services

app = FastAPI(
    title="Wealthy Partner Dashboard API",
    description="API for identifying selling opportunities in client portfolios (SIP + Insurance)",
    version="2.0.0"
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
        "version": "2.0.0",
        "modules": {
            "sip": "Systematic Investment Plan opportunities",
            "insurance": "Insurance coverage and gap analysis"
        },
        "endpoints": {
            "sip_opportunities": {
                "all": "/api/opportunities",
                "no_increase": "/api/opportunities/no-sip-increase",
                "failed": "/api/opportunities/failed-sips",
                "inactive": "/api/opportunities/high-value-inactive",
                "stats": "/api/opportunities/stats"
            },
            "insurance_opportunities": {
                "gaps": "/api/insurance/opportunities/gaps",
                "no_coverage": "/api/insurance/opportunities/no-coverage",
                "stats": "/api/insurance/stats"
            },
            "clients": {
                "sips": "/api/clients/{user_id}/sips",
                "insurance": "/api/clients/{user_id}/insurance"
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


@app.get("/api/clients/{user_id}/insurance", response_model=List[schemas.InsuranceRecordResponse])
def get_client_insurance(
    user_id: str,
    db: Session = Depends(get_db)
):
    """Get all insurance records for a specific client"""
    return services.get_client_insurance_records(db, user_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8111)
