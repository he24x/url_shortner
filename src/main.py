from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from .code_generator import generate_unique_code
from .database import get_url, increment_click_count, save, get_click_count
from .models import URLRequest, URLResponse, ClickCountResponse

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/shorten")
async def shorten_url(url: URLRequest):
    short_code = generate_unique_code(8)
    save(short_code, str(url.url))
    return URLResponse(url=str(url.url), shortcode=short_code)

@app.get("/clicks/{short_code}")
def read_click_count(short_code: str):  
    clicks = get_click_count(short_code)
    if clicks is None:
        raise HTTPException(status_code=404, detail="Short code not found")
    return ClickCountResponse(short_code=short_code, clicks=clicks)

@app.get("/{short_code}")
async def redirect_to_url(short_code: str):
    url = get_url(short_code)
    print(f"Redirecting to URL: {url}")
    if url:
        increment_click_count(short_code)
        print(f"Click count for {short_code}: {get_click_count(short_code)}")
        return RedirectResponse(str(url["long_url"]))
    else:
        raise HTTPException(status_code=404, detail="Short code not found")
