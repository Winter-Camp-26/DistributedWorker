import time

from worker.registry import get_handler


def execute_job(job: dict, worker_id: str) -> dict:
    """
    Execute a job using the appropriate registered handler.

    Returns either a COMPLETED or FAILED result.
    """

    start_time = time.perf_counter()

    job_id = job.get("jobId")
    job_type = job.get("type")
    payload = job.get("payload", {})

    try:
        if not job_id:
            raise ValueError("Missing 'jobId'")

        if not job_type:
            raise ValueError("Missing 'type'")

        handler = get_handler(job_type)

        result = handler(payload)

        duration_ms = int(
            (time.perf_counter() - start_time) * 1000
        )

        return {
            "jobId": job_id,
            "status": "COMPLETED",
            "result": result,
            "metadata": {
                "workerId": worker_id,
                "durationMs": duration_ms
            }
        }

    except Exception as error:

        duration_ms = int(
            (time.perf_counter() - start_time) * 1000
        )

        return {
            "jobId": job_id,
            "status": "FAILED",
            "error": {
                "type": type(error).__name__,
                "message": str(error)
            },
            "metadata": {
                "workerId": worker_id,
                "durationMs": duration_ms
            }
        }