import pika
import sys

QUEUE_NAME = "ikbo-65-23_bogacheva"
EXCHANGE_NAME = "ikbo-65-23_bogacheva_exchange"
ROUTING_KEY = "payment.processed"

def main():
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost", port=5672,
                                      credentials=pika.PlainCredentials("guest", "guest"))
        )
        channel = connection.channel()

        channel.queue_declare(
            queue=QUEUE_NAME, 
            durable=True, 
            arguments={'x-queue-type': 'quorum'}
        )
        channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="direct", durable=True)
        channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE_NAME, routing_key=ROUTING_KEY)

        delay_seconds = 3
        body = str(delay_seconds)

        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=ROUTING_KEY,
            body=body,
            properties=pika.BasicProperties(
                content_type="text/plain",
                delivery_mode=2,
            ),
        )
        print(f"Отправлено сообщение с числом {delay_seconds} в очередь '{QUEUE_NAME}'")
        connection.close()

    except Exception as e:
        print(f"ОШИБКА ПРОДЮСЕРА: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()