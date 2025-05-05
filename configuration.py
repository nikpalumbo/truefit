"""
User-specific configuration schema for LangGraph sessions.
"""

from pydantic import BaseModel

class Configuration(BaseModel):
    user_id: str
