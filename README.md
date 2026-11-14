# Доставка хлебобулочных изделий из пекарни

## run:
* ```cd production-service and order-service ; go run main.go```
* ```cd delivery-service; uvicorn main:app --port 8083 --reload```
* ```cd payment-service; uvicorn main:app --port 8084 --reload```
* ```cd notification-service; uvicorn main:app --port 8085 --reload```
* ```cd complaint-service; uvicorn main:app --port 8086 --reload```

## build go files:
```go build main.go```
## run tests:
```go run main_test.go```

```pytest tests/ -v```