import pika, os, json, uuid


RABBIT = os.getenv('RABBITMQ_URL', 'amqp://guest:guest@rabbitmq:5672/')


def enqueue_job(payload: dict) -> str:
conn = pika.BlockingConnection(pika.URLParameters(RABBIT))
ch = conn.channel()
ch.queue_declare(queue='jobs', durable=True)
job_id = str(uuid.uuid4())
payload['job_id'] = job_id
ch.basic_publish(
exchange='', routing_key='jobs', body=json.dumps(payload),
properties=pika.BasicProperties(delivery_mode=2)
)
conn.close()
return job_id
