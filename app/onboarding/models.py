from pydantic import BaseModel
from typing import List, Optional

class Country(BaseModel):
    code: str
    name: str

class Language(BaseModel):
    code: str
    name: str

class Artist(BaseModel):
    id: str
    name: str
    genres: List[str]
    image: Optional[str] = None

class Mode(BaseModel):
    id: str
    name: str
    emoji: str

class UserOnboardingData(BaseModel):
    country_code: str
    language_code: str
    artist_ids: List[str]
    mode_ids: List[str]
