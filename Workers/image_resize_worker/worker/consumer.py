import json

import pika

from worker.executor import execute_job


class ImageWorkerConsumer:

    def __init__(
        self,
        rabbitmq_host: str,
        worker_id: str,
        input_queue: str = "jobs.image",
        result_queue: str = "jobs.results"
    ):
        self.worker_id = worker_id
        self.input_queue = input_queue
        self.result_queue = result_queue

        # -------------------------
        # RabbitMQ connection
        # -------------------------

        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=rabbitmq_host
            )
        )

        self.channel = self.connection.channel()

        # -------------------------
        # Declare queues
        # -------------------------

        self.channel.queue_declare(
            queue=self.input_queue,
            durable=True
        )

        self.channel.queue_declare(
            queue=self.result_queue,
            durable=True
        )

        # -------------------------
        # Worker receives one job
        # at a time
        # -------------------------

        self.channel.basic_qos(
            prefetch_count=1
        )

    def start(self):
        """
        Start consuming jobs from RabbitMQ.
        """

        self.channel.basic_consume(
            queue=self.input_queue,
            on_message_callback=self.handle_message,
            auto_ack=False
        )

        print(
            f"[{self.worker_id}] "
            f"Listening on queue '{self.input_queue}'"
        )

        self.channel.start_consuming()

    def handle_message(
        self,
        channel,
        method,
        properties,
        body
    ):
        """
        Process one RabbitMQ message.
        """

        job_id = None

        try:
            # -------------------------
            # Parse message
            # -------------------------

            job = json.loads(body)

            job_id = job.get("jobId")

            print(
                f"[{self.worker_id}] "
                f"Received job: {job_id}"
            )

            # -------------------------
            # Execute job
            # -------------------------

            result = execute_job(
                job=job,
                worker_id=self.worker_id
            )

            # -------------------------
            # Publish result
            # -------------------------

            channel.basic_publish(
                exchange="",
                routing_key=self.result_queue,
                body=json.dumps(result),
                properties=pika.BasicProperties(
                    content_type="application/json",
                    delivery_mode=2
                )
            )

            print(
                f"[{self.worker_id}] "
                f"Job {job_id} → {result['status']}"
            )

            # -------------------------
            # ACK
            # -------------------------

            channel.basic_ack(
                delivery_tag=method.delivery_tag
            )

        except json.JSONDecodeError as error:

            print(
                f"[{self.worker_id}] "
                f"Invalid JSON message: {error}"
            )

            # Invalid messages should not
            # be endlessly requeued.
            channel.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=False
            )

        except Exception as error:

            print(
                f"[{self.worker_id}] "
                f"Unexpected error for job "
                f"{job_id}: {error}"
            )

            channel.basic_nack(
                delivery_tag=method.delivery_tag,
                requeue=False
            )