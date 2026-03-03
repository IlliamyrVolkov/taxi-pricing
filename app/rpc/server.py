import grpc

from app.core.logger import logger
from app.rpc.generated import pricing_pb2, pricing_pb2_grpc
from app.domain.calculator import calculate_ride_price
from app.external.maps_service import maps_client
from app.external.weather_service import weather_client
from app.external.alarm_service import alarms_client


class PricingService(pricing_pb2_grpc.PricingServiceServicer):

    async def GetPrice(self, request, context):
        try:
            logger.info(f"--- Request from user_id: {request.user_id} ---")

            dist = await maps_client.get_distance(
                request.pickup_address,
                request.destination_address
            )

            coords = await maps_client.get_coords(request.pickup_address)
            if coords:
                lat, lon = coords
            else:
                error_msg = f"Not found address: {request.pickup_address}"
                logger.error(error_msg)

                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(error_msg)

                return pricing_pb2.PriceResponse()

            bad_weather = await weather_client.get_weather_coef(lat, lon)
            air_alarm = await alarms_client.get_alarm(request.pickup_address)

            final_price = calculate_ride_price(dist, bad_weather, air_alarm)

            response = pricing_pb2.PriceResponse(
                price=final_price,
                currency="UAH"
            )

            logger.info(f"Distance: {dist}km | Rain: {bad_weather} | Alarm: {air_alarm}")
            logger.info(f"--- Response: {final_price} UAH ---\n")
            return response

        except Exception as e:
            logger.error(f"Calculation error: {e}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return pricing_pb2.PriceResponse()
