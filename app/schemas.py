
from pydantic import BaseModel, Field, ConfigDict,HttpUrl

class ShortenUrlInput(BaseModel):
    longurl: HttpUrl
    model_config = ConfigDict(extra="ignore")
