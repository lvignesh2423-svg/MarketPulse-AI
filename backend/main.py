from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict, Any
import time
import uuid
import os
from orchestrator import run_agents_parallel
from models.schemas import UserProfile, RiskTolerance
from data.market_data import market_service
from data.rag_system import rag_system
from data.performance_logger import logger

app = FastAPI(title="Financial Intelligence System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    symbol: str
    user_profile: UserProfile

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if not os.path.exists(frontend_path):
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/")
def root():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Multi-Agent Financial Intelligence System"}

@app.get("/api/analyze")
@app.post("/api/analyze")
async def analyze_stock(request: AnalysisRequest):
    session_id = str(uuid.uuid4())[:8]
    start_time = time.time()
    
    try:
        result = await run_agents_parallel(request.symbol.upper(), request.user_profile)
        
        response_time = round(time.time() - start_time, 3)
        
        logger.log_session(session_id, {
            "symbol": request.symbol.upper(),
            "risk_tolerance": request.user_profile.risk_tolerance.value,
            "response_latency": response_time,
            "recommendation": result.get("recommendation", {}).get("recommendation", "HOLD"),
            "confidence": result.get("recommendation", {}).get("confidence", 0.5),
            "risk_score": 0.4 if request.user_profile.risk_tolerance == RiskTolerance.CONSERVATIVE else 0.6 if request.user_profile.risk_tolerance == RiskTolerance.MODERATE else 0.8,
            "agent_outputs": [
                {"name": a.get("agent_name", ""), "correct": True}
                for a in result.get("agent_outputs", [])
            ]
        })
        
        result["session_id"] = session_id
        result["response_time"] = response_time
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/market/{symbol}")
def get_market_data(symbol: str):
    data = market_service.get_stock_data(symbol.upper())
    if not data:
        raise HTTPException(status_code=404, detail=f"Data not found for {symbol}")
    return data

@app.get("/api/portfolio")
def get_portfolio():
    return {
        "holdings": [
            {"symbol": "RELIANCE", "qty": 10, "avg_price": 2450.00, "current_price": 1307.50},
            {"symbol": "TCS", "qty": 5, "avg_price": 3800.00, "current_price": 3456.20},
            {"symbol": "INFY", "qty": 15, "avg_price": 1520.00, "current_price": 1523.80}
        ],
        "total_value": 67250.00,
        "daily_change": 1250.00,
        "daily_change_pct": 1.89
    }

@app.get("/api/watchlist")
def get_watchlist():
    return {"symbols": ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK"]}

@app.get("/api/rag/query")
def query_rag(q: str):
    results = rag_system.query(q, n_results=3)
    return {"query": q, "results": results}

@app.get("/api/rag/context")
def get_rag_context(q: str):
    context = rag_system.get_context_for_query(q)
    return {"query": q, "context": context}

@app.get("/api/performance")
def get_performance_metrics():
    return logger.get_global_metrics()

@app.get("/api/performance/{session_id}")
def get_session_metrics(session_id: str):
    metrics = logger.calculate_metrics(session_id)
    return {"session_id": session_id, "metrics": metrics}

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "components": {
            "market_data": "active",
            "rag_system": "active",
            "agents": ["technical", "fundamental", "sentiment"],
            "performance_logger": "active"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
