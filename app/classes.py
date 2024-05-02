from pydantic import BaseModel

class UserProfile(BaseModel):
    email: str
    linkedin_url: str

class EmailBody(BaseModel):
    email: str

class JobStructure(BaseModel):
    title: str
    subtitle: str
    caption: str
    metadata: str
