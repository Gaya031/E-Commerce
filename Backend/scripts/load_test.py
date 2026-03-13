import argparse
import asyncio
import random
import statistics
import time

import httpx


ENDPOINT_WEIGHTS = [
    ("GET", "/system/health/live", 3),
    ("GET", "/system/metrics", 2),
    ("GET", "/search/?q=milk", 2),
    ("GET", "/search/products?q=bread", 2),
    ("GET", "/categories/", 1),
]


def pick_endpoint() -> tuple[str, str]:
    choices = []
    for method, path, weight in ENDPOINT_WEIGHTS:
        choices.extend([(method, path)] * weight)
    return random.choice(choices)


async def run_once(client: httpx.AsyncClient, base_url: str) -> tuple[bool, float, int]:
    method, path = pick_endpoint()
    start = time.perf_counter()
    try:
        response = await client.request(method, f"{base_url.rstrip('/')}{path}")
        latency_ms = (time.perf_counter() - start) * 1000
        ok = 200 <= response.status_code < 500
        return ok, latency_ms, response.status_code
    except Exception:
        latency_ms = (time.perf_counter() - start) * 1000
        return False, latency_ms, 0


async def worker(
    client: httpx.AsyncClient,
    base_url: str,
    iterations: int,
    output: list[tuple[bool, float, int]],
) -> None:
    for _ in range(iterations):
        output.append(await run_once(client, base_url))


async def main() -> int:
    parser = argparse.ArgumentParser(description="RushCart load test")
    parser.add_argument("--base-url", default="http://localhost:8000/api/v1")
    parser.add_argument("--iterations", type=int, default=400)
    parser.add_argument("--concurrency", type=int, default=20)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--max-failure-rate", type=float, default=0.03)
    parser.add_argument("--p95-threshold-ms", type=float, default=1200.0)
    args = parser.parse_args()

    per_worker = max(1, args.iterations // max(1, args.concurrency))
    results: list[tuple[bool, float, int]] = []

    async with httpx.AsyncClient(timeout=httpx.Timeout(args.timeout)) as client:
        await asyncio.gather(
            *[
                worker(client, args.base_url, per_worker, results)
                for _ in range(max(1, args.concurrency))
            ]
        )

    if not results:
        print("No load test results collected.")
        return 1

    latencies = [row[1] for row in results]
    failures = [row for row in results if not row[0]]
    p95 = statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else max(latencies)
    avg = statistics.mean(latencies)
    failure_rate = len(failures) / len(results)

    print(f"Total requests: {len(results)}")
    print(f"Failures: {len(failures)}")
    print(f"Failure rate: {failure_rate:.2%}")
    print(f"Avg latency: {avg:.2f} ms")
    print(f"P95 latency: {p95:.2f} ms")

    if failure_rate > args.max_failure_rate:
        print("Load test failed: failure rate above threshold.")
        return 2
    if p95 > args.p95_threshold_ms:
        print("Load test failed: p95 latency above threshold.")
        return 3
    print("Load test passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
