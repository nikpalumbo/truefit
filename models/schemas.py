"""
Shared Pydantic models used for memory extraction and tool communication.
"""

from typing import Optional, Literal, TypedDict
from pydantic import BaseModel, Field

class CompanyInfo(BaseModel):
    name: Optional[str] = Field(description="Company name")
    website: Optional[str] = Field(description="Company website")
    values: list[str] = Field(description="Company values", default_factory=list)
    mission: Optional[str] = Field(description="Company mission")
    description: Optional[str] = Field(description="Brief company description")
    role_title: Optional[str] = Field(description="Job title being applied for")
    job_description: Optional[str] = Field(description="Full job description text")
    cover_letter: Optional[str] = Field(description="Finalized cover letter text")
    cover_letter_created_at: Optional[str] = Field(description="Timestamp of cover letter creation")

class Profile(BaseModel):
    fullname: Optional[str] = Field(description="User Full Name")
    values: list[str] = Field(description="The user's core values")
    personality_traits: list[str] = Field(description="Key personality traits")
    interests: list[str] = Field(description="Industries/domains the user is interested in")
    resume: Optional[str] = Field(description="The user's resume or professional background")

class UpdateMemory(TypedDict):
    """Decision on what memory type to update"""
    update_type: Literal['user', 'company', 'company_info', 'review']