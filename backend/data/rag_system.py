from typing import List, Dict, Any

class SimpleRAG:
    def __init__(self):
        self.documents = [
            {
                "id": "sebi_1",
                "text": "SEBI regulations require all listed companies to disclose material events to stock exchanges within 30 minutes. This ensures transparency and protects retail investors from information asymmetry.",
                "source": "SEBI Regulations",
                "topic": "disclosure"
            },
            {
                "id": "sebi_2",
                "text": "SEBI's 2024 data shows 89% of retail F&O participants in India lose money. The regulatory body has introduced margin requirements and position limits to protect retail traders.",
                "source": "SEBI Report 2024",
                "topic": "retail_trading"
            },
            {
                "id": "earnings_1",
                "text": "Quarterly earnings reports should be analyzed for revenue growth, profit margins, EBITDA, and guidance. Consistent revenue growth above 15% YoY indicates strong business fundamentals.",
                "source": "Earnings Analysis Guide",
                "topic": "fundamentals"
            },
            {
                "id": "technical_1",
                "text": "RSI above 70 indicates overbought conditions, while below 30 indicates oversold. Volume confirmation is essential - price moves on high volume are more reliable than low volume moves.",
                "source": "Technical Analysis Guide",
                "topic": "indicators"
            },
            {
                "id": "macro_1",
                "text": "FII (Foreign Institutional Investor) flows are key indicators of market sentiment. Consistent FII buying often precedes bull markets, while sustained selling may indicate bearish outlook.",
                "source": "Market Analysis",
                "topic": "institutional_flows"
            },
            {
                "id": "risk_1",
                "text": "Portfolio diversification across sectors and market caps reduces risk. A concentrated portfolio with more than 25% in a single stock increases idiosyncratic risk significantly.",
                "source": "Risk Management",
                "topic": "portfolio"
            },
            {
                "id": "fii_1",
                "text": "FII ownership patterns in Indian markets show increased participation in IT, Banking, and FMCG sectors. Changes in FII holdings often signal institutional confidence in sector growth.",
                "source": "FII Analysis",
                "topic": "institutional_investment"
            },
            {
                "id": "options_1",
                "text": "Options chain analysis reveals market sentiment. High put-call ratio suggests bearish sentiment, while low ratio indicates bullish outlook. Max pain level acts as support/resistance.",
                "source": "Options Analysis",
                "topic": "derivatives"
            }
        ]
    
    def _simple_similarity(self, query: str, text: str) -> float:
        query_words = set(query.lower().split())
        text_words = set(text.lower().split())
        intersection = query_words.intersection(text_words)
        return len(intersection) / len(query_words) if query_words else 0
    
    def query(self, query_text: str, n_results: int = 3) -> List[Dict[str, Any]]:
        scored_docs = []
        for doc in self.documents:
            score = self._simple_similarity(query_text, doc["text"])
            scored_docs.append({
                "text": doc["text"],
                "source": doc["source"],
                "topic": doc["topic"],
                "relevance_score": round(score, 3)
            })
        
        scored_docs.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored_docs[:n_results]
    
    def get_context_for_query(self, query_text: str) -> str:
        results = self.query(query_text, n_results=2)
        if not results:
            return "No relevant regulatory or analytical context available."
        
        context_parts = []
        for r in results:
            context_parts.append(f"[Source: {r['source']}] {r['text']}")
        
        return "\n\n".join(context_parts)

rag_system = SimpleRAG()
