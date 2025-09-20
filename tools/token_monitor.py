#!/usr/bin/env python3
"""
Advanced Token Monitoring and Circuit Breaker System

Real-time token usage monitoring with automatic optimization switching
and predictive budget management.
"""

import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class OptimizationLevel(Enum):
    STANDARD = "standard"
    OPTIMIZED = "optimized" 
    LIGHTWEIGHT = "lightweight"
    EMERGENCY = "emergency"
    SKELETON = "skeleton"

@dataclass
class TokenUsageMetrics:
    timestamp: datetime
    tokens_used: int
    component: str  # 'directive', 'tools', 'memory', 'response'
    interaction_id: str
    optimization_level: OptimizationLevel

@dataclass
class BudgetAlert:
    level: str  # 'warning', 'critical', 'emergency'
    message: str
    recommended_action: str
    timestamp: datetime

class TokenCircuitBreaker:
    """Implements circuit breaker pattern for token usage protection."""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 300):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func, *args, **kwargs):
        """Execute function with circuit breaker protection."""
        if self.state == "OPEN":
            if self._should_attempt_reset():
                self.state = "HALF_OPEN"
            else:
                raise Exception("Circuit breaker is OPEN - too many token budget violations")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _should_attempt_reset(self) -> bool:
        return (time.time() - self.last_failure_time) >= self.recovery_timeout
    
    def _on_success(self):
        self.failure_count = 0
        self.state = "CLOSED"
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"

