package main

import (
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
	_, err = ch.QueueDeclare(qName, true, false, false, false, nil)
	if err != nil {
		log.Fatalf("Error declaring queue -> %v", err)
	}
	exchName := "ikbo-65-23_kleymenov_exchange"
	err = ch.ExchangeDeclare(exchName, "direct", true, false, false, false, nil)
	if err != nil {
		log.Fatalf("Error declaring exchange -> %v", err)
	}
	routKey := "order.created"
	err = ch.QueueBind(qName, routKey, exchName, false, nil)
	if err != nil {
		log.Fatalf("Error binding queue -> %v", err)
	}
	err = ch.Qos(1, 0, false)
	if err != nil {
		log.Fatalf("Error Qos -> %v", err)
	}
	msgs, err := ch.Consume(
		qName,
		"",
		false,
		false,
		false,
		false,
		nil,
	)
	if err != nil {
		log.Fatalf("Error registering consumer -> %v", err)
	}
	log.Println("Консьюмер вар2 ожидает...")
	for d := range msgs {
		delay := time.Duration(len(d.Body)) * time.Second
		log.Printf("Message with %d bytes, delay -> %v", len(d.Body), delay)
		time.Sleep(delay)
		if err := d.Ack(false); err != nil {
			log.Printf("Error confirming -> %v", err)
		}
		log.Println("Message confirmed...")
	}
}
