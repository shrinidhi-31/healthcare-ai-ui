"""
Alert schemas — emergency alert lifecycle.

Alerts are created by the Emergency Flow when red-flag symptoms are detected
and are surfaced on the Admin Dashboard.
"""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class AlertSeverity(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class AlertStatus(str, Enum):
    OPEN = "open"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"


# ---------------------------------------------------------------------------
# Request / command schemas
# ---------------------------------------------------------------------------


class AlertCreate(BaseModel):
    """
    Payload for POST /alerts (internal).

    Sent by the Emergency Flow to Alert Service.
    """

    user_id: str = Field(
        ...,
        description="Phone number of the affected user.",
        examples=["919876543210"],
    )
    severity: AlertSeverity = Field(
        default=AlertSeverity.HIGH,
        description="Triage severity level.",
    )
    reason: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Human-readable reason for the alert.",
        examples=["Chest pain detected"],
    )
    symptoms: list[str] = Field(
        default_factory=list,
        description="List of reported symptoms that triggered the alert.",
        examples=[["chest pain", "shortness of breath"]],
    )
    session_snapshot: dict[str, Any] | None = Field(
        default=None,
        description="Snapshot of the user's session at the time of alert creation.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "919876543210",
                    "severity": "HIGH",
                    "reason": "Chest pain detected",
                    "symptoms": ["chest pain", "shortness of breath"],
                    "session_snapshot": {"flow": "emergency", "step": 1, "language": "en"},
                }
            ]
        }
    }


class AlertUpdate(BaseModel):
    """
    Payload for PATCH /alerts/{alert_id}.

    Used by admin dashboard to change alert status.
    """

    status: AlertStatus = Field(..., description="New status to set on the alert.")

    model_config = {
        "json_schema_extra": {
            "examples": [{"status": "acknowledged"}]
        }
    }


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------


class Alert(BaseModel):
    """
    Full alert representation returned by GET /alerts and GET /alerts/{id}.
    """

    alert_id: str = Field(..., description="Unique alert identifier.")
    user_id: str = Field(..., description="Phone number of the affected user.")
    severity: AlertSeverity
    reason: str
    status: AlertStatus = AlertStatus.OPEN
    symptoms: list[str] = Field(default_factory=list)
    session_snapshot: dict[str, Any] | None = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp when the alert was created.",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="UTC timestamp of the last status change.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "alert_id": "alert_01HXK2J4",
                    "user_id": "919876543210",
                    "severity": "HIGH",
                    "reason": "Chest pain detected",
                    "status": "open",
                    "symptoms": ["chest pain", "shortness of breath"],
                    "session_snapshot": {"flow": "emergency", "step": 1, "language": "en"},
                    "created_at": "2024-11-15T10:30:00Z",
                    "updated_at": "2024-11-15T10:30:00Z",
                }
            ]
        }
    }

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def ensure_utc(cls, v: Any) -> datetime:
        if isinstance(v, str):
            return datetime.fromisoformat(v.replace("Z", "+00:00"))
        return v


class AlertListResponse(BaseModel):
    """Paginated list of alerts returned by GET /alerts."""

    total: int = Field(..., description="Total number of matching alerts (before pagination).")
    alerts: list[Alert]

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "total": 1,
                    "alerts": [
                        {
                            "alert_id": "alert_01HXK2J4",
                            "user_id": "919876543210",
                            "severity": "HIGH",
                            "reason": "Chest pain detected",
                            "status": "open",
                            "symptoms": ["chest pain"],
                            "session_snapshot": None,
                            "created_at": "2024-11-15T10:30:00Z",
                            "updated_at": "2024-11-15T10:30:00Z",
                        }
                    ],
                }
            ]
        }
    }
