from app.core.observability import RequestMetrics, normalize_path


def test_normalize_path_masks_dynamic_segments():
    assert normalize_path("/orders/123") == "/orders/:id"
    assert normalize_path("/users/abcd1234-ffff-9999/profile") == "/users/:id/profile"


def test_request_metrics_snapshot_and_prometheus():
    metrics = RequestMetrics()

    metrics.begin_request()
    metrics.end_request(method="GET", path="/orders/1", status_code=200, duration_ms=120.0)
    metrics.begin_request()
    metrics.end_request(method="POST", path="/orders/2/cancel", status_code=500, duration_ms=350.0)

    snap = metrics.snapshot()
    assert snap["total_requests"] == 2
    assert snap["total_errors"] == 1
    assert snap["error_rate"] == 0.5
    assert snap["p95_duration_ms"] >= 120.0
    assert "GET /orders/:id" in {row["route"] for row in snap["top_routes"]}

    prometheus = metrics.prometheus_text()
    assert "rushcart_http_request_duration_ms_p95" in prometheus
    assert "rushcart_http_error_rate" in prometheus
