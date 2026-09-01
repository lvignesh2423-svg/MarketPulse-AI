from typing import List
from models.schemas import AgentOutput, SynthesizedRecommendation, UserProfile, RiskTolerance

def synthesize_recommendation(
    symbol: str,
    agent_outputs: List[AgentOutput],
    user_profile: UserProfile
) -> SynthesizedRecommendation:
    
    risk_multiplier = {
        RiskTolerance.CONSERVATIVE: 0.7,
        RiskTolerance.MODERATE: 1.0,
        RiskTolerance.AGGRESSIVE: 1.3
    }
    
    scores = {"BUY": 0, "SELL": 0, "HOLD": 0}
    for output in agent_outputs:
        signal = output.signal.signal_type.upper()
        if signal in ["BUY", "POSITIVE"]:
            scores["BUY"] += output.signal.confidence
        elif signal in ["SELL", "NEGATIVE"]:
            scores["SELL"] += output.signal.confidence
        else:
            scores["HOLD"] += output.signal.confidence
    
    reasoning_chain = []
    for output in agent_outputs:
        reasoning_chain.append(f"{output.agent_name}: {output.signal.signal_type} ({output.signal.confidence*100:.0f}% confidence)")
    
    if scores["BUY"] > scores["SELL"] and scores["BUY"] > scores["HOLD"]:
        recommendation = "BUY"
        confidence = scores["BUY"] / len(agent_outputs)
    elif scores["SELL"] > scores["BUY"] and scores["SELL"] > scores["HOLD"]:
        recommendation = "SELL"
        confidence = scores["SELL"] / len(agent_outputs)
    else:
        recommendation = "HOLD"
        confidence = scores["HOLD"] / len(agent_outputs)
    
    adjusted_confidence = min(confidence * risk_multiplier[user_profile.risk_tolerance], 0.95)
    
    if recommendation == "BUY":
        agree_signals = ["BUY", "POSITIVE"]
    elif recommendation == "SELL":
        agree_signals = ["SELL", "NEGATIVE"]
    else:
        agree_signals = ["HOLD", "NEUTRAL"]
    
    agreeing = sum(1 for output in agent_outputs if output.signal.signal_type.upper() in agree_signals)
    
    reasoning_chain.append(f"Synthesis: {recommendation} - {agreeing}/{len(agent_outputs)} agents agree")
    reasoning_chain.append(f"Risk adjustment for {user_profile.risk_tolerance.value}: {risk_multiplier[user_profile.risk_tolerance]}x")
    reasoning_chain.append(f"Final confidence: {adjusted_confidence*100:.1f}%")
    
    return SynthesizedRecommendation(
        symbol=symbol,
        recommendation=recommendation,
        confidence=adjusted_confidence,
        reasoning_chain=reasoning_chain,
        agent_outputs=agent_outputs,
        risk_adjusted=(user_profile.risk_tolerance != RiskTolerance.MODERATE)
    )
