FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod ./
RUN go mod tidy
COPY . .
RUN go build -o main .

FROM alpine:latest
WORKDIR /app
COPY --from=builder /app/main .
# Для order-service EXPOSE 8081, для production-service EXPOSE 8082
EXPOSE 8082 
CMD ["./main"]