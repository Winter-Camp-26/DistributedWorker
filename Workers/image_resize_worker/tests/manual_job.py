from worker.executor import execute_job


job = {
    "jobId": "job-001",
    "type": "IMAGE_RESIZE",
    "payload": {
        "image": "data/input/photo.jpg",
        "width": 800,
        "height": 600
    },
    "metadata": {
        "priority": "NORMAL",
        "attempt": 1
    }
}


result = execute_job(
    job=job,
    worker_id="image-worker-test"
)

print(result)