class TokenMonitor:
    """Advanced token usage monitoring and optimization system."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path) if config_path else Path.home() / ".ai-mcp-framework" / "token_monitor_config.json"
        self.metrics_file = Path.home() / ".ai-mcp-framework" / "token_metrics.jsonl"
        self.alerts_file = Path.home() / ".ai-mcp-framework" / "token_alerts.json"
        
        # Ensure directory exists
        self.config_path.parent.mkdir(exist_ok=True)
        
        self.config = self._load_config()
        self.metrics: List[TokenUsageMetrics] = []
        self.alerts: List[BudgetAlert] = []
        self.circuit_breaker = TokenCircuitBreaker()
        self.current_optimization = OptimizationLevel.STANDARD
        
        # Real-time monitoring
        self._monitoring = False
        self._monitor_thread = None
        
        # Load existing metrics
        self._load_metrics()
    
    def _load_config(self) -> Dict:
        """Load or create default configuration."""
        default_config = {
            "daily_budget": 50000,
            "hourly_budget": 5000,
            "warning_threshold": 0.8,  # 80% of budget
            "critical_threshold": 0.95,  # 95% of budget
            "auto_optimization": True,
            "optimization_thresholds": {
                "optimized": 0.7,      # Switch to optimized at 70%
                "lightweight": 0.85,   # Switch to lightweight at 85% 
                "emergency": 0.95,     # Switch to emergency at 95%
                "skeleton": 0.98       # Switch to skeleton at 98%
            },
            "component_limits": {
                "directive": 1000,     # Max tokens for directive loading
                "tools": 2000,         # Max tokens for tool operations
                "memory": 1500,        # Max tokens for memory queries
                "response": 3000       # Max tokens for response generation
            }
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except Exception as e:
                print(f"⚠️  Error loading config, using defaults: {e}")
        
        # Save default config
        with open(self.config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    def _load_metrics(self):
        """Load existing metrics from file."""
        if not self.metrics_file.exists():
            return
        
        try:
            with open(self.metrics_file, 'r') as f:
                for line in f:
                    if line.strip():
                        data = json.loads(line)
                        metric = TokenUsageMetrics(
                            timestamp=datetime.fromisoformat(data['timestamp']),
                            tokens_used=data['tokens_used'],
                            component=data['component'],
                            interaction_id=data['interaction_id'],
                            optimization_level=OptimizationLevel(data['optimization_level'])
                        )
                        self.metrics.append(metric)
        except Exception as e:
            print(f"⚠️  Error loading metrics: {e}")
    
    def record_usage(self, tokens_used: int, component: str, interaction_id: str = None):
        """Record token usage for a component."""
        if interaction_id is None:
            interaction_id = f"interaction_{int(time.time())}"
        
        metric = TokenUsageMetrics(
            timestamp=datetime.now(),
            tokens_used=tokens_used,
            component=component,
            interaction_id=interaction_id,
            optimization_level=self.current_optimization
        )
        
        self.metrics.append(metric)
        self._save_metric(metric)
        
        # Check budgets and trigger alerts if needed
        self._check_budgets()
        
        # Auto-optimize if enabled
        if self.config.get('auto_optimization', True):
            self._auto_optimize()
    
    def _save_metric(self, metric: TokenUsageMetrics):
        """Append metric to file."""
        try:
            with open(self.metrics_file, 'a') as f:
                data = {
                    'timestamp': metric.timestamp.isoformat(),
                    'tokens_used': metric.tokens_used,
                    'component': metric.component,
                    'interaction_id': metric.interaction_id,
                    'optimization_level': metric.optimization_level.value
                }
                f.write(json.dumps(data) + '\n')
        except Exception as e:
            print(f"⚠️  Error saving metric: {e}")
    
    def _check_budgets(self):
        """Check current usage against budgets and generate alerts."""
        now = datetime.now()
        
        # Daily usage
        daily_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        daily_usage = self._get_usage_since(daily_start)
        daily_budget = self.config['daily_budget']
        daily_utilization = daily_usage / daily_budget if daily_budget > 0 else 0
        
        # Hourly usage  
        hourly_start = now.replace(minute=0, second=0, microsecond=0)
        hourly_usage = self._get_usage_since(hourly_start)
        hourly_budget = self.config['hourly_budget']
        hourly_utilization = hourly_usage / hourly_budget if hourly_budget > 0 else 0
        
        # Generate alerts based on thresholds
        max_utilization = max(daily_utilization, hourly_utilization)
        
        if max_utilization >= self.config['critical_threshold']:
            self._create_alert(
                'critical',
                f"Token usage at {max_utilization:.1%} of budget",
                "Switch to emergency mode immediately"
            )
        elif max_utilization >= self.config['warning_threshold']:
            self._create_alert(
                'warning', 
                f"Token usage at {max_utilization:.1%} of budget",
                "Consider switching to optimized mode"
            )
    
    def _get_usage_since(self, since: datetime) -> int:
        """Get total token usage since specified time."""
        return sum(
            m.tokens_used for m in self.metrics 
            if m.timestamp >= since
        )
    
    def _create_alert(self, level: str, message: str, action: str):
        """Create and save alert."""
        alert = BudgetAlert(
            level=level,
            message=message,
            recommended_action=action,
            timestamp=datetime.now()
        )
        
        self.alerts.append(alert)
        
        # Save alerts to file
        try:
            alerts_data = [
                {
                    'level': a.level,
                    'message': a.message,
                    'recommended_action': a.recommended_action,
                    'timestamp': a.timestamp.isoformat()
                }
                for a in self.alerts[-10:]  # Keep last 10 alerts
            ]
            with open(self.alerts_file, 'w') as f:
                json.dump(alerts_data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Error saving alerts: {e}")
        
        print(f"🚨 {level.upper()}: {message} - {action}")
    
    def _auto_optimize(self):
        """Automatically switch optimization levels based on usage."""
        now = datetime.now()
        daily_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        daily_usage = self._get_usage_since(daily_start)
        daily_budget = self.config['daily_budget']
        utilization = daily_usage / daily_budget if daily_budget > 0 else 0
        
        thresholds = self.config['optimization_thresholds']
        
        new_level = self.current_optimization
        
        if utilization >= thresholds['skeleton']:
            new_level = OptimizationLevel.SKELETON
        elif utilization >= thresholds['emergency']:
            new_level = OptimizationLevel.EMERGENCY
        elif utilization >= thresholds['lightweight']:
            new_level = OptimizationLevel.LIGHTWEIGHT
        elif utilization >= thresholds['optimized']:
            new_level = OptimizationLevel.OPTIMIZED
        else:
            new_level = OptimizationLevel.STANDARD
        
        if new_level != self.current_optimization:
            print(f"🔄 Auto-switching from {self.current_optimization.value} to {new_level.value} mode")
            self.current_optimization = new_level
            self._apply_optimization_level(new_level)
    
    def _apply_optimization_level(self, level: OptimizationLevel):
        """Apply the specified optimization level."""
        # This would integrate with your deployment system
        print(f"🚀 Applying {level.value} optimization level")
        
        # Example: Call deploy-smart-framework.py with appropriate flags
        import subprocess
        try:
            framework_dir = Path(__file__).parent.parent
            deploy_script = framework_dir / "tools" / "deploy-smart-framework.py"
            
            if deploy_script.exists():
                cmd = ["python", str(deploy_script), "--optimization", level.value, "--silent"]
                subprocess.run(cmd, check=True)
                print(f"✅ Successfully applied {level.value} optimization")
            else:
                print(f"⚠️  Deploy script not found at {deploy_script}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error applying optimization: {e}")
    
    def get_current_status(self) -> Dict:
        """Get current monitoring status and metrics."""
        now = datetime.now()
        
        # Daily metrics
        daily_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        daily_usage = self._get_usage_since(daily_start)
        daily_budget = self.config['daily_budget']
        
        # Hourly metrics
        hourly_start = now.replace(minute=0, second=0, microsecond=0)
        hourly_usage = self._get_usage_since(hourly_start)
        hourly_budget = self.config['hourly_budget']
        
        # Component breakdown
        component_usage = {}
        for component in ['directive', 'tools', 'memory', 'response']:
            component_usage[component] = sum(
                m.tokens_used for m in self.metrics[-50:]  # Last 50 interactions
                if m.component == component
            )
        
        return {
            'current_optimization': self.current_optimization.value,
            'circuit_breaker_state': self.circuit_breaker.state,
            'daily_usage': {
                'used': daily_usage,
                'budget': daily_budget,
                'utilization': daily_usage / daily_budget if daily_budget > 0 else 0,
                'remaining': max(0, daily_budget - daily_usage)
            },
            'hourly_usage': {
                'used': hourly_usage,
                'budget': hourly_budget,
                'utilization': hourly_usage / hourly_budget if hourly_budget > 0 else 0,
                'remaining': max(0, hourly_budget - hourly_usage)
            },
            'component_breakdown': component_usage,
            'recent_alerts': [
                {
                    'level': a.level,
                    'message': a.message,
                    'timestamp': a.timestamp.isoformat()
                }
                for a in self.alerts[-5:]  # Last 5 alerts
            ],
            'total_interactions': len(set(m.interaction_id for m in self.metrics)),
            'monitoring_active': self._monitoring
        }
    
    def start_monitoring(self):
        """Start real-time monitoring thread."""
        if self._monitoring:
            return
        
        self._monitoring = True
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        print("🔍 Token monitoring started")
    
    def stop_monitoring(self):
        """Stop real-time monitoring."""
        self._monitoring = False
        if self._monitor_thread:
            self._monitor_thread.join()
        print("⏹️  Token monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop."""
        while self._monitoring:
            try:
                # Periodic checks (every 30 seconds)
                self._check_budgets()
                time.sleep(30)
            except Exception as e:
                print(f"⚠️  Monitoring error: {e}")
                time.sleep(60)  # Back off on error

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Advanced Token Monitoring System")
    parser.add_argument("--start-monitoring", action="store_true", help="Start real-time monitoring")
    parser.add_argument("--status", action="store_true", help="Show current status")
    parser.add_argument("--record-usage", type=int, help="Record token usage for testing")
    parser.add_argument("--component", default="test", help="Component name for usage recording")
    parser.add_argument("--config", help="Path to configuration file")
    
    args = parser.parse_args()
    
    monitor = TokenMonitor(args.config)
    
    if args.record_usage:
        monitor.record_usage(args.record_usage, args.component)
        print(f"✅ Recorded {args.record_usage} tokens for {args.component}")
    
    if args.status:
        status = monitor.get_current_status()
        print("\n=== Token Monitor Status ===")
        print(f"Current Optimization: {status['current_optimization']}")
        print(f"Circuit Breaker: {status['circuit_breaker_state']}")
        print(f"\nDaily Usage: {status['daily_usage']['used']:,} / {status['daily_usage']['budget']:,} ({status['daily_usage']['utilization']:.1%})")
        print(f"Hourly Usage: {status['hourly_usage']['used']:,} / {status['hourly_usage']['budget']:,} ({status['hourly_usage']['utilization']:.1%})")
        
        print("\nComponent Breakdown:")
        for component, usage in status['component_breakdown'].items():
            print(f"  {component}: {usage:,} tokens")
        
        if status['recent_alerts']:
            print("\nRecent Alerts:")
            for alert in status['recent_alerts']:
                print(f"  [{alert['level'].upper()}] {alert['message']}")
    
    if args.start_monitoring:
        try:
            monitor.start_monitoring()
            print("Monitoring active. Press Ctrl+C to stop.")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            monitor.stop_monitoring()
            print("\nMonitoring stopped.")

if __name__ == "__main__":
    main()