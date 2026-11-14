package main

import (
	"time"

	"github.com/gin-gonic/gin"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

type Batch struct {
	ID            string    `json:"batchId" gorm:"primaryKey"`
	OrderID       string    `json:"orderId"`
	ProductType   string    `json:"productType"`
	Quantity      int       `json:"quantity"`
	Status        string    `json:"status"`
	QualityStatus string    `json:"qualityStatus"`
	CreatedAt     time.Time `json:"createdAt"`
}

var db *gorm.DB

func initDB() {
	dsn := "host=localhost user=postgres password=admin dbname=bakery_db port=5432 sslmode=disable"
	db, _ = gorm.Open(postgres.Open(dsn), &gorm.Config{})
	db.AutoMigrate(&Batch{})
}

func createBatch(c *gin.Context) {
	var batch Batch
	c.ShouldBindJSON(&batch)
	batch.ID = "bat-" + time.Now().Format("150405")
	batch.Status = "PLANNED"
	batch.QualityStatus = "PENDING"
	db.Create(&batch)
	c.JSON(200, batch)
}

func bakeBatch(c *gin.Context) {
	id := c.Param("id")
	var batch Batch
	if err := db.First(&batch, "id = ?", id).Error; err != nil {
		c.JSON(404, gin.H{"error": "Batch not found"})
		return
	}
	batch.Status = "BAKED"
	db.Save(&batch)
	c.JSON(200, batch)
}

func checkBatch(c *gin.Context) {
	id := c.Param("id")
	var batch Batch
	if err := db.First(&batch, "id = ?", id).Error; err != nil {
		c.JSON(404, gin.H{"error": "Batch not found"})
		return
	}
	batch.QualityStatus = "PASSED"
	db.Save(&batch)
	c.JSON(200, batch)
}

func writeOffBatch(c *gin.Context) {
	id := c.Param("id")
	var batch Batch
	if err := db.First(&batch, "id = ?", id).Error; err != nil {
		c.JSON(404, gin.H{"error": "Batch not found"})
		return
	}
	batch.Status = "WRITTEN_OFF"
	db.Save(&batch)
	c.JSON(200, batch)
}

func main() {
	initDB()
	r := gin.Default()
	r.POST("/api/batches", createBatch)
	r.POST("/api/batches/:id/bake", bakeBatch)
	r.POST("/api/batches/:id/check", checkBatch)
	r.POST("/api/batches/:id/write-off", writeOffBatch)
	r.Run(":8082")
}
