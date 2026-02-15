from datetime import date
import decimal
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
'''
# Schema for standards
class StandardsRead(BaseModel):
    code: str
    name: str
    is_default: bool
    description: Optional[str]
    model_config = ConfigDict(from_attributes=True)

# Schema for EF Versions
class EfVersionsRead(BaseModel):
    ef_id: int
    version: str
    description: Optional[str] = None
    ipcc_valid_from: Optional[date] = None
    ipcc_valid_till: Optional[date] = None
    ghg_valid_from: Optional[date] = None
    ghg_valid_till: Optional[date] = None
    defra_valid_from: Optional[date] = None
    defra_valid_till: Optional[date] = None
    epa_valid_from: Optional[date] = None
    epa_valid_till: Optional[date] = None
    year: int
    isCurrent: bool
    model_config = ConfigDict(extra="ignore", from_attributes=True)
class EfVersionsResponse(BaseModel):
    success:bool
    message:str
    versions_available:List[EfVersionsRead]
    model_config = ConfigDict(extra="ignore")

# Bioenergy input
class BioenergyInput(BaseModel):
    type_:str =  Field(alias="_type")
    fuel: str
    unit: str
    consumption_value: float
    emission_scope:str

# Hotel input
class HotelInput(BaseModel):
    country: str
    rooms: int
    nights_per_room: int
    emission_scope:str

# Assessment input
class AssessmentInput(BaseModel):
    start_date: date
    end_date: date
    description:Optional[str] = None
    bioenergyList: Optional[List[BioenergyInput]] = Field(None, alias="bioenergy")
    hotelList: Optional[List[HotelInput]] = Field(None, alias="hotel")
    model_config = ConfigDict(extra="ignore")
class AssessmentResultsCreate(BaseModel):
    assessment_id: int
    ef_id: Optional[int] = None
    category: str
    standard_used: Optional[str] = None
    details: dict
    emissions_tonnes: float
    model_config = ConfigDict(extra="ignore")
class LockAssessmentInput(BaseModel):
    start_date:Optional[date] = None
    end_date:Optional[date] = None
    assessment_id:Optional[int] = None
'''
class UrlCreate(BaseModel):
    short_url: str
    long_url: str
    model_config = ConfigDict(extra="ignore")
