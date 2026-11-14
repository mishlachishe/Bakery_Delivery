package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/gin-gonic/gin"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

// ----ИНТЕГРАЦИОННЫЙ ТЕСТ---- \\
func TestOrderIntegration(t *testing.T) {
	dsn := "host=localhost user=postgres password=admin dbname=bakery_db port=5432 sslmode=disable"
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		t.Fatalf("Failed to connect to database: %v", err)
	}
	db.AutoMigrate(&Order{})

	orderID := "ord-test-" + time.Now().Format("150405")
	testOrder := Order{
		ID: orderID, ClientID: "client-test", Items: "1 bread",
		DeliveryAddress: "Test Address", Total: 100, Status: "CREATED",
	}

	db.Create(&testOrder)

	var found Order
	db.First(&found, "id = ?", orderID)

	if found.Total != 100 {
		t.Errorf("Expected total 100, got %d", found.Total)
	}
	db.Delete(&Order{}, "id = ?", orderID)
}

// ----E2E ТЕСТ---- \\
func TestOrderE2E(t *testing.T) {
	gin.SetMode(gin.TestMode)
	initDB()
	r := gin.Default()
	r.POST("/api/orders", createOrder)

	jsonBody := []byte(`{"clientId":"client-e2e", "items":"2 bageta", "deliveryAddress":"ul. Pushkina, 10", "total":300}`)
	req, _ := http.NewRequest(http.MethodPost, "/api/orders", bytes.NewBuffer(jsonBody))
	req.Header.Set("Content-Type", "application/json")

	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("Expected status 200, got %d", w.Code)
	}

	var response Order
	json.Unmarshal(w.Body.Bytes(), &response)
	if response.Status != "CREATED" {
		t.Errorf("Expected status CREATED, got %s", response.Status)
	}
}
