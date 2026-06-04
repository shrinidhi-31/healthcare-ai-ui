"""
Session state schema — stored in Redis as JSON.

Key format: session:{user_id}
Default TTL: 3600 seconds (1 hour)
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class FlowName(str, Enum):
    """All valid conversation flow identifiers."""

    START = "start"
    SYMPTOMS = "symptoms"
    REPORT = "report"
    DOCTOR = "doctor"
    EMERGENCY = "emergency"


class Language(str, Enum):
    """Supported UI languages."""

    ENGLISH = "en"
    HINDI = "hi"
    TAMIL = "ta"
    TELUGU = "te"
    KANNADA = "kn"


class SessionState(BaseModel):
    """
    Represents a user's full conversation state.

    Persisted in Redis as JSON. All fields must be JSON-serialisable.
    """

    user_id: str = Field(
        ...,
        description="User's phone number in E.164 format without '+' (e.g. '919876543210')",
        examples=["919876543210"],
    )
    flow: FlowName = Field(
        default=FlowName.START,
        description="The currently active conversation flow.",
    )
    step: int = Field(
        default=0,
        ge=0,
        description="Step index within the active flow (0-indexed).",
    )
    language: Language = Field(
        default=Language.ENGLISH,
        description="User's preferred language for bot replies.",
    )
    intent: str | None = Field(
        default=None,
        description="Detected user intent from the last message, if any.",
    )
    data: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Arbitrary key-value store for flow-specific state "
            "(e.g. collected symptoms, city, report URL)."
        ),
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "919876543210",
                    "flow": "symptoms",
                    "step": 2,
                    "language": "en",
                    "intent": None,
                    "data": {
                        "main_symptom": "headache",
                        "duration": "2 days",
                    },
                }
            ]
        }
    }

    def reset(self) -> "SessionState":
        """Return a fresh session for the same user (keeps user_id + language)."""
        return SessionState(user_id=self.user_id, language=self.language)

    def advance(self) -> "SessionState":
        """Return a copy of this session with step incremented by 1."""
        return self.model_copy(update={"step": self.step + 1})

    def transition(self, flow: FlowName) -> "SessionState":
        """Return a copy of this session switched to a new flow at step 0."""
        return self.model_copy(update={"flow": flow, "step": 0, "data": {}})
