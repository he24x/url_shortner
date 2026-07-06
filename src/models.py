from pydantic import BaseModel, HttpUrl

class URLRequest(BaseModel):
    url: HttpUrl

class URLResponse(BaseModel):
    url: HttpUrl
    shortcode: str

class ClickCountResponse(BaseModel):
    short_code: str
    clicks: int