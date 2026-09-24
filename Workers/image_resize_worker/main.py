import os

from dotenv import load_dotenv

from worker.runtime import start_worker


def main():
    load_dotenv()

    rabbitmq_host = os.getenv(
        "RABBITMQ_HOST",
        "localhost"
    )

    worker_id = os.getenv(
        "WORKER_ID",
        "image-worker-01"
    )

    print("=" * 50)
    print("IMAGE RESIZE WORKER")
    print("=" * 50)
    print(f"Worker ID    : {worker_id}")
    print(f"RabbitMQ     : {rabbitmq_host}")
    print("=" * 50)

    start_worker(
        rabbitmq_host=rabbitmq_host,
        worker_id=worker_id
    )


if __name__ == "__main__":
    main()