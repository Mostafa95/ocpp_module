from ocpp.v16 import ChargePoint as cp
from ocpp.v16 import call_result,call
from ocpp.v16.enums import RegistrationStatus, AuthorizationStatus, RemoteStartStopStatus
from ocpp.routing import on
import datetime
from ocpp.v16.enums import RegistrationStatus
import logging
import uuid

event_logger = logging.getLogger("events")

def log_event(event_type, charger_id, data):
    log_message = f"{event_type} received from Charger {charger_id}: {data}"
    event_logger.info(log_message)

class OCPPHandler(cp):
    def __init__(self, consumer):
        self.consumer = consumer
        self.session = consumer.session
        super().__init__(consumer.charger_id, consumer)

    async def handle_message(self, message):
        message_id = message[1]
        action = message[2]  # Action is always the third element
        payload = message[3]  # Payload dictionary
        charger_id = self.consumer.charger_id
        log_event(action, charger_id, message)

        response = None
        if action == "BootNotification":
            response = await self.on_boot_notification(**payload)
        elif action == "Heartbeat":
            response = await self.on_heartbeat(**payload)
        elif action == "StartTransaction":
            response = await self.on_start_transaction(**payload)
        elif action == "StopTransaction":
            response = await self.on_stop_transaction(**payload)
        elif action == "Authorize":
            response = await self.on_authorize(**payload)
        elif action == "RemoteStartTransaction":
            response = await self.on_remote_start_transaction(**payload)
        elif action == "RemoteStopTransaction":
            response = await self.on_remote_stop_transaction(**payload)

        print(f"Generated Response: {response}")  
        if response:
            return [3, message_id, response]
        return None

    @on("BootNotification")
    async def on_boot_notification(self, **kwargs):
        print(f"BootNotification received from {self.id}")
         # Update charger status
        self.session.update_status("Available")

        return call_result.BootNotification(
            current_time=datetime.datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted.value
        ).__dict__


    @on("Heartbeat")
    async def on_heartbeat(self, **kwargs):
        print(f"Heartbeat received from {self.id}")
        event_logger.debug(f"Heartbeat from charger {self.id}")
        # Update heartbeat timestamp
        self.session.update_heartbeat()
        response = call_result.Heartbeat(
            current_time=datetime.datetime.utcnow().isoformat()
        ).__dict__

        print(f"Heartbeat response: {response}")
        return response


    @on("StartTransaction")
    async def on_start_transaction(self, connector_id=None, id_tag=None, meter_start=None, timestamp=None, **kwargs):
        print(f"StartTransaction received from {self.id} - Connector {connector_id}, ID Tag {id_tag}")

        transaction_id = int(uuid.uuid4().hex[:8], 16)
        self.session.start_transaction(transaction_id, connector_id)
        return call_result.StartTransaction(
            transaction_id=transaction_id,
            id_tag_info={"status": AuthorizationStatus.accepted.value}
        ).__dict__
    

    @on("StopTransaction")
    async def on_stop_transaction(self,transaction_id=None, meter_stop=None, timestamp=None, **kwargs):
        print(f"StopTransaction received for transaction {transaction_id}")
        self.session.stop_transaction()           
        return call_result.StopTransaction(
            id_tag_info={"status": AuthorizationStatus.accepted.value}
        ).__dict__
    

    @on("Authorize")
    async def on_authorize(self, idTag, **kwargs):
        print(f"Authorize request for ID tag: {idTag}")
        return call_result.Authorize(
            id_tag_info={"status": AuthorizationStatus.accepted.value}
        ).__dict__


    @on("RemoteStartTransaction")
    async def on_remote_start_transaction(self, id_tag, connector_id, **kwargs):
       print(f"RemoteStartTransaction requested for {self.id} on Connector {connector_id}")
        
        request = call.RemoteStartTransaction(
                id_tag='EV-123',
                connector_id=1
        )
        response = await self.call(request)
        print(f"RemoteStartTransaction response: {response})")
        if response.status == RemoteStartStopStatus.accepted:
            print("Transaction Started!!!")
        else:
            print("Transaction Failed to Start!!!")


    @on("RemoteStopTransaction")
    async def on_remote_stop_transaction(self,transaction_id=1, **kwargs):
        """Handles remote stop transaction requests."""
        print(f"RemoteStopTransaction requested for Transaction {transaction_id}")

        request = call.RemoteStopTransaction(
            transaction_id=transaction_id
        )
        response = await self.call(request)

        if response.status == RemoteStartStopStatus.accepted:
            print("Stopping transaction")
        else:
            print("Failed to stop transaction")

