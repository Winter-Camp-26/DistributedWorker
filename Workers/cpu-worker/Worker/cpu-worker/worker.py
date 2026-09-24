import json
import sys
import time
from math import isqrt
from typing import Any


WORKER_ID = "cpu-worker-01"


class InvalidJobPayload(Exception):
    pass


def validate_job(job: dict[str, Any]) -> None:
    if "jobId" not in job:
        raise InvalidJobPayload("jobId is required")

    if job.get("type") != "CPU_INTENSIVE":
        raise InvalidJobPayload("unsupported job type")

    payload = job.get("payload")

    if not isinstance(payload, dict):
        raise InvalidJobPayload("payload is required")

    if payload.get("operation") != "PRIME_COUNT":
        raise InvalidJobPayload("unsupported operation")

    limit = payload.get("limit")

    if not isinstance(limit, int):
        raise InvalidJobPayload("limit must be an integer")

    if limit <= 1:
        raise InvalidJobPayload("limit must be greater than 1")


def is_prime(number: int) -> bool:
    if number < 2:
        return False

    if number == 2:
        return True

    if number % 2 == 0:
        return False

    for divisor in range(3, isqrt(number) + 1, 2):
        if number % divisor == 0:
            return False

    return True


def count_primes(limit: int) -> int:
    count = 0

    for number in range(2, limit + 1):
        if is_prime(number):
            count += 1

    return count


def execute_job(job: dict[str, Any]) -> dict[str, Any]:
    start_time = time.perf_counter()

    try:
        validate_job(job)

        payload = job["payload"]
        limit = payload["limit"]

        prime_count = count_primes(limit)

        duration_ms = int(
            (time.perf_counter() - start_time) * 1000
        )

        return {
            "jobId": job["jobId"],
            "status": "COMPLETED",
            "result": {
                "operation": "PRIME_COUNT",
                "limit": limit,
                "primeCount": prime_count,
            },
            "metadata": {
                "workerId": WORKER_ID,
                "durationMs": duration_ms,
            },
        }

    except InvalidJobPayload as error:
        duration_ms = int(
            (time.perf_counter() - start_time) * 1000
        )

        return {
            "jobId": job.get("jobId"),
            "status": "FAILED",
            "error": {
                "type": "InvalidJobPayload",
                "message": str(error),
            },
            "metadata": {
                "workerId": WORKER_ID,
                "durationMs": duration_ms,
            },
        }


def main() -> None:
    raw_input = sys.stdin.read()
    job = json.loads(raw_input)

    result = execute_job(job)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
