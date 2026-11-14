package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type Order struct {
	ID              string    `json:"orderId" gorm:"primaryKey"`
	ClientID        string    `json:"clientId"`
	Items           string    `json:"items"`
	DeliveryAddress string    `json:"deliveryAddress"`
	Total           int       `json:"total"`
	Status          string    `json:"status"`
	CreatedAt       time.Time `json:"createdAt"`
}

type Client struct {
	ID     string `json:"clientId" gorm:"primaryKey"`
	Name   string `json:"name"`
	Phone  string `json:"phone"`
	Status string `json:"status"`
}

var db *gorm.DB

func initDB() {
	dsn := "host=localhost user=postgres password=admin dbname=bakery_db port=5432 sslmode=disable"
	var err error
	db, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		panic("Failed to connect to database")
	}
	db.AutoMigrate(&Order{}, &Client{})
}

// Кросс-сервисный вызов ProductionService
func callProductionService(orderId string) {
	url := "http://localhost:8082/api/batches"
	payload := map[string]interface{}{
		"orderId":     orderId,
		"productType": "Багет",
		"quantity":    2,
	}
	jsonPayload, _ := json.Marshal(payload)
	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonPayload))
	if err == nil {
		defer resp.Body.Close()
		println("Успешно вызван ProductionService для заказа", orderId)
	} else {
		println("Ошибка вызова ProductionService:", err.Error())
	}
}

func createOrder(c *gin.Context) {
	var order Order
	if err := c.ShouldBindJSON(&order); err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}
	order.ID = "ord-" + time.Now().Format("150405")
	order.Status = "CREATED"
	db.Create(&order)
	go callProductionService(order.ID)
	c.JSON(200, order)
}

func getOrder(c *gin.Context) {
	id := c.Param("id")
	var order Order
	if err := db.First(&order, "id = ?", id).Error; err != nil {
		c.JSON(404, gin.H{"error": "Order not found"})
		return
	}
	c.JSON(200, order)
}

func cancelOrder(c *gin.Context) {
	id := c.Param("id")
	var order Order
	if err := db.First(&order, "id = ?", id).Error; err != nil {
		c.JSON(404, gin.H{"error": "Order not found"})
		return
	}
	order.Status = "CANCELLED"
	db.Save(&order)
	c.JSON(200, order)
}

func createClient(c *gin.Context) {
	var client Client
	if err := c.ShouldBindJSON(&client); err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}
	client.ID = "cli-" + time.Now().Format("150405")
	client.Status = "ACTIVE"
	db.Create(&client)
	c.JSON(200, client)
}

func main() {
	initDB()
	r := gin.Default()
	r.POST("/api/orders", createOrder)
	r.GET("/api/orders/:id", getOrder)
	r.POST("/api/orders/:id/cancel", cancelOrder)
	r.POST("/api/clients", createClient) // 4-й эндпоинт
	r.Run(":8081")
}
