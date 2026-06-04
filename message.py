"""
Incoming message schemas.

Models the WhatsApp Cloud API webhook payload shape that FastAPI
receives on POST /webhook/whatsapp.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class MessageType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    DOCUMENT = "document"
    AUDIO = "audio"
    VIDEO = "video"
    INTERACTIVE = "interactive"
    BUTTON = "button"
    LOCATION = "location"
    UNKNOWN = "unknown"


# ---------------------------------------------------------------------------
# Nested WhatsApp Cloud API structures
# ---------------------------------------------------------------------------


class TextContent(BaseModel):
    body: str = Field(..., description="Raw text sent by the user.")


class MediaContent(BaseModel):
    id: str = Field(..., description="WhatsApp media ID (use to download).")
    mime_type: str | None = None
    sha256: str | None = None
    caption: str | None = None


class WhatsAppMessage(BaseModel):
    """A single message object inside the webhook payload."""

    from_: str = Field(..., alias="from", description="Sender phone number.")
    id: str = Field(..., description="Unique WhatsApp message ID.")
    timestamp: str = Field(..., description="Unix timestamp string.")
    type: MessageType = Field(default=MessageType.UNKNOWN)

    # Optional content blocks — only the relevant one will be populated
    text: TextContent | None = None
    image: MediaContent | None = None
    document: MediaContent | None = None
    audio: MediaContent | None = None

    model_config = {"populate_by_name": True}

    @property
    def user_id(self) -> str:
        """Alias for from_ — matches session key convention."""
        return self.from_

    @property
    def body(self) -> str:
        """Convenience accessor for message text (empty string if not a text message)."""
        return self.text.body.strip() if self.text else ""

    @property
    def media_id(self) -> str | None:
        """Returns the media ID for image/document/audio messages."""
        for media in (self.image, self.document, self.audio):
            if media:
                return media.id
        return None


class WhatsAppMetadata(BaseModel):
    display_phone_number: str
    phone_number_id: str


class WhatsAppValue(BaseModel):
    messaging_product: str
    metadata: WhatsAppMetadata
    messages: list[WhatsAppMessage] = Field(default_factory=list)


class WhatsAppChange(BaseModel):
    value: WhatsAppValue
    field: str


class WhatsAppEntry(BaseModel):
    id: str
    changes: list[WhatsAppChange]


class WhatsAppPayload(BaseModel):
    """
    Root model for the WhatsApp Cloud API webhook payload.

    POST /webhook/whatsapp receives this body.
    """

    object: str = Field(..., description="Always 'whatsapp_business_account'.")
    entry: list[WhatsAppEntry]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "object": "whatsapp_business_account",
                    "entry": [
                        {
                            "id": "BUSINESS_ACCOUNT_ID",
                            "changes": [
                                {
                                    "value": {
                                        "messaging_product": "whatsapp",
                                        "metadata": {
                                            "display_phone_number": "919876543210",
                                            "phone_number_id": "PHONE_ID",
                                        },
                                        "messages": [
                                            {
                                                "from": "919876543210",
                                                "id": "wamid.xxx",
                                                "timestamp": "1700000000",
                                                "type": "text",
                                                "text": {"body": "1"},
                                            }
                                        ],
                                    },
                                    "field": "messages",
                                }
                            ],
                        }
                    ],
                }
            ]
        }
    }

    def extract_message(self) -> WhatsAppMessage | None:
        """
        Extract the first user message from the payload.

        Returns None if the payload contains no user messages
        (e.g. status update webhooks).
        """
        try:
            return self.entry[0].changes[0].value.messages[0]
        except (IndexError, AttributeError):
            return None


# ---------------------------------------------------------------------------
# Simplified internal representation passed to the Orchestrator
# ---------------------------------------------------------------------------


class IncomingMessage(BaseModel):
    """
    Normalised message passed from the API layer to the Orchestrator.

    Decouples the Orchestrator from the WhatsApp payload structure,
    making it easier to add other channels (e.g. web chat) later.
    """

    user_id: str = Field(..., description="Sender's phone number / unique user ID.")
    body: str = Field(default="", description="Stripped message text.")
    media_id: str | None = Field(default=None, description="Media ID for file uploads.")
    message_type: MessageType = Field(default=MessageType.TEXT)
    raw: dict[str, Any] | None = Field(
        default=None,
        description="Original WhatsApp message dict for audit logging.",
        exclude=True,
    )

    @classmethod
    def from_whatsapp(cls, msg: WhatsAppMessage) -> "IncomingMessage":
        return cls(
            user_id=msg.user_id,
            body=msg.body,
            media_id=msg.media_id,
            message_type=msg.type,
            raw=msg.model_dump(by_alias=True),
        )
