"""
Bengaluru Sahayaka - Voice-First AI Agent for Local Government Services
FastAPI backend for Vapi Squads
Returns raw data for Vapi's LLM to process
"""

import os
import json
import logging
import traceback
from fastapi import FastAPI, Request
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

app = FastAPI(title="Bengaluru Sahayaka - Government Services Assist")

# ------------------------------------------------------------------
# Service handler registry
# ------------------------------------------------------------------
SERVICE_HANDLERS = {}


def _load_handlers():
    """Lazy-load service handlers so import errors don't crash startup."""
    global SERVICE_HANDLERS
    if SERVICE_HANDLERS:
        return

    try:
        from app.services.certificates import (
            assess_eligibility as cert_eligibility,
            generate_document_checklist as cert_checklist,
            get_procedure_steps as cert_procedure,
            get_affidavit_template as cert_affidavit,
            get_office_info as cert_office,
            general_cert_query as cert_general,
        )

        SERVICE_HANDLERS["certificates"] = {
            "assess_eligibility": cert_eligibility,
            "generate_document_checklist": cert_checklist,
            "get_procedure_steps": cert_procedure,
            "get_affidavit_template": cert_affidavit,
            "get_office_info": cert_office,
            "general_cert_query": cert_general,
        }
        logger.info("[INIT] Certificate handler registered")
    except Exception as e:
        logger.error(f"[INIT] Certificate handler failed: {e}")

    try:
        from app.services.tax import (
            get_tax_estimate as tax_estimate,
            get_payment_options as tax_payment,
            general_tax_query as tax_general,
        )

        SERVICE_HANDLERS["tax"] = {
            "get_tax_estimate": tax_estimate,
            "get_payment_options": tax_payment,
            "general_tax_query": tax_general,
        }
        logger.info("[INIT] Tax handler registered")
    except Exception as e:
        logger.error(f"[INIT] Tax handler failed: {e}")

    try:
        from app.services.grievances import (
            file_complaint as grievance_file,
            get_complaint_status as grievance_status,
            general_grievance_query as grievance_general,
        )

        SERVICE_HANDLERS["grievances"] = {
            "file_complaint": grievance_file,
            "get_complaint_status": grievance_status,
            "general_grievance_query": grievance_general,
        }
        logger.info("[INIT] Grievance handler registered")
    except Exception as e:
        logger.error(f"[INIT] Grievance handler failed: {e}")


_load_handlers()


# ------------------------------------------------------------------
# Generic service webhook dispatcher
# ------------------------------------------------------------------
async def dispatch_service_webhook(service: str, request: Request):
    """Handle Vapi tool-calls for a specific government service."""
    try:
        body = await request.json()
        message_type = body.get("message", {}).get("type")

        if message_type in ["function-call", "tool-calls"]:
            # Extract function call details
            if message_type == "tool-calls":
                tool_calls = body.get("message", {}).get("toolCalls", [])
                if not tool_calls:
                    return {"results": []}
                tool_call = tool_calls[0]
                tool_call_id = tool_call.get("id")
                function_data = tool_call.get("function", {})
                function_name = function_data.get("name")
                arguments = function_data.get("arguments", "{}")
                if isinstance(arguments, str):
                    arguments = json.loads(arguments)
            else:
                function_call = body.get("message", {}).get("functionCall", {})
                function_name = function_call.get("name")
                arguments = function_call.get("parameters", {})
                tool_call_id = body.get("message", {}).get("toolCallId")

            logger.info(f"[{service.upper()}] {function_name}: {arguments}")

            handler_map = SERVICE_HANDLERS.get(service)
            if not handler_map:
                logger.error(f"[{service.upper()}] No handler registered")
                return {"results": []}

            func = handler_map.get(function_name)
            if not func:
                logger.error(f"[{service.upper()}] Unknown function: {function_name}")
                return {"results": []}

            # Call handler and extract response payload
            raw_result = func(**arguments)
            response_text = raw_result.get("response", json.dumps(raw_result, indent=2))

            logger.info(f"[{service.upper()} RETURNING] {response_text[:150]}...")

            return {
                "results": [{
                    "toolCallId": tool_call_id,
                    "result": response_text
                }]
            }

        return {"results": []}

    except Exception as e:
        logger.error(f"[{service.upper()} ERROR] {e}")
        traceback.print_exc()
        return {"results": []}


@app.post("/vapi/webhook/{service}")
async def service_webhook(service: str, request: Request):
    """Dynamic webhook for any registered government service."""
    return await dispatch_service_webhook(service, request)


@app.get("/")
async def root():
    return {
        "status": "running",
        "mode": "bengaluru-government-services",
        "services": list(SERVICE_HANDLERS.keys()),
    }
