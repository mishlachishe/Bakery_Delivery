import pika




QUEUE_NAME = "ikbo-65-23_uchar"
EXCHANGE_NAME = "ikbo-65-23_uchar_exchange"


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672,
                                  credentials=pika.PlainCredentials("guest", "guest"))
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True, auto_delete=True)

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout", durable=True)

    channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE_NAME, routing_key="")

    body = "Hello from Variant 3 (fanout)!"
    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key="",
        body=body,
        properties=pika.BasicProperties(content_type="text/plain"),
    )
    print(f"[x] Отправлено сообщение в fanout-обменник '{EXCHANGE_NAME}'")

    connection.close()

main()