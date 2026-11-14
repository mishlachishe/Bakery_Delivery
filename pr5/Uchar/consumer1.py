import random
import time
import sys
import pika

QUEUE_NAME = "ikbo-65-23_uchar"
EXCHANGE_NAME = "ikbo-65-23_uchar_exchange"


def callback(ch, method, properties, body):
    delay_sec = random.randint(1, 5)
    print(f"[x] Получено сообщение: {body.decode()!r}. Случайная задержка {delay_sec} сек...")
    time.sleep(delay_sec)

    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("[x] Обработка завершена, сообщение подтверждено")


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672,
                                  credentials=pika.PlainCredentials("guest", "guest"))
    )
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True, auto_delete=True)
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="fanout", durable=True)
    channel.queue_bind(queue=QUEUE_NAME, exchange=EXCHANGE_NAME, routing_key="")

    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback, auto_ack=False)

    print("[*] Консьюмер варианта 3 запущен. Ожидание сообщений. Для выхода нажмите CTRL+C")
    channel.start_consuming()

main()