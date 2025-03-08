import datetime
import logging
import json

transaction_logger = logging.getLogger("transactions")

class ChargerSession:
    def __init__(self, charger_id):
        self.charger_id = charger_id
        self.status = "Available"  # Default status
        self.last_heartbeat = None
        self.current_transaction_id = None
        self.connector_id = None
        self.connector_status = {}  # connector_id -> status

    def log_transaction(self,transaction_data):
        transaction_logger.info(json.dumps(transaction_data, ensure_ascii=False))

    def update_status(self, new_status):
        self.status = new_status
        print(f"Charger {self.charger_id} status updated to {new_status}")

    def update_heartbeat(self):
        self.last_heartbeat = datetime.datetime.utcnow()
        print(f"Heartbeat updated for {self.charger_id} at {self.last_heartbeat}")

    def start_transaction(self, transaction_id, connector_id):
        self.current_transaction_id = transaction_id
        self.connector_id = connector_id
        self.status = 'Charging'
        self.connector_status[connector_id] = "Charging"

        transaction_data = {
            "event": "StartTransaction",
            "charger_id": self.charger_id,
            "connector_id": self.connector_id,
            "transaction_id": self.current_transaction_id,
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }
        self.log_transaction(transaction_data)
        print(f"Charging started on {self.charger_id}, Connector {connector_id}, Transaction {transaction_id}")

    def stop_transaction(self):
        if self.connector_id in self.connector_status:
            self.connector_status[self.connector_id] = "Available"
        self.current_transaction_id = None
        self.status = 'Available'

        transaction_data = {
            "event": "StopTransaction",
            "charger_id": self.charger_id,
            "connector_id": self.connector_id,
            "transaction_id": self.current_transaction_id,
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }
        self.log_transaction(transaction_data)
        print(f"Charging stopped on {self.charger_id}, Connector {self.connector_id}")
