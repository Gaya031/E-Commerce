import argparse
import asyncio
import time

import httpx


async def main() -> int:
    parser = argparse.ArgumentParser(description="RushCart failover status checker")
    parser.add_argument("--base-url", default="http://localhost:8000/api/v1")
    parser.add_argument("--expect", choices=["ready", "degraded"], required=True)
    parser.add_argument("--timeout-seconds", type=float, default=40.0)
    parser.add_argument("--interval-seconds", type=float, default=2.0)
    args = parser.parse_args()

    endpoint = f"{args.base_url.rstrip('/')}/system/health/ready"
    deadline = time.time() + args.timeout_seconds

    async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as client:
        while time.time() < deadline:
            try:
                response = await client.get(endpoint)
                if response.status_code == 200:
                    body = response.json()
                    status = body.get("status")
                    print(f"Current status: {status}")
                    if status == args.expect:
                        print(f"Expected status '{args.expect}' reached.")
                        return 0
            except Exception:
                pass
            await asyncio.sleep(args.interval_seconds)

    print(f"Failover check failed: status '{args.expect}' not reached within timeout.")
    return 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
