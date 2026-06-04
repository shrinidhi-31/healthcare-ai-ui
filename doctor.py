"""
Doctor schemas — discovery and recommendation flow.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class DoctorSearchRequest(BaseModel):
    """
    Input collected by the Doctor Flow before querying the registry.
    """

    city: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="City in which to search for doctors.",
        examples=["Bengaluru"],
    )
    specialization: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Medical specialization to filter by.",
        examples=["Cardiologist", "General Physician", "Neurologist"],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [{"city": "Bengaluru", "specialization": "Cardiologist"}]
        }
    }


class Doctor(BaseModel):
    """
    A single doctor record returned by the Doctor Flow.
    """

    doctor_id: str = Field(..., description="Unique identifier for the doctor.")
    name: str = Field(..., description="Full name including salutation (e.g. 'Dr. Priya Sharma').")
    specialization: str = Field(..., description="Medical specialization.")
    hospital: str = Field(..., description="Hospital or clinic name.")
    city: str = Field(..., description="City where the doctor practices.")
    phone: str | None = Field(default=None, description="Contact phone number.")
    address: str | None = Field(default=None, description="Clinic / hospital address.")
    available_days: list[str] | None = Field(
        default=None,
        description="Days of the week the doctor is available.",
        examples=[["Monday", "Wednesday", "Friday"]],
    )
    rating: float | None = Field(
        default=None,
        ge=0.0,
        le=5.0,
        description="Average patient rating out of 5.",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "doctor_id": "doc_001",
                    "name": "Dr. Priya Sharma",
                    "specialization": "Cardiologist",
                    "hospital": "Apollo Hospitals",
                    "city": "Bengaluru",
                    "phone": "+91-80-12345678",
                    "address": "Bannerghatta Road, Bengaluru - 560076",
                    "available_days": ["Monday", "Wednesday", "Friday"],
                    "rating": 4.8,
                }
            ]
        }
    }

    def format_for_whatsapp(self) -> str:
        """
        Returns a compact string suitable for a WhatsApp message.

        Example output:
            🩺 Dr. Priya Sharma (Cardiologist)
            🏥 Apollo Hospitals, Bengaluru
            📞 +91-80-12345678
            📅 Mon, Wed, Fri
        """
        days = ", ".join(self.available_days[:3]) if self.available_days else "Call to confirm"
        phone_line = f"📞 {self.phone}\n" if self.phone else ""
        return (
            f"🩺 *{self.name}* ({self.specialization})\n"
            f"🏥 {self.hospital}, {self.city}\n"
            f"{phone_line}"
            f"📅 {days}"
        )
