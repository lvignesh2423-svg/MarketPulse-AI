# Multi-Agent Financial Intelligence System
## Architecture & Decision Logic Summary

### System Overview

A multi-agent AI system that converts real-time market data, regulatory filings, and behavioral signals into explainable, personalized investment intelligence for retail investors.

---

## Agent Architecture

### 1. Technical Analyst Agent
- **Input**: Price history, volume data, technical indicators (RSI, SMA, MACD)
- **Processing**: Rule-based analysis of momentum, trend, and volume anomalies
- **Output**: BUY/SELL/HOLD signal with confidence score
- **Sources**: Yahoo Finance real-time data

### 2. Fundamental Analyst Agent  
- **Input**: P/E ratio, profit margins, debt levels, dividend yield, earnings data
- **Processing**: Valuation analysis against sector benchmarks
- **Output**: BUY/SELL/HOLD signal with confidence score
- **Sources**: Yahoo Finance fundamentals + SEBI regulatory database (via RAG)

### 3. Sentiment Analyst Agent
- **Input**: News sentiment, social media trends, analyst ratings
- **Processing**: Natural language analysis of market sentiment
- **Output**: POSITIVE/NEGATIVE/NEUTRAL sentiment with confidence score
- **Sources**: Market news analysis + sentiment indicators

### 4. Synthesis Agent
- **Input**: Outputs from all 3 analyst agents
- **Processing**: Weighted aggregation based on user risk profile
- **Output**: Final recommendation with reasoning chain
- **Risk Adjustment**: Conservative (0.7x), Moderate (1.0x), Aggressive (1.3x)

---

## Data Pipeline

```
[Market Data API] → [Data Ingestion] → [Parallel Agent Processing]
                                            ↓
[Document Corpus] → [RAG Retrieval] → [Agent Enhancement]
                                            ↓
[User Profile] → [Risk Adjustment] → [Synthesis Layer]
                                            ↓
[Performance Logger] → [Metrics Storage] → [Dashboard Display]
```

---

## Minimum Requirements Checklist

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Signal classification (3+ dimensions) | ✅ | Technical, Fundamental, Sentiment agents |
| RAG component with source attribution | ✅ | ChromaDB vector store + document corpus |
| Multi-agent architecture (3+ agents) | ✅ | Technical, Fundamental, Sentiment agents in parallel |
| User profiling with risk modification | ✅ | Risk tolerance affects agent weighting |
| Live interface with signals and portfolio | ✅ | Real-time dashboard with all components |
| Performance log (3+ metrics) | ✅ | Signal accuracy, response latency, risk score |
| End-to-end demo scenario | ✅ | Full pipeline from data to recommendation |
| Degraded data handling | ✅ | Graceful fallback when data unavailable |
| Written architecture summary | ✅ | This document |

---

## Degraded Data Handling

### Scenario 1: Market Data Unavailable
- System returns cached data or gracefully degrades
- Technical agent uses last known values
- Other agents continue with available data

### Scenario 2: News Feed Down
- Sentiment agent defaults to NEUTRAL with lower confidence
- Reasoning chain explains the limitation
- Other agents unaffected

### Scenario 3: Conflicting Agent Signals
- Synthesis agent weights by confidence levels
- Shows disagreement in reasoning chain
- User sees full transparency

---

## Performance Metrics

1. **Signal Accuracy**: Percentage of correct predictions (backtested)
2. **Response Latency**: Time from request to response (target: <2s)
3. **Portfolio Risk Score**: Concentration and volatility measure (0-1)

---

## Technology Stack

- **Backend**: Python, FastAPI, asyncio
- **AI/ML**: OpenRouter API, rule-based analysis
- **Data**: Yahoo Finance, ChromaDB vector store
- **Frontend**: HTML5, CSS3, JavaScript, 3D animations
- **Storage**: JSON logs, in-memory cache

---

## User Flow

1. User enters stock symbol and selects risk profile
2. System fetches real-time market data
3. Three agents analyze in parallel (<1s each)
4. RAG system provides regulatory context
5. Synthesis agent combines outputs with risk adjustment
6. Full reasoning chain displayed to user
7. Performance metrics logged for analysis

---

## Key Differentiators

1. **Multi-perspective analysis**: Not just one view, but three independent analyses
2. **Explainable AI**: Full reasoning chain visible at every step
3. **Personalized**: Risk profile affects recommendations
4. **Regulatory grounded**: RAG system cites SEBI regulations
5. **Performance tracked**: Metrics logged for continuous improvement

---

*Architecture prepared for IEEE HackVerse 2026 - PS-01*
