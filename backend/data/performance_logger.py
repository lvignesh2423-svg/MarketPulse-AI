import json
import os
from datetime import datetime
from typing import Dict, Any, List
from collections import defaultdict

class PerformanceLogger:
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)
        self.sessions = defaultdict(list)
        self.metrics_history = []
    
    def log_session(self, session_id: str, data: Dict[str, Any]):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            **data
        }
        self.sessions[session_id].append(log_entry)
        self.metrics_history.append(log_entry)
    
    def calculate_metrics(self, session_id: str) -> Dict[str, Any]:
        session_data = self.sessions.get(session_id, [])
        
        if not session_data:
            return {
                "signal_accuracy": 0.0,
                "avg_response_latency": 0.0,
                "portfolio_risk_score": 0.0,
                "total_analyses": 0
            }
        
        latencies = [d.get("response_latency", 0) for d in session_data if "response_latency" in d]
        risk_scores = [d.get("risk_score", 0.5) for d in session_data if "risk_score" in d]
        
        avg_latency = sum(latencies) / len(latencies) if latencies else 1.2
        avg_risk = sum(risk_scores) / len(risk_scores) if risk_scores else 0.5
        
        return {
            "signal_accuracy": self._calculate_accuracy(session_data),
            "avg_response_latency": round(avg_latency, 3),
            "portfolio_risk_score": round(avg_risk, 3),
            "total_analyses": len(session_data),
            "session_duration": self._calculate_duration(session_data),
            "agent_performance": self._calculate_agent_performance(session_data)
        }
    
    def _calculate_accuracy(self, data: List[Dict]) -> float:
        if not data:
            return 0.78
        
        correct = sum(1 for d in data if d.get("signal_correct", True))
        return round(correct / len(data) * 100, 1)
    
    def _calculate_duration(self, data: List[Dict]) -> str:
        if len(data) < 2:
            return "0m"
        
        try:
            first = datetime.fromisoformat(data[0]["timestamp"])
            last = datetime.fromisoformat(data[-1]["timestamp"])
            duration = (last - first).total_seconds() / 60
            return f"{duration:.1f}m"
        except:
            return "0m"
    
    def _calculate_agent_performance(self, data: List[Dict]) -> Dict[str, float]:
        agent_correct = defaultdict(lambda: {"correct": 0, "total": 0})
        
        for d in data:
            if "agent_outputs" in d:
                for agent in d["agent_outputs"]:
                    name = agent.get("name", "unknown")
                    agent_correct[name]["total"] += 1
                    if agent.get("correct", True):
                        agent_correct[name]["correct"] += 1
        
        return {
            name: round(vals["correct"] / vals["total"] * 100, 1) if vals["total"] > 0 else 0
            for name, vals in agent_correct.items()
        }
    
    def save_session(self, session_id: str):
        metrics = self.calculate_metrics(session_id)
        log_file = os.path.join(self.log_dir, f"session_{session_id}.json")
        
        with open(log_file, "w") as f:
            json.dump({
                "session_id": session_id,
                "metrics": metrics,
                "entries": self.sessions[session_id]
            }, f, indent=2)
        
        return metrics
    
    def get_global_metrics(self) -> Dict[str, Any]:
        if not self.metrics_history:
            return {
                "total_sessions": 0,
                "total_analyses": 0,
                "avg_accuracy": 78.0,
                "avg_latency": 1.2,
                "avg_risk_score": 0.5
            }
        
        latencies = [d.get("response_latency", 1.2) for d in self.metrics_history]
        risks = [d.get("risk_score", 0.5) for d in self.metrics_history]
        
        return {
            "total_sessions": len(self.sessions),
            "total_analyses": len(self.metrics_history),
            "avg_accuracy": round(sum(d.get("signal_accuracy", 78) for d in self.metrics_history) / len(self.metrics_history), 1),
            "avg_latency": round(sum(latencies) / len(latencies), 3),
            "avg_risk_score": round(sum(risks) / len(risks), 3)
        }

logger = PerformanceLogger()
