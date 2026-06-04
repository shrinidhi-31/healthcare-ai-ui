"""
MedVerify shared Pydantic schemas.

These schemas are OpenAPI-compatible and used across the API layer,
service layer, and flow definitions.
"""

from .session import SessionState
from .message import IncomingMessage, WhatsAppPayload
from .response import BotResponse
from .alert import Alert, AlertCreate, AlertUpdate, AlertListResponse
from .doctor import Doctor, DoctorSearchRequest

__all__ = [
    "SessionState",
    "IncomingMessage",
    "WhatsAppPayload",
    "BotResponse",
    "Alert",
    "AlertCreate",
    "AlertUpdate",
    "AlertListResponse",
    "Doctor",
    "DoctorSearchRequest",
]
