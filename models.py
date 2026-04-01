# models.py
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class InquiryEntry(BaseModel):
    character: str
    question: str
    response: str

class Scenario(BaseModel):
    scenario: str
    highlighted_scenario: str
    characters: List[str]

class WitnessResponse(BaseModel):
    response: str

class Analysis(BaseModel):
    thought_process: str
    analysis: str
    highlighted_analysis: str

class CaseRecord(BaseModel):
    case_id: str
    date: str = Field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    player_name: str
    difficulty: str
    scenario: str
    inquiry_history: List[InquiryEntry] = []
    judgment: str
    analysis: str
