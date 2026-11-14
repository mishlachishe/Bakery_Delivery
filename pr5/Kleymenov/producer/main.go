package main

import (
	"context"
	"log"
	"time"

	amqp "github.com/rabbitmq/amqp091-go"
)

func main() {
	conn, err := amqp.Dial("amqp://guest:guest@localhost:5672/")
	if err != nil {
		log.Fatalf("Error connection -> %v", err)
	}
	defer conn.Close()
	ch, err := conn.Channel()
	if err != nil {
		log.Fatalf("Eror openning channel -> %v", err)
	}
	defer ch.Close()
	qName := "ikbo-65-23_kleymenov"
	_, err = ch.QueueDeclare(
		qName,
		true,
		false,
		false,
		false,
		nil,
	)
	exchName := "ikbo-65-23_kleymenov_exchange"
	err = ch.ExchangeDeclare(
		exchName,
		"direct",
		true,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.Fatalf("Error declaring exchange -> %v", err)
	}
	routKey := "order.created"
	err = ch.QueueBind(
		qName,
		routKey,
		exchName,
		false,
		nil,
	)
	if err != nil {
		log.Fatalf("Error binding queue: %v", err)
	}
	body := []byte("Вариант 2 -> ОченьОченьОченьДлинноеСообщение777")
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()
	err = ch.PublishWithContext(
		ctx,
		exchName,
		routKey,
		false,
		false,
		amqp.Publishing{
			ContentType: "text/plain",
			Body:        body,
		},
	)
	if err != nil {
		log.Fatalf("Error publishing -> %v", err)
	}
	log.Printf("Message with %d byte published in %q", len(body), qName)
}
