import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .ocpp_handler import OCPPHandler
from ocpp.v16 import call, call_result
from .chargerSession import ChargerSession

active_chargers = {}

class OCPPConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.charger_id = self.scope["url_route"]["kwargs"]["charger_id"]
        if self.charger_id in active_chargers:
            print(f"Charger {self.charger_id} is reconnecting. Replacing old connection.")
            # Close old connection
            old_instance = active_chargers[self.charger_id]
            await old_instance.close()
            del active_chargers[self.charger_id]

        # Register the new connection
        active_chargers[self.charger_id] = self
        self.session = ChargerSession(self.charger_id)
        self.ocpp_handler = OCPPHandler(self)
        await self.accept()
        print(f"Charger {self.charger_id} connected (Session Active)")


    async def disconnect(self, close_code):
        if self.charger_id in active_chargers:
            del active_chargers[self.charger_id]
        print(f"Charger {self.charger_id} disconnected")

    async def receive(self, text_data):
        message = json.loads(text_data)
        response = await self.ocpp_handler.handle_message(message)
        if response is None:
            message_id = message[1]
            response = [4, message_id, "NotSupported", {}]
        try:
            await self.send(json.dumps(response))
            print(f"Successfully sent response to {self.charger_id}")
        except Exception as e:
            print(f"Failed to send response: {e}")
