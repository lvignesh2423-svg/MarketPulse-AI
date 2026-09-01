from models.schemas import AgentOutput, Signal

def analyze_sentiment(symbol: str, news_data: list = None) -> AgentOutput:
    reasons = []
    score = 0
    
    if news_data and len(news_data) > 0:
        positive_words = ["surge", "rally", "gain", "profit", "growth", "bullish", "upgrade", "beat"]
        negative_words = ["crash", "drop", "loss", "decline", "bearish", "downgrade", "miss", "fall"]
        
        for news in news_data[:5]:
            news_lower = news.lower()
            if any(word in news_lower for word in positive_words):
                score += 1
                reasons.append(f"Positive: {news[:50]}...")
            elif any(word in news_lower for word in negative_words):
                score -= 1
                reasons.append(f"Negative: {news[:50]}...")
    else:
        reasons.append("No recent news data available")
        reasons.append("Using general market conditions")
        score = 0
    
    if score >= 2:
        sentiment = "POSITIVE"
        confidence = 0.7
    elif score <= -2:
        sentiment = "NEGATIVE"
        confidence = 0.65
    else:
        sentiment = "NEUTRAL"
        confidence = 0.5
    
    reasoning = f"Sentiment Analysis for {symbol}:\n"
    reasoning += "\n".join([f"- {r}" for r in reasons])
    reasoning += f"\nSentiment Score: {score} -> {sentiment}"
    
    signal = Signal(
        symbol=symbol,
        signal_type=sentiment,
        confidence=confidence,
        reasoning=reasoning,
        sources=["Market News Analysis"]
    )
    
    return AgentOutput(
        agent_name="Sentiment Analyst",
        signal=signal,
        raw_analysis=reasoning,
        metrics={
            "sentiment_score": score,
            "news_coverage": len(news_data) if news_data else 0
        }
    )
