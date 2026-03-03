# Taxi Pricing Service (gRPC)

A microservice for calculating taxi ride costs with dynamic coefficients based on weather conditions and air raid alerts.

## Overview

The service calculates the price of a trip based on the route distance and adjusts it using external data:
- Weather Service: Checks weather conditions at the pickup location via Open-Meteo API. Adverse weather (rain, snow) increases the price.
- Alerts Service: Checks for active air raid alerts. If an alert is active, a higher tariff is applied.
- Maps Service: Handles geocoding and distance calculations.

## Technology Stack

- Python 3.12
- gRPC (Protobuf) - High-performance RPC framework.
- AsyncIO / HTTPX - Fully asynchronous architecture.
- Docker - Containerization.
- uv - Python package manager.

## Quick Start (Docker)

You can run the service without installing Python or dependencies using Docker.

Run the following command in your terminal:

docker run -d -p 50052:50052 -e GRPC_HOST=0.0.0.0 -e GRPC_PORT=50052 YOUR_DOCKER_LOGIN/taxi-pricing:v1

The service will start on port 50052.

## Project Structure

- app/domain: Business logic (price calculation rules).
- app/external: External API clients (Weather, Maps, Alerts).
- app/rpc: gRPC server implementation and generated code.
- protos/: Protocol Buffer definitions (.proto files).

## Testing

To manually test the service, you can run the included client script:

python -m scripts.manual_client