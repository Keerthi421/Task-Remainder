from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class TaskReminderRequest(BaseModel):
    """Schema for Smart Task Reminder Request"""
    task: str = Field(..., description="Task name (e.g., Math Assignment)")
    deadline: str = Field(..., description="Deadline in format: YYYY-MM-DD HH:MM")
    difficulty: str = Field(..., description="Difficulty level: easy, medium, hard")

    class Config:
        json_schema_extra = {
            "example": {
                "task": "Math Assignment",
                "deadline": "2026-01-15 23:59",
                "difficulty": "hard"
            }
        }


class TaskReminderResponse(BaseModel):
    """Schema for Smart Task Reminder Response"""
    task: str
    deadline: str
    difficulty: str
    reminders: List[str]
    time_pressure_score: int
    days_remaining: int


class FixedReminderRequest(BaseModel):
    """Schema for Fixed-Time Reminder Request"""
    title: str = Field(..., description="Reminder title (e.g., Take Paracetamol)")
    time: str = Field(..., description="Time in HH:MM format (e.g., 17:00)")
    frequency: str = Field(..., description="Frequency: daily, weekly, custom")
    days_ahead: int = Field(3, description="Number of days to generate reminders for")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Take Paracetamol",
                "time": "17:00",
                "frequency": "daily",
                "days_ahead": 3
            }
        }


class FixedReminderResponse(BaseModel):
    """Schema for Fixed-Time Reminder Response"""
    title: str
    time: str
    frequency: str
    next_reminders: List[str]
