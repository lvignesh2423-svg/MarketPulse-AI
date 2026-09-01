from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class RiskTolerance(str, Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"

class UserProfile(BaseModel):
    user_id: str
    name: str
    risk_tolerance: RiskTolerance = RiskTolerance.MODERATE
    portfolio: List[Dict[str, Any]] = []
    watchlist: List[str] = []
    investment_horizon: str = "medium"

class Signal(BaseModel):
    symbol: str
    signal_type: str
    confidence: float
    reasoning: str
    sources: List[str] = []
    timestamp: datetime = datetime.now()

class AgentOutput(BaseModel):
    agent_name: str
    signal: Signal
    raw_analysis: str
    metrics: Dict[str, float] = {}

class SynthesizedRecommendation(BaseModel):
    symbol: str
    recommendation: str
    confidence: float
    reasoning_chain: List[str]
    agent_outputs: List[AgentOutput]
    risk_adjusted: bool
    timestamp: datetime = datetime.now()
