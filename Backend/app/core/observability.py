from __future__ import annotations

import re
import statistics
import time
from collections import Counter
from collections import deque
from threading import Lock


_numeric_segment_pattern = re.compile(r"/\d+(?=/|$)")
_hex_like_segment_pattern = re.compile(r"/[0-9a-fA-F-]{8,}(?=/|$)")


def normalize_path(path: str) -> str:
    if not path:
        return "/"
    path = _numeric_segment_pattern.sub("/:id", path)
    path = _hex_like_segment_pattern.sub("/:id", path)
    return path


class RequestMetrics:
    def __init__(self) -> None:
        self._lock = Lock()
        self._started_at = time.time()
        self._inflight = 0
        self._total_requests = 0
        self._total_errors = 0
        self._duration_ms_total = 0.0
        self._duration_ms_max = 0.0
        self._status_counts: Counter[str] = Counter()
        self._route_counts: Counter[str] = Counter()
        self._method_counts: Counter[str] = Counter()
        self._recent_durations_ms = deque(maxlen=5000)

    def begin_request(self) -> None:
        with self._lock:
            self._inflight += 1

    def end_request(self, *, method: str, path: str, status_code: int, duration_ms: float) -> None:
        normalized_path = normalize_path(path)
        status_label = str(status_code)
        method_label = (method or "UNKNOWN").upper()
        route_key = f"{method_label} {normalized_path}"

        with self._lock:
            self._inflight = max(0, self._inflight - 1)
            self._total_requests += 1
            if status_code >= 500:
                self._total_errors += 1
            self._duration_ms_total += duration_ms
            self._duration_ms_max = max(self._duration_ms_max, duration_ms)
            self._status_counts[status_label] += 1
            self._route_counts[route_key] += 1
            self._method_counts[method_label] += 1
            self._recent_durations_ms.append(duration_ms)

    def _percentile(self, values: list[float], percentile: float) -> float:
        if not values:
            return 0.0
        if len(values) == 1:
            return float(values[0])
        rank = max(0, min(len(values) - 1, int(round((percentile / 100.0) * (len(values) - 1)))))
        sorted_values = sorted(values)
        return float(sorted_values[rank])

    def snapshot(self) -> dict:
        with self._lock:
            total_requests = self._total_requests
            avg_duration = round(self._duration_ms_total / total_requests, 2) if total_requests else 0.0
            recent = list(self._recent_durations_ms)
            p95 = round(self._percentile(recent, 95), 2) if recent else 0.0
            p99 = round(self._percentile(recent, 99), 2) if recent else 0.0
            median = round(statistics.median(recent), 2) if recent else 0.0
            error_rate = round((self._total_errors / total_requests), 6) if total_requests else 0.0
            return {
                "uptime_seconds": int(time.time() - self._started_at),
                "inflight_requests": self._inflight,
                "total_requests": total_requests,
                "total_errors": self._total_errors,
                "error_rate": error_rate,
                "average_duration_ms": avg_duration,
                "median_duration_ms": median,
                "p95_duration_ms": p95,
                "p99_duration_ms": p99,
                "max_duration_ms": round(self._duration_ms_max, 2),
                "status_counts": dict(self._status_counts),
                "method_counts": dict(self._method_counts),
                "top_routes": [
                    {"route": route, "count": count}
                    for route, count in self._route_counts.most_common(20)
                ],
            }

    def prometheus_text(self) -> str:
        snap = self.snapshot()
        lines = [
            "# HELP rushcart_uptime_seconds Application uptime in seconds.",
            "# TYPE rushcart_uptime_seconds gauge",
            f"rushcart_uptime_seconds {snap['uptime_seconds']}",
            "# HELP rushcart_http_inflight_requests Number of in-flight requests.",
            "# TYPE rushcart_http_inflight_requests gauge",
            f"rushcart_http_inflight_requests {snap['inflight_requests']}",
            "# HELP rushcart_http_requests_total Total number of HTTP requests.",
            "# TYPE rushcart_http_requests_total counter",
            f"rushcart_http_requests_total {snap['total_requests']}",
            "# HELP rushcart_http_errors_total Total number of HTTP 5xx responses.",
            "# TYPE rushcart_http_errors_total counter",
            f"rushcart_http_errors_total {snap['total_errors']}",
            "# HELP rushcart_http_error_rate Error rate for HTTP requests.",
            "# TYPE rushcart_http_error_rate gauge",
            f"rushcart_http_error_rate {snap['error_rate']}",
            "# HELP rushcart_http_request_duration_ms_average Average HTTP request duration in milliseconds.",
            "# TYPE rushcart_http_request_duration_ms_average gauge",
            f"rushcart_http_request_duration_ms_average {snap['average_duration_ms']}",
            "# HELP rushcart_http_request_duration_ms_p95 p95 HTTP request duration in milliseconds.",
            "# TYPE rushcart_http_request_duration_ms_p95 gauge",
            f"rushcart_http_request_duration_ms_p95 {snap['p95_duration_ms']}",
            "# HELP rushcart_http_request_duration_ms_p99 p99 HTTP request duration in milliseconds.",
            "# TYPE rushcart_http_request_duration_ms_p99 gauge",
            f"rushcart_http_request_duration_ms_p99 {snap['p99_duration_ms']}",
            "# HELP rushcart_http_request_duration_ms_max Maximum HTTP request duration in milliseconds.",
            "# TYPE rushcart_http_request_duration_ms_max gauge",
            f"rushcart_http_request_duration_ms_max {snap['max_duration_ms']}",
        ]

        for status_code, count in sorted(snap["status_counts"].items()):
            lines.append(f'rushcart_http_requests_by_status_total{{status="{status_code}"}} {count}')
        for method, count in sorted(snap["method_counts"].items()):
            lines.append(f'rushcart_http_requests_by_method_total{{method="{method}"}} {count}')
        for route in snap["top_routes"]:
            route_label = route["route"].replace("\\", "\\\\").replace('"', '\\"')
            lines.append(f'rushcart_http_requests_by_route_total{{route="{route_label}"}} {route["count"]}')

        return "\n".join(lines) + "\n"


request_metrics = RequestMetrics()
