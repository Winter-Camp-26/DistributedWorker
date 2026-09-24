from math import isqrt


def run_cpu_job(payload: dict) -> dict:
    """
    Run a CPU-intensive operation according to the job payload.

    Expected payload:
    {
        "operation": "PRIME_COUNT",
        "limit": 1000000
    }

    Returns:
    {
        "operation": "PRIME_COUNT",
        "limit": 1000000,
        "primeCount": 78498
    }
    """

    operation = payload.get("operation")
    limit = payload.get("limit")

    # -------------------------
    # Validate payload
    # -------------------------

    if operation != "PRIME_COUNT":
        raise ValueError(
            f"Unsupported operation: {operation}"
        )

    if limit is None:
        raise ValueError("Missing 'limit' field")

    # bool is a subclass of int, so reject it explicitly.
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise ValueError("'limit' must be an integer")

    if limit <= 1:
        raise ValueError("'limit' must be greater than 1")

    # -------------------------
    # Return result
    # -------------------------

    return {
        "operation": operation,
        "limit": limit,
        "primeCount": count_primes(limit)
    }


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


# Trial division is used on purpose instead of a sieve:
# the goal of this job is to generate CPU load.
def count_primes(limit: int) -> int:
    count = 0

    for number in range(2, limit + 1):
        if is_prime(number):
            count += 1

    return count
