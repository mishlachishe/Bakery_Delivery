import time
import pika

QUEUE_NAME = "ikbo-65-23_bogacheva"
EXCHANGE_NAME = "ikbo-65-23_bogacheva_exchange"
ROUTING_KEY = "payment.processed"

def callback(ch, method, properties, body):
    raw_body = body.decode()
    try:
        delay_seconds = int(raw_body)
    except ValueError:
        print(f"Ошибка парсинга числа из сообщения {raw_body!r}. Сообщение отклонено")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        return

    print(f"Получено сообщение: задержка {delay_seconds} сек. Симуляция нагрузки...")
    time.sleep(delay_seconds)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Обработка завершена, сообщение подтверждено")

def main():
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

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)

    print(f"Консьюмер варианта 4 запущен. Ожидание сообщений в '{QUEUE_NAME}'")
    channel.start_consuming()

main()