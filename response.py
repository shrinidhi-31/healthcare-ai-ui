"""
Bot response schema.

Represents the structured reply returned by a flow to the Orchestrator,
which then sends it back to the user via WhatsApp.
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class ResponseType(str, Enum):
    """
    Controls how the WhatsApp sender formats the outgoing message.
    """

    TEXT = "text"
    """Plain text message."""

    MENU = "menu"
    """Numbered list menu (rendered as a WhatsApp List Message if >3 items)."""

    BUTTONS = "buttons"
    """Quick-reply buttons (max 3 options on WhatsApp)."""

    MEDIA = "media"
    """Message with an attached image, PDF, or audio clip."""


class QuickReply(BaseModel):
    id: str = Field(..., description="Machine-readable reply identifier.")
    title: str = Field(..., max_length=20, description="Button label (max 20 chars on WhatsApp).")


class BotResponse(BaseModel):
    """
    The structured reply produced by a flow step.

    The API layer translates this into a WhatsApp Cloud API request.
    """

    text: str = Field(..., description="Main message body to display to the user.")
    response_type: ResponseType = Field(
        default=ResponseType.TEXT,
        description="Controls message formatting on the client.",
    )
    quick_replies: list[QuickReply] | None = Field(
        default=None,
        description="Optional quick-reply buttons (used when response_type is BUTTONS or MENU).",
    )
    media_url: str | None = Field(
        default=None,
        description="Public URL of the media to attach (used when response_type is MEDIA).",
    )
    end_session: bool = Field(
        default=False,
        description="If True, the session is reset to the start flow after this reply.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "Welcome to MedVerify! Please choose an option:",
                    "response_type": "menu",
                    "quick_replies": [
                        {"id": "1", "title": "Symptom Assessment"},
                        {"id": "2", "title": "Upload Report"},
                        {"id": "3", "title": "Find Doctor"},
                    ],
                    "media_url": None,
                    "end_session": False,
                }
            ]
        }
    }

    @classmethod
    def text_only(cls, message: str, *, end_session: bool = False) -> "BotResponse":
        """Convenience constructor for simple text replies."""
        return cls(text=message, response_type=ResponseType.TEXT, end_session=end_session)

    @classmethod
    def main_menu(cls) -> "BotResponse":
        """Returns the standard main menu response."""
        return cls(
            text=(
                "Welcome to MedVerify 🏥\n\n"
                "How can I help you today?\n\n"
                "1️⃣  Symptom Assessment\n"
                "2️⃣  Upload Medical Report\n"
                "3️⃣  Find a Doctor nearby"
            ),
            response_type=ResponseType.MENU,
            quick_replies=[
                QuickReply(id="1", title="Symptom Assessment"),
                QuickReply(id="2", title="Upload Report"),
                QuickReply(id="3", title="Find Doctor"),
            ],
        )

    @classmethod
    def emergency_response(cls) -> "BotResponse":
        """Returns the standardised emergency guidance message."""
        return cls(
            text=(
                "🚨 *EMERGENCY DETECTED* 🚨\n\n"
                "Your symptoms may be life-threatening.\n\n"
                "Please:\n"
                "• *Call 112* (or your local emergency number) immediately\n"
                "• Do not be alone — get someone to stay with you\n"
                "• Stay calm and sit or lie down\n\n"
                "Our team has been alerted and will follow up shortly.\n\n"
                "Your health is our priority. Please seek help NOW. 🙏"
            ),
            response_type=ResponseType.TEXT,
            end_session=True,
        )
