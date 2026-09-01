from typing import List
from models.schemas import AgentOutput, UserProfile
from agents.technical_agent import analyze_technical
from agents.fundamental_agent import analyze_fundamental
from agents.sentiment_agent import analyze_sentiment
from agents.synthesis_agent import synthesize_recommendation
from data.market_data import market_service
import asyncio
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(max_workers=3)

async def run_agents_parallel(symbol: str, user_profile: UserProfile) -> dict:
    market_data = market_service.get_stock_data(symbol)
    
    if not market_data:
        return {"error": f"Unable to fetch market data for {symbol}"}
    
    loop = asyncio.get_event_loop()
    
    technical_task = loop.run_in_executor(executor, analyze_technical, symbol, market_data)
    fundamental_task = loop.run_in_executor(executor, analyze_fundamental, symbol)
    sentiment_task = loop.run_in_executor(executor, analyze_sentiment, symbol)
    
    technical_output, fundamental_output, sentiment_output = await asyncio.gather(
        technical_task, fundamental_task, sentiment_task
    )
    
    agent_outputs = [technical_output, fundamental_output, sentiment_output]
    
    recommendation = synthesize_recommendation(symbol, agent_outputs, user_profile)
    
    return {
        "market_data": market_data,
        "agent_outputs": [output.dict() for output in agent_outputs],
        "recommendation": recommendation.dict()
    }
