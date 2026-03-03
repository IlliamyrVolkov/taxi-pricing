import asyncio
import grpc
from app.rpc.generated import pricing_pb2, pricing_pb2_grpc


async def test_run():
    async with grpc.aio.insecure_channel('localhost:50052') as channel:
        client = pricing_pb2_grpc.PricingServiceStub(channel)

        request = pricing_pb2.PriceRequest(
            pickup_address="Kyiv",
            destination_address="Chernihiv",
            user_id="Andrew"
        )

        response = await client.GetPrice(request)

        print(f"   Price: {response.price}")
        print(f"   Currency: {response.currency}")


if __name__ == "__main__":
    asyncio.run(test_run())
