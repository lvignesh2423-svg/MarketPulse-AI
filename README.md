# FinOracle

### Multi-Agent Autonomous Financial Intelligence System for Retail Investors

[![IEEE HackVerse 2026](https://img.shields.io/badge/HackVerse-2026-orange)]()
[![Python](https://img.shields.io/badge/Python-3.10+-blue)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)]()

---

## Overview

**FinOracle** is an AI-powered multi-agent system that converts real-time market data, regulatory filings, and behavioral signals into explainable, personalized investment intelligence for retail investors.

> *"Bridging the gap between raw financial data and actionable decision-making"*

India's retail investment ecosystem fails not because data is unavailable, but because there's no infrastructure to convert continuous market events into timely, personalized, explainable guidance. **FinOracle** solves this.

---

## Key Features

### Multi-Agent Architecture
- **Technical Analyst** - Analyzes price momentum, RSI, volume anomalies, trends
- **Fundamental Analyst** - Evaluates P/E ratios, earnings, debt levels, profit margins  
- **Sentiment Analyst** - Processes news sentiment, market mood, analyst ratings
- **Synthesis Agent** - Combines all outputs with risk-adjusted weighting

### Explainable AI
- Full reasoning chain visible at every step
- Source attribution for regulatory context
- Transparent confidence scores

### Personalized Intelligence
- Risk profiles: Conservative, Moderate, Aggressive
- Different outputs for different risk tolerances
- Portfolio-aware recommendations

### Real-Time Market Data
- Live stock prices from Yahoo Finance
- Technical indicators (RSI, SMA, Volume)
- Support for Indian stocks (NSE: RELIANCE, TCS, INFY, etc.)

### RAG (Retrieval-Augmented Generation)
- Vector database with regulatory documents
- SEBI regulations and compliance context
- Source-cited analysis

### Performance Tracking
- Signal accuracy metrics
- Response latency monitoring
- Portfolio risk scoring

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, FastAPI, asyncio |
| AI/ML | Rule-based analysis, OpenRouter API |
| Data | Yahoo Finance, ChromaDB |
| Frontend | HTML5, CSS3, JavaScript, 3D animations |
| Storage | JSON logs, in-memory cache |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (3D Dashboard)            │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│              ORCHESTRATION LAYER (FastAPI)                  │
│         Coordinates agents, manages data flow              │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
┌───────▼───────┐    ┌───────▼───────┐    ┌───────▼───────┐
│   TECHNICAL   │    │  FUNDAMENTAL  │    │   SENTIMENT   │
│    ANALYST    │    │    ANALYST    │    │    ANALYST    │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    SYNTHESIS LAYER                          │
│         Risk-adjusted recommendation engine                │
└─────────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                               │
│  [Yahoo Finance] [RAG Database] [Performance Logs]         │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/FinOracle.git
cd FinOracle

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
cd backend
pip install -r requirements.txt
```

### Running the Application

```bash
# Start the backend server
python main.py

# Open frontend/index.html in your browser
```

The server runs on `http://localhost:8000`

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/analyze` | POST | Analyze a stock |
| `/api/market/{symbol}` | GET | Get market data |
| `/api/portfolio` | GET | Get portfolio |
| `/api/watchlist` | GET | Get watchlist |
| `/api/rag/query` | GET | Query RAG system |
| `/api/rag/context` | GET | Get regulatory context |
| `/api/performance` | GET | Get performance metrics |
| `/api/health` | GET | System health check |

### Example Request

```json
POST /api/analyze
{
  "symbol": "RELIANCE",
  "user_profile": {
    "user_id": "investor1",
    "name": "Demo User",
    "risk_tolerance": "moderate",
    "portfolio": [],
    "watchlist": [],
    "investment_horizon": "medium"
  }
}
```

---

## Supported Stocks

### Indian Stocks (NSE)
- RELIANCE (Reliance Industries)
- TCS (Tata Consultancy Services)
- INFY (Infosys)
- HDFCBANK (HDFC Bank)
- ICICIBANK (ICICI Bank)
- SBIN (State Bank of India)
- ITC (ITC Limited)
- WIPRO (Wipro)
- TATAMOTORS (Tata Motors)
- BAJFINANCE (Bajaj Finance)

### US Stocks
Any stock supported by Yahoo Finance (e.g., AAPL, GOOGL, MSFT)

---

## Features in Action

### Signal Classification
- Technical: RSI, volume analysis, trend detection
- Fundamental: P/E ratio, profit margins, debt levels
- Sentiment: News analysis, market mood

### Risk-Adjusted Outputs
| Risk Level | Multiplier | Behavior |
|------------|------------|----------|
| Conservative | 0.7x | Lower confidence, cautious |
| Moderate | 1.0x | Balanced |
| Aggressive | 1.3x | Higher confidence, action-oriented |

### Degraded Data Handling
- Graceful fallback when market data unavailable
- Default sentiment when news feed down
- Transparent handling of conflicting signals

---

## Performance Metrics

The system tracks three key metrics per session:

1. **Signal Accuracy** - Percentage of correct predictions
2. **Response Latency** - Time from request to response (target: <2s)
3. **Portfolio Risk Score** - Concentration and volatility measure (0-1)

---

## Project Structure

```
FinOracle/
├── backend/
│   ├── agents/              # AI agents
│   │   ├── technical_agent.py
│   │   ├── fundamental_agent.py
│   │   ├── sentiment_agent.py
│   │   └── synthesis_agent.py
│   ├── data/
│   │   ├── market_data.py   # Yahoo Finance integration
│   │   ├── rag_system.py    # Vector database
│   │   └── performance_logger.py
│   ├── models/
│   │   └── schemas.py       # Data models
│   ├── config.py            # Configuration
│   ├── llm_client.py        # LLM integration
│   ├── main.py              # FastAPI server
│   └── orchestrator.py      # Agent coordination
├── frontend/
│   ├── index.html           # 3D Dashboard
│   ├── styles.css           # Styling
│   ├── app.js               # Frontend logic
│   └── particles.js         # Particle effects
├── .env                     # API keys (not committed)
├── .gitignore
├── ARCHITECTURE.md          # Technical documentation
└── README.md
```

---

## Demo Scenarios

### Scenario 1: Basic Stock Analysis
1. Enter "RELIANCE" in search box
2. Select "Moderate" risk profile
3. Click "Analyze"
4. View multi-agent outputs with reasoning chain

### Scenario 2: Risk Profile Comparison
1. Analyze "TCS" with Conservative profile
2. Note the confidence level
3. Analyze "TCS" with Aggressive profile
4. Compare the different confidence levels

### Scenario 3: Different Stocks
1. Analyze RELIANCE, TCS, INFY
2. Compare different RSI values and signals
3. See how each stock gets unique analysis

---

## Hackathon Submission

**Event:** IEEE HackVerse 2026 - Into the Web
**Problem Statement:** PS-01 - Multi-Agent Autonomous Financial Intelligence System

### Requirements Checklist

- [x] Signal classification module (3+ dimensions)
- [x] RAG component with source attribution
- [x] Multi-agent architecture (3+ agents in parallel)
- [x] User profiling with risk modification
- [x] Live interface with signals and portfolio
- [x] Performance log (3+ metrics)
- [x] End-to-end demo scenario
- [x] Degraded data handling
- [x] Written architecture summary

---

## Known Limitations

1. Market data delayed by ~15 minutes (Yahoo Finance free tier)
2. Sentiment analysis uses rule-based approach (no LLM calls without credits)
3. Limited to NSE and NYSE stocks

---

## Future Enhancements

- [ ] Real-time WebSocket data feeds
- [ ] LLM-powered sentiment analysis
- [ ] Backtesting engine
- [ ] Mobile app
- [ ] Social trading features
- [ ] SEBI filing integration

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- IEEE Robotics & Automation Society, VIT Chennai
- Yahoo Finance API
- FastAPI framework
- The open-source community

---

