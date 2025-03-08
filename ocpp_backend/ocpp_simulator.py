import asyncio
import websockets
import logging
import uuid
from ocpp.v16 import call
from ocpp.v16 import ChargePoint as cp
from ocpp.routing import on

logging.basicConfig(level=logging.DEBUG)

class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotification(
            charge_point_model="EV Charger",
            charge_point_vendor="MyCompany"
        )
        response = await self.call(request,skip_schema_validation=True)
        print(f"BootNotification Response: {response}")


    async def send_authorize(self):
        request = call.Authorize(id_tag="test_tag")
        response = await self.call(request,skip_schema_validation=True)
        print(f"Authorize Response:",response)


    async def send_heartbeat(self):
        request = call.Heartbeat()
        response = await self.call(request,skip_schema_validation=True)
        print(f"Heartbeat Response: {response}")


    async def send_start_transaction(self):
        request = call.StartTransaction(
            connector_id=1,
            id_tag="test_tag",
            meter_start=100,
            timestamp="2025-03-06T22:58:22Z"
        )
        response = await self.call(request,skip_schema_validation=True)
        print(f"StartTransaction Response: {response}")


    async def send_stop_transaction(self, transaction_id):
        request = call.StopTransaction(
            transaction_id=transaction_id,
            meter_stop=150,
            timestamp="2025-03-06T23:10:45Z"
        )
        response = await self.call(request,skip_schema_validation=True)
        print(f"StopTransaction Response: {response}")


    async def charge_funcs(self):
        await self.send_authorize()
        await asyncio.sleep(2)
        await self.send_boot_notification()
        await asyncio.sleep(2)
        await self.send_heartbeat()
        await asyncio.sleep(2)
        await self.send_start_transaction()
        await asyncio.sleep(5)
        await self.send_stop_transaction(transaction_id=12345)


async def main():
    charger_id = 'EV-1234'
    uri = "ws://127.0.0.1:8000/ws/ocpp/"+charger_id+"/"  # Modify with your backend WebSocket URL
    async with websockets.connect(uri, subprotocols=["ocpp1.6"]) as ws:
        charge_point = ChargePoint(charger_id, ws)
        await asyncio.gather(charge_point.start(), charge_point.charge_funcs())

if __name__ == "__main__":
    asyncio.run(main())
