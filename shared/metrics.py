"""Prometheus-style Metrics & Monitoring"""

import time
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict
from datetime import datetime
import threading

class Counter:
    """Prometheus-style counter - only increases"""
    
    def __init__(self, name: str, help: str, labels: List[str] = None):
        self.name = name
        self.help = help
        self.labels = labels or []
        self._values: Dict[tuple, int] = defaultdict(int)
        self._lock = threading.Lock()
    
    def inc(self, amount: int = 1, **label_values):
        with self._lock:
            key = self._make_key(label_values)
            self._values[key] += amount
    
    def get(self, **label_values) -> int:
        key = self._make_key(label_values)
        return self._values.get(key, 0)
    
    def _make_key(self, label_values: dict) -> tuple:
        return tuple(label_values.get(l, "") for l in self.labels)
    
    def collect(self) -> str:
        lines = [f"# HELP {self.name} {self.help}", f"# TYPE {self.name} counter"]
        for key, value in self._values.items():
            labels = ",".join(f'{self.labels[i]}="{key[i]}"' for i in range(len(self.labels)))
            lines.append(f"{self.name}{{{labels}}} {value}")
        return "\n".join(lines)

class Gauge:
    """Prometheus-style gauge - can increase and decrease"""
    
    def __init__(self, name: str, help: str, labels: List[str] = None):
        self.name = name
        self.help = help
        self.labels = labels or []
        self._values: Dict[tuple, float] = defaultdict(float)
        self._lock = threading.Lock()
    
    def set(self, value: float, **label_values):
        with self._lock:
            key = self._make_key(label_values)
            self._values[key] = value
    
    def inc(self, amount: float = 1, **label_values):
        with self._lock:
            key = self._make_key(label_values)
            self._values[key] += amount
    
    def dec(self, amount: float = 1, **label_values):
        with self._lock:
            key = self._make_key(label_values)
            self._values[key] -= amount
    
    def get(self, **label_values) -> float:
        key = self._make_key(label_values)
        return self._values.get(key, 0.0)
    
    def _make_key(self, label_values: dict) -> tuple:
        return tuple(label_values.get(l, "") for l in self.labels)
    
    def collect(self) -> str:
        lines = [f"# HELP {self.name} {self.help}", f"# TYPE {self.name} gauge"]
        for key, value in self._values.items():
            labels = ",".join(f'{self.labels[i]}="{key[i]}"' for i in range(len(self.labels)))
            lines.append(f"{self.name}{{{labels}}} {value}")
        return "\n".join(lines)

class Histogram:
    """Prometheus-style histogram"""
    
    def __init__(self, name: str, help: str, buckets: List[float] = None, labels: List[str] = None):
        self.name = name
        self.help = help
        self.buckets = buckets or [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10]
        self.labels = labels or []
        self._buckets: Dict[tuple, List[int]] = defaultdict(lambda: [0] * (len(self.buckets) + 1))
        self._sum: Dict[tuple, float] = defaultdict(float)
        self._count: Dict[tuple, int] = defaultdict(int)
        self._lock = threading.Lock()
    
    def observe(self, value: float, **label_values):
        with self._lock:
            key = self._make_key(label_values)
            
            # Increment appropriate bucket
            for i, bound in enumerate(self.buckets):
                if value <= bound:
                    self._buckets[key][i] += 1
                    break
            else:
                self._buckets[key][-1] += 1
            
            self._sum[key] += value
            self._count[key] += 1
    
    def _make_key(self, label_values: dict) -> tuple:
        return tuple(label_values.get(l, "") for l in self.labels)
    
    def collect(self) -> str:
        lines = [f"# HELP {self.name} {self.help}", f"# TYPE {self.name} histogram"]
        for key, buckets in self._buckets.items():
            labels = ",".join(f'{self.labels[i]}="{key[i]}"' for i in range(len(self.labels)))
            
            for i, bound in enumerate(self.buckets):
                lines.append(f'{self.name}_bucket{{{labels},le="{bound}"}} {buckets[i]}')
            lines.append(f'{self.name}_bucket{{{labels},le="+Inf"}} {buckets[-1]}')
            lines.append(f"{self.name}_sum{{{labels}}} {self._sum[key]}")
            lines.append(f"{self.name}_count{{{labels}}} {self._count[key]}")
        return "\n".join(lines)

class MetricsRegistry:
    """Central metrics registry"""
    
    def __init__(self):
        self._metrics: Dict[str, any] = {}
        self._lock = threading.Lock()
    
    def counter(self, name: str, help: str, labels: List[str] = None) -> Counter:
        with self._lock:
            if name not in self._metrics:
                self._metrics[name] = Counter(name, help, labels)
            return self._metrics[name]
    
    def gauge(self, name: str, help: str, labels: List[str] = None) -> Gauge:
        with self._lock:
            if name not in self._metrics:
                self._metrics[name] = Gauge(name, help, labels)
            return self._metrics[name]
    
    def histogram(self, name: str, help: str, buckets: List[float] = None, labels: List[str] = None) -> Histogram:
        with self._lock:
            if name not in self._metrics:
                self._metrics[name] = Histogram(name, help, buckets, labels)
            return self._metrics[name]
    
    def collect_all(self) -> str:
        lines = []
        for metric in self._metrics.values():
            lines.append(metric.collect())
        return "\n".join(lines)

# Global metrics registry
_registry = MetricsRegistry()

# Pre-defined metrics
agent_requests = _registry.counter(
    "clawpack_agent_requests_total",
    "Total agent requests",
    ["agent", "status"]
)

tool_calls = _registry.counter(
    "clawpack_tool_calls_total",
    "Total tool calls",
    ["agent", "tool", "status"]
)

llm_requests = _registry.counter(
    "clawpack_llm_requests_total",
    "Total LLM requests",
    ["provider", "model", "cached"]
)

llm_tokens = _registry.counter(
    "clawpack_llm_tokens_total",
    "Total LLM tokens used",
    ["provider", "type"]
)

llm_duration = _registry.histogram(
    "clawpack_llm_duration_seconds",
    "LLM request duration",
    labels=["provider"]
)

tool_duration = _registry.histogram(
    "clawpack_tool_duration_seconds",
    "Tool execution duration",
    labels=["agent", "tool"]
)

active_agents = _registry.gauge(
    "clawpack_active_agents",
    "Currently active agents"
)

memory_files = _registry.gauge(
    "clawpack_memory_files_total",
    "Total memory files"
)

rate_limit_throttled = _registry.counter(
    "clawpack_rate_limit_throttled_total",
    "Total throttled requests"
)

def get_metrics() -> MetricsRegistry:
    return _registry

def export_metrics() -> str:
    return _registry.collect_all()
# Learning metrics for agent improvement
class LearningMetrics:
    def __init__(self):
        self.success_rates = {}
        self.pattern_effectiveness = {}
    
    def record_success(self, agent: str, pattern: str, success: bool):
        if agent not in self.success_rates:
            self.success_rates[agent] = {"success": 0, "total": 0}
        self.success_rates[agent]["total"] += 1
        if success:
            self.success_rates[agent]["success"] += 1
    
    def get_best_patterns(self, agent: str) -> list:
        return sorted(self.pattern_effectiveness.get(agent, {}).items(), 
                     key=lambda x: x[1], reverse=True)[:5]
