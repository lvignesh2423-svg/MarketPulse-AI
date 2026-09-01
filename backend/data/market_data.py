import yfinance as yf
import pandas as pd
from typing import Dict, Any, Optional
from datetime import datetime, timedelta

class MarketDataService:
    INDIAN_STOCKS = ["RELIANCE", "TCS", "INFY", "HDFCBANK", "ICICIBANK", "SBIN", "ITC", "WIPRO", "TATAMOTORS", "BAJFINANCE"]
    
    def __init__(self):
        self.cache = {}
    
    def get_stock_data(self, symbol: str, period: str = "3mo") -> Optional[Dict[str, Any]]:
        try:
            yf_symbol = f"{symbol}.NS" if symbol.upper() in self.INDIAN_STOCKS else symbol
            ticker = yf.Ticker(yf_symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                return None
            
            current_price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            volume = hist['Volume'].iloc[-1]
            avg_volume = hist['Volume'].mean()
            
            sma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
            sma_50 = hist['Close'].rolling(window=50).mean().iloc[-1] if len(hist) >= 50 else None
            
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean().iloc[-1]
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean().iloc[-1]
            rs = gain / loss if loss != 0 else 0
            rsi = 100 - (100 / (1 + rs))
            
            return {
                "symbol": symbol,
                "current_price": round(current_price, 2),
                "price_change": round(current_price - prev_price, 2),
                "price_change_pct": round(((current_price - prev_price) / prev_price) * 100, 2),
                "volume": int(volume),
                "avg_volume": int(avg_volume),
                "volume_ratio": round(volume / avg_volume, 2) if avg_volume > 0 else 0,
                "sma_20": round(sma_20, 2),
                "sma_50": round(sma_50, 2) if sma_50 else None,
                "rsi": round(rsi, 2),
                "period_high": round(hist['High'].max(), 2),
                "period_low": round(hist['Low'].min(), 2),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
    
    def get_multiple_stocks(self, symbols: list) -> Dict[str, Any]:
        results = {}
        for symbol in symbols:
            data = self.get_stock_data(symbol)
            if data:
                results[symbol] = data
        return results

market_service = MarketDataService()
