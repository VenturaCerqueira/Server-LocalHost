import time
import logging
from typing import Dict, Any, List
from datetime import datetime, timedelta
import json
import os
from flask import current_app

logger = logging.getLogger(__name__)

class MetricsService:
    def __init__(self):
        self.metrics_file = None  # Will be initialized lazily
        self.metrics: Dict[str, Any] = {
            'total_requests': 0,
            'total_response_time': 0,
            'endpoint_metrics': {},
            'slow_requests': [],
            'alerts': []
        }
        self.request_start_time = None

    def _initialize_metrics_file(self):
        """Initialize metrics file path lazily"""
        try:
            from flask import current_app
            self.metrics_file = os.path.join(current_app.root_path, 'metrics.json')
        except RuntimeError as e:
            # This error occurs if no app context is active
            logger.warning(f"App context not active yet: {e}")
            self.metrics_file = 'metrics.json'
        except Exception as e:
            logger.error(f"Error initializing metrics file path: {e}")
            # Fallback to a default path if current_app is not available
            self.metrics_file = 'metrics.json'

    def _load_metrics(self) -> Dict[str, Any]:
        """Load metrics from file"""
        # Initialize metrics_file lazily if not already set
        if self.metrics_file is None:
            self._initialize_metrics_file()

        if os.path.exists(self.metrics_file):
            try:
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading metrics: {e}")
        return {
            'total_requests': 0,
            'total_response_time': 0,
            'endpoint_metrics': {},
            'slow_requests': [],
            'alerts': []
        }

    def _save_metrics(self):
        """Save metrics to file"""
        if self.metrics_file is None:
            self._initialize_metrics_file()
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Error saving metrics: {e}")

    def start_request(self):
        """Record start time of request"""
        self.request_start_time = time.time()

    def end_request(self, endpoint: str, method: str, status_code: int):
        """Record end of request and calculate metrics"""
        if self.request_start_time is None:
            return

        response_time = time.time() - self.request_start_time
        self.request_start_time = None

        # Update total metrics
        self.metrics['total_requests'] += 1
        self.metrics['total_response_time'] += response_time

        # Update endpoint-specific metrics
        endpoint_key = f"{method} {endpoint}"
        if endpoint_key not in self.metrics['endpoint_metrics']:
            self.metrics['endpoint_metrics'][endpoint_key] = {
                'count': 0,
                'total_time': 0,
                'avg_time': 0,
                'min_time': float('inf'),
                'max_time': 0,
                'status_codes': {}
            }

        endpoint_metrics = self.metrics['endpoint_metrics'][endpoint_key]
        endpoint_metrics['count'] += 1
        endpoint_metrics['total_time'] += response_time
        endpoint_metrics['avg_time'] = endpoint_metrics['total_time'] / endpoint_metrics['count']
        endpoint_metrics['min_time'] = min(endpoint_metrics['min_time'], response_time)
        endpoint_metrics['max_time'] = max(endpoint_metrics['max_time'], response_time)

        # Track status codes
        status_key = str(status_code)
        if status_key not in endpoint_metrics['status_codes']:
            endpoint_metrics['status_codes'][status_key] = 0
        endpoint_metrics['status_codes'][status_key] += 1

        # Check for slow requests (response time > 5 seconds)
        if response_time > 5.0:
            slow_request = {
                'timestamp': datetime.now().isoformat(),
                'endpoint': endpoint_key,
                'response_time': response_time,
                'status_code': status_code
            }
            self.metrics['slow_requests'].append(slow_request)

            # Keep only last 100 slow requests
            if len(self.metrics['slow_requests']) > 100:
                self.metrics['slow_requests'] = self.metrics['slow_requests'][-100:]

            # Log alert
            logger.warning(f"SLOW REQUEST ALERT: {endpoint_key} took {response_time:.2f}s")

            # Add to alerts if not already present
            alert_msg = f"Endpoint {endpoint_key} is responding slowly (>5s)"
            if alert_msg not in [a['message'] for a in self.metrics['alerts']]:
                self.metrics['alerts'].append({
                    'timestamp': datetime.now().isoformat(),
                    'message': alert_msg,
                    'severity': 'warning'
                })

        # Clean old alerts (keep only last 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)
        self.metrics['alerts'] = [
            alert for alert in self.metrics['alerts']
            if datetime.fromisoformat(alert['timestamp']) > cutoff_time
        ]

        self._save_metrics()

    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of current metrics"""
        total_requests = self.metrics['total_requests']
        avg_response_time = self.metrics['total_response_time'] / total_requests if total_requests > 0 else 0

        # Get top 5 slowest endpoints
        endpoint_times = []
        for endpoint, data in self.metrics['endpoint_metrics'].items():
            if data['count'] > 0:
                endpoint_times.append({
                    'endpoint': endpoint,
                    'avg_time': data['avg_time'],
                    'count': data['count']
                })

        endpoint_times.sort(key=lambda x: x['avg_time'], reverse=True)
        top_slow_endpoints = endpoint_times[:5]

        return {
            'total_requests': total_requests,
            'avg_response_time': avg_response_time,
            'top_slow_endpoints': top_slow_endpoints,
            'slow_requests_count': len(self.metrics['slow_requests']),
            'active_alerts': len(self.metrics['alerts']),
            'last_updated': datetime.now().isoformat()
        }

    def get_detailed_metrics(self) -> Dict[str, Any]:
        """Get detailed metrics for all endpoints"""
        return self.metrics

    def clear_metrics(self):
        """Clear all metrics (for testing or reset)"""
        self.metrics = {
            'total_requests': 0,
            'total_response_time': 0,
            'endpoint_metrics': {},
            'slow_requests': [],
            'alerts': []
        }
        self._save_metrics()
        logger.info("Metrics cleared")

# Global instance
metrics_service = MetricsService()
