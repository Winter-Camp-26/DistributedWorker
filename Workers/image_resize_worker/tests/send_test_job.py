import json

import pika


connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host="localhost"
    )
)

channel = connection.channel()

channel.queue_declare(
    queue="jobs.image",
    durable=True
)


job = {
    "jobId": "job-001",
    "type": "IMAGE_RESIZE",
    "payload": {
        "image": "data/input/photo.jpg",
        "width": 600,
        "height": 600
    },
    "metadata": {
        "priority": "NORMAL",
        "attempt": 1
    }
}


channel.basic_publish(
    exchange="",
    routing_key="jobs.image",
    body=json.dumps(job)
)

print("Job sent:")
print(json.dumps(job, indent=2))

connection.close()