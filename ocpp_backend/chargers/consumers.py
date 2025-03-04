import json
from channels.generic.websocket import AsyncWebsocketConsumer


active_chargers = {}

class OCPPConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.charger_id = self.scope["url_route"]["kwargs"]["charger_id"]
        await self.accept()
        active_chargers[self.charger_id] = self
        print(f"Charger {self.charger_id} connected")

    async def disconnect(self, close_code):
        if self.charger_id in active_chargers:
            del active_chargers[self.charger_id]  
        print(f"Charger {self.charger_id} disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)
        print(f"Received from {self.charger_id}: {data}")

        if data.get("action") == "BootNotification":
            response = {
                "messageTypeId": 3,
                "uniqueId": data["uniqueId"],
                "payload": {
                    "status": "Accepted",
                    "currentTime": "2025-03-03T12:00:00Z",
                    "interval": 10
                }
            }
            await self.send(json.dumps(response))
            print(f"Sent BootNotification Response to {self.charger_id}")
