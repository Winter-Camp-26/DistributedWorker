from worker.consumer import ImageWorkerConsumer


def start_worker(
    rabbitmq_host: str,
    worker_id: str
):
    """
    Create and start the image worker.
    """

    consumer = ImageWorkerConsumer(
        rabbitmq_host=rabbitmq_host,
        worker_id=worker_id
    )

    consumer.start()