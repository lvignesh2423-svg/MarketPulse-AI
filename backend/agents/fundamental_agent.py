from models.schemas import AgentOutput, Signal
import yfinance as yf
from data.rag_system import rag_system

INDIAN_STOCKS = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "ITC", "WIPRO", "TATAMOTORS", "BAJFINANCE"]

def analyze_fundamental(symbol: str) -> AgentOutput:
    try:
        yf_symbol = f"{symbol}.NS" if symbol.upper() in INDIAN_STOCKS else symbol
        ticker = yf.Ticker(yf_symbol)
        info = ticker.info
        
        pe_ratio = info.get('trailingPE', None)
        profit_margin = info.get('profitMargins', None)
        debt_equity = info.get('debtToEquity', None)
        dividend_yield = info.get('dividendYield', None)
        
        rag_context = rag_system.get_context_for_query(f"fundamental analysis {symbol} earnings valuation")
        
        score = 0
        reasons = []
        
        if pe_ratio:
            if pe_ratio < 15:
                score += 2
                reasons.append(f"Attractive P/E ratio: {pe_ratio:.1f}")
            elif pe_ratio < 25:
                score += 1
                reasons.append(f"Reasonable P/E ratio: {pe_ratio:.1f}")
            elif pe_ratio > 40:
                score -= 2
                reasons.append(f"High P/E ratio: {pe_ratio:.1f}")
            else:
                reasons.append(f"P/E ratio: {pe_ratio:.1f}")
        
        if profit_margin:
            if profit_margin > 0.2:
                score += 2
                reasons.append(f"Strong profit margin: {profit_margin*100:.1f}%")
            elif profit_margin > 0.1:
                score += 1
                reasons.append(f"Good profit margin: {profit_margin*100:.1f}%")
            else:
                reasons.append(f"Profit margin: {profit_margin*100:.1f}%")
        
        if debt_equity:
            if debt_equity < 50:
                score += 1
                reasons.append(f"Low debt: {debt_equity:.1f}")
            elif debt_equity > 150:
                score -= 1
                reasons.append(f"High debt: {debt_equity:.1f}")
        
        if dividend_yield and dividend_yield > 0.02:
            score += 1
            reasons.append(f"Dividend yield: {dividend_yield*100:.2f}%")
        
        if score >= 3:
            signal_type = "BUY"
            confidence = 0.75
        elif score <= -2:
            signal_type = "SELL"
            confidence = 0.65
        else:
            signal_type = "HOLD"
            confidence = 0.55
        
        reasoning = f"Fundamental Analysis for {symbol} ({info.get('longName', 'Unknown')}):\n"
        reasoning += "\n".join([f"- {r}" for r in reasons])
        reasoning += f"\n\n[Regulatory Context]: {rag_context[:200]}..."
        reasoning += f"\nFundamental Score: {score} -> {signal_type}"
        
        signal = Signal(
            symbol=symbol,
            signal_type=signal_type,
            confidence=confidence,
            reasoning=reasoning,
            sources=["Yahoo Finance Fundamentals", "SEBI Regulatory Database"]
        )
        
        return AgentOutput(
            agent_name="Fundamental Analyst",
            signal=signal,
            raw_analysis=reasoning,
            metrics={
                "pe_ratio": pe_ratio or 0,
                "profit_margin": profit_margin or 0,
                "debt_equity": debt_equity or 0
            }
        )
    except Exception as e:
        return AgentOutput(
            agent_name="Fundamental Analyst",
            signal=Signal(symbol=symbol, signal_type="HOLD", confidence=0.3, reasoning=f"Error: {str(e)}"),
            raw_analysis=f"Unable to fetch fundamental data: {str(e)}",
            metrics={}
        )
