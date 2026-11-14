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

// ---- ИНТЕГРАЦИОННЫЙ ТЕСТ ---- \\
func TestBatchIntegration(t *testing.T) {
	dsn := "host=localhost user=postgres password=admin dbname=bakery_db port=5432 sslmode=disable"
	db, _ = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	db.AutoMigrate(&Batch{})

	batchID := "bat-test-" + time.Now().Format("150405")
	testBatch := Batch{
		ID: batchID, OrderID: "ord-1", ProductType: "Baget",
		Quantity: 10, Status: "PLANNED", QualityStatus: "PENDING",
	}

	db.Create(&testBatch)
	var found Batch
	db.First(&found, "id = ?", batchID)

	if found.Quantity != 10 {
		t.Errorf("Expected quantity 10, got %d", found.Quantity)
	}
	db.Delete(&Batch{}, "id = ?", batchID)
}

// ---- E2E ТЕСТ ---- \\
func TestBatchE2E(t *testing.T) {
	gin.SetMode(gin.TestMode)
	initDB()
	r := gin.Default()
	r.POST("/api/batches", createBatch)

	jsonBody := []byte(`{"orderId":"ord-e2e", "productType":"Baget", "quantity":5}`)
	req, _ := http.NewRequest(http.MethodPost, "/api/batches", bytes.NewBuffer(jsonBody))
	req.Header.Set("Content-Type", "application/json")

	w := httptest.NewRecorder()
	r.ServeHTTP(w, req)

	if w.Code != http.StatusOK {
		t.Errorf("Expected status 200, got %d", w.Code)
	}

	var response Batch
	json.Unmarshal(w.Body.Bytes(), &response)
	if response.Status != "PLANNED" {
		t.Errorf("Expected status PLANNED, got %s", response.Status)
	}
}
