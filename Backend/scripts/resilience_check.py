import argparse
import asyncio
import statistics
import time

import httpx


async def run_probe(client: httpx.AsyncClient, url: str) -> tuple[bool, float, int]:
    start = time.perf_counter()
    try:
        response = await client.get(url)
        latency_ms = (time.perf_counter() - start) * 1000
        ok = 200 <= response.status_code < 300
        return ok, latency_ms, response.status_code
    except Exception:
        latency_ms = (time.perf_counter() - start) * 1000
        return False, latency_ms, 0


async def worker(
    client: httpx.AsyncClient,
    url: str,
    iterations: int,
    results: list[tuple[bool, float, int]],
) -> None:
    for _ in range(iterations):
        results.append(await run_probe(client, url))


async def main() -> int:
    parser = argparse.ArgumentParser(description="RushCart resilience smoke checker")
    parser.add_argument("--base-url", default="http://localhost:8000/api/v1", help="Backend base API URL")
    parser.add_argument("--iterations", type=int, default=60, help="Total request count")
    parser.add_argument("--concurrency", type=int, default=10, help="Concurrent workers")
    parser.add_argument("--timeout", type=float, default=5.0, help="Request timeout in seconds")
    parser.add_argument(
        "--max-failure-rate",
        type=float,
        default=0.05,
        help="Max allowed failure rate (0.05 = 5%%)",
    )
    parser.add_argument("--p95-threshold-ms", type=float, default=1200.0, help="Max acceptable p95 latency")
    args = parser.parse_args()

    target = f"{args.base_url.rstrip('/')}/system/health/live"
    timeout = httpx.Timeout(args.timeout)
    results: list[tuple[bool, float, int]] = []

    per_worker = max(1, args.iterations // max(1, args.concurrency))
    worker_count = max(1, args.concurrency)

    async with httpx.AsyncClient(timeout=timeout) as client:
        tasks = [worker(client, target, per_worker, results) for _ in range(worker_count)]
        await asyncio.gather(*tasks)

        # Readiness and metrics checks should respond successfully at least once.
        ready = await run_probe(client, f"{args.base_url.rstrip('/')}/system/health/ready")
        metrics = await run_probe(client, f"{args.base_url.rstrip('/')}/system/metrics")
        results.append(ready)
        results.append(metrics)

    if not results:
        print("No probe results were collected.")
        return 1

    success = [r for r in results if r[0]]
    failures = [r for r in results if not r[0]]
    latencies = [r[1] for r in results]
    p95 = statistics.quantiles(latencies, n=20)[18] if len(latencies) >= 20 else max(latencies)
    avg = statistics.mean(latencies)
    failure_rate = len(failures) / len(results)

    print(f"Target: {target}")
    print(f"Total probes: {len(results)}")
    print(f"Success: {len(success)}")
    print(f"Failures: {len(failures)}")
    print(f"Failure rate: {failure_rate:.2%}")
    print(f"Average latency: {avg:.2f} ms")
    print(f"P95 latency: {p95:.2f} ms")

    if failures:
        sample_codes = {}
        for _, _, status in failures:
            sample_codes[status] = sample_codes.get(status, 0) + 1
        print(f"Failure status distribution: {sample_codes}")

    if failure_rate > args.max_failure_rate:
        print("Resilience check failed: failure rate above threshold.")
        return 2
    if p95 > args.p95_threshold_ms:
        print("Resilience check failed: latency p95 above threshold.")
        return 3
    print("Resilience check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
