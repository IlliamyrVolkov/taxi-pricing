import asyncio
import grpc
from app.config import settings
from app.core.logger import logger
from app.rpc.generated import pricing_pb2_grpc
from app.rpc.server import PricingService


async def serve():
    server = grpc.aio.server()

    pricing_pb2_grpc.add_PricingServiceServicer_to_server(
        PricingService(),
        server
    )

    listen_addr = f"{settings.GRPC_HOST}:{settings.GRPC_PORT}"
    server.add_insecure_port(listen_addr)

    logger.info(f" Server started on {listen_addr}")
    print("Press Ctrl+C to stop...")

    await server.start()

    await server.wait_for_termination()


if __name__ == "__main__":
    try:
        asyncio.run(serve())
    except KeyboardInterrupt:
        logger.info("\n Server stopped by user")