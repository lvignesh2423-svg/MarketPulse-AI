from data.market_data import market_service
from models.schemas import AgentOutput, Signal

SYSTEM_PROMPT = """You are a Technical Analyst AI agent. Analyze market data and provide technical analysis."""

def analyze_technical(symbol: str, market_data: dict) -> AgentOutput:
    rsi = market_data.get('rsi', 50)
    volume_ratio = market_data.get('volume_ratio', 1)
    price_change_pct = market_data.get('price_change_pct', 0)
    sma_20 = market_data.get('sma_20', 0)
    current_price = market_data.get('current_price', 0)
    
    score = 0
    reasons = []
    
    if rsi < 30:
        score += 2
        reasons.append(f"RSI oversold at {rsi}")
    elif rsi > 70:
        score -= 2
        reasons.append(f"RSI overbought at {rsi}")
    else:
        reasons.append(f"RSI neutral at {rsi}")
    
    if volume_ratio > 1.5:
        score += 1
        reasons.append(f"High volume ({volume_ratio}x avg)")
    elif volume_ratio < 0.5:
        score -= 1
        reasons.append(f"Low volume ({volume_ratio}x avg)")
    
    if current_price > sma_20:
        score += 1
        reasons.append("Price above SMA20 (bullish)")
    else:
        score -= 1
        reasons.append("Price below SMA20 (bearish)")
    
    if price_change_pct > 2:
        score += 1
        reasons.append(f"Strong momentum (+{price_change_pct}%)")
    elif price_change_pct < -2:
        score -= 1
        reasons.append(f"Negative momentum ({price_change_pct}%)")
    
    if score >= 2:
        signal_type = "BUY"
        confidence = min(0.6 + (score * 0.05), 0.85)
    elif score <= -2:
        signal_type = "SELL"
        confidence = min(0.6 + (abs(score) * 0.05), 0.85)
    else:
        signal_type = "HOLD"
        confidence = 0.5
    
    reasoning = f"Technical Analysis for {symbol}:\n" + "\n".join([f"- {r}" for r in reasons])
    reasoning += f"\nOverall Score: {score} -> {signal_type}"
    
    signal = Signal(
        symbol=symbol,
        signal_type=signal_type,
        confidence=confidence,
        reasoning=reasoning,
        sources=["Yahoo Finance Technical Data"]
    )
    
    return AgentOutput(
        agent_name="Technical Analyst",
        signal=signal,
        raw_analysis=reasoning,
        metrics={
            "rsi": market_data['rsi'],
            "volume_ratio": market_data['volume_ratio'],
            "price_momentum": market_data['price_change_pct']
        }
    )
