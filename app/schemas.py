"""Defines what information the website sends to the server."""
from typing import Literal
from pydantic import BaseModel, Field


class PatientInput(BaseModel):
    age: int = Field(ge=0, le=120)
    sex: Literal["female", "male", "other"]
    symptoms: str = Field(min_length=10, max_length=3000)
    duration: str = Field(default="", max_length=200)
    conditions: str = Field(default="", max_length=1000)
    medications: str = Field(default="", max_length=1000)
    access_code: str = Field(default="", max_length=100)


def format_patient(p: PatientInput) -> str:
    """Turns the form into one block of text that every agent receives."""
    return (
        f"Age: {p.age}\n"
        f"Sex: {p.sex}\n"
        f"Symptoms (patient's own words): {p.symptoms}\n"
        f"How long: {p.duration or 'not stated'}\n"
        f"Known medical conditions: {p.conditions or 'none stated'}\n"
        f"Current medications: {p.medications or 'none stated'}"
    )
