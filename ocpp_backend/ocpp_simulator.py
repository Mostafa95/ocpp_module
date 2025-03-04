import asyncio
import websockets
from ocpp.v16 import call
from ocpp.v16 import ChargePoint as cp
import json

async def test_ocpp():
    uri = "ws://localhost:8000/ws/ocpp/EV-123/"  # Replace with your WebSocket URL

    async with websockets.connect(uri) as websocket:
        print("Connected to OCPP backend!")

        boot_notification = {
            "messageTypeId": 2,  # 2 = CALL (OCPP request)
            "uniqueId": "12345",
            "action": "BootNotification",
            "payload": {
                "chargePointVendor": "EV-Charger Inc.",
                "chargePointModel": "EVSE-123"
            }
        }
        await websocket.send(json.dumps(boot_notification))
        print("BootNotification sent!")

        response = await websocket.recv()
        print(f"Received response: {response}")

asyncio.run(test_ocpp())