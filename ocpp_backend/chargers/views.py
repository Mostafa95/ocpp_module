from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from .consumers import active_chargers
from ocpp.v16 import call
from asgiref.sync import sync_to_async,async_to_sync


def list_chargers(request):
    """Returns a list of active chargers."""
    return JsonResponse({"active_chargers": list(active_chargers.keys())})


@csrf_exempt
def get_charger_status(request, charger_id):
    """Returns the status of a specific charger."""
    if charger_id in active_chargers:
        charger = active_chargers[charger_id].session
        return JsonResponse({
            "charger_id": charger.charger_id,
            "status": charger.status,
            "last_heartbeat": charger.last_heartbeat.isoformat() if charger.last_heartbeat else None,
            "current_transaction_id": charger.current_transaction_id,
            "connector_status": charger.connector_status
        })
    return JsonResponse({"error": "Charger not found"}, status=404)


@csrf_exempt
def get_logs(request):
    """Fetch transaction logs with optional filters."""
    charger_id = request.GET.get("charger_id")
    connector_id = request.GET.get("connector_id")
    transaction_id = request.GET.get("transaction_id")

    log_entries = []
    try:
        with open("logs/transactions.log", "r") as log_file:
            for line in log_file:
                    try:
                        json_start = line.find('{')  # Find start of JSON data
                        log_entry = json.loads(line[json_start:].strip())
                        if ((not charger_id or log_entry.get("charger_id") == charger_id) and
                            (not connector_id or str(log_entry.get("connector_id")) == connector_id) and
                            (not transaction_id or str(log_entry.get("transaction_id")) == transaction_id)):
                            log_entries.append(log_entry)
                    except json.JSONDecodeError:
                        continue  # Skip lines that can't be decoded as JSON
    except FileNotFoundError:
        return JsonResponse({"error": "Log file not found"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Error reading log file"}, status=500)

    return JsonResponse({"logs": log_entries})


@sync_to_async
@csrf_exempt
@async_to_sync
async def remote_start_transaction(request):
    """Sends a remote start command to a charger."""

    try:
        data = json.loads(request.body)
        charger_id = data.get("charger_id")
        id_tag = data.get("id_tag", "default-tag")
        connector_id = data.get("connector_id", 1)

        charger = active_chargers.get(charger_id)
        if not charger:
            return JsonResponse({"error": "Charger not found"}, status=404)

        request_msg = call.RemoteStartTransaction(
            id_tag=id_tag,
            connector_id=connector_id
        )

        # Convert the message to JSON (properly formatted as a string)
        message_json = json.dumps(request_msg.to_json())

        # Send the message over WebSocket
        await charger.send(message_json)


        return JsonResponse({
            "status": "Command Sent"
        })

    except json.JSONDecodeError:
        return  JsonResponse({"error": "Invalid JSON"}, status=400)
    except Exception as e:
        return  JsonResponse({"error": str(e)}, status=500)

