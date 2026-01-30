from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class InsuranceRecord(Base):
    __tablename__ = "insurance_records"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Identifiers
    uid = Column(String, index=True)
    source_id = Column(String, index=True, unique=True)
    deleted = Column(String)
    checksum = Column(String)
    
    # Client Information
    user_id = Column(String, index=True)  # itf.user_id
    name = Column(String, index=True)
    mf_current_value = Column(Float)
    wealth_band = Column(String, index=True)
    mock_age = Column(Integer)
    
    # Transaction Details
    transaction_date = Column(String, index=True)
    transaction_amount = Column(Float)
    transaction_type = Column(String)
    transaction_category = Column(String)
    instrument_type = Column(String)
    product_name = Column(String)
    transaction_status = Column(String, index=True)
    order_status = Column(String, index=True)
    
    # Dates
    event_date = Column(String)
    created_at = Column(String)
    wealthy_processed_at = Column(String)
    order_date = Column(String)
    
    # Order Information
    order_id = Column(String)
    transaction_id = Column(String)
    transaction_units = Column(String)
    order_category = Column(String)
    order_type = Column(String)
    
    # Insurance Specific
    insurance_order_id = Column(String)
    insurance_type = Column(String, index=True)  # ULIP, Traditional, Health, Term, etc.
    sourcing_channel = Column(String)
    user_product_id = Column(String)
    insurer = Column(String, index=True)
    premium_frequency = Column(String)
    policy_issue_date = Column(String)
    policy_number = Column(String)
    application_number = Column(String)
    wpc = Column(String)
    premium = Column(Float)
    
    # Agent Information
    agent_id = Column(String, index=True)
    agent_external_id = Column(String, index=True)  # itf.agent_external_id
    member_id = Column(String, index=True)
    b_agent_external_id = Column(String)  # b.agent_external_id
    
    # Opportunity Metrics
    total_premium = Column(Float)
    baseline_expected_premium = Column(Float)
    premium_gap = Column(Float, index=True)
    opportunity_score = Column(Integer, index=True)
    
    # Metadata
    created_in_db = Column(DateTime(timezone=True), server_default=func.now())
    updated_in_db = Column(DateTime(timezone=True), onupdate=func.now())


class SIPRecord(Base):
    __tablename__ = "sip_records"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Identifiers
    uid = Column(String, index=True)
    sip_meta_id = Column(String, index=True, unique=True)
    user_id = Column(String, index=True)
    goal_id = Column(String)
    
    # Agent/Advisor Information
    agent_id = Column(String, index=True)
    agent_external_id = Column(String, index=True)
    member_id = Column(String, index=True)
    
    # SIP Details
    amount = Column(Float)
    sip_days = Column(String)
    num_days = Column(Integer)
    scheme_name = Column(Text)
    goal_name = Column(String)
    
    # Dates
    created_at = Column(String)
    sip_meta_date = Column(String)
    sip_meta_month = Column(String)
    start_date = Column(String, index=True)
    end_date = Column(String)
    event_date = Column(String)
    inserted_at = Column(String)
    
    # Increment Configuration
    increment_percentage = Column(Float)
    increment_amount = Column(Float)
    increment_period = Column(String, index=True)
    
    # Pause Information
    paused_from = Column(String)
    paused_till = Column(String)
    paused_reason = Column(String)
    
    # Status Fields
    is_active = Column(String)
    sip_sales_status = Column(String, index=True)
    current_sip_status = Column(String, index=True)
    
    # Mandate Information
    had_mandate_at_creation = Column(String)
    has_current_mandate = Column(String)
    mandate_tracking_status = Column(String)
    mandate_confirmed_date = Column(String)
    
    # Order Dates
    first_order_nav_allocated_at = Column(String)
    first_success_order_date = Column(String, index=True)
    latest_success_order_date = Column(String, index=True)
    first_success_order_month = Column(String)
    latest_success_order_month = Column(String)
    
    # Financial Tracking
    success_amount = Column(Float)
    pending_amount = Column(Float)
    failed_amount = Column(Float)
    in_progress_amount = Column(Float)
    paused_amount = Column(Float)
    success_count = Column(Integer)
    
    # Flags
    stepper_enabled = Column(String)
    deleted = Column(String)
    
    # Metadata
    created_in_db = Column(DateTime(timezone=True), server_default=func.now())
    updated_in_db = Column(DateTime(timezone=True), onupdate=func.now())
