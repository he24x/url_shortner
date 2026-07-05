from fastapi import FastAPI
from .code_generator import generate_unique_code
from .database import get_url, increment_click_count, save, get_click_count

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/shorten")
async def shorten_url(url: str):
    short_code = generate_unique_code(8)
    save(short_code, url)
    return {"short_code": short_code, "url": url}

@app.get("/clicks/{short_code}")
def read_click_count(short_code: str):  
    clicks = get_click_count(short_code)
    if clicks is None:
        return {"error": "Short code not found"}
    return {"short_code": short_code, "clicks": clicks}

@app.get("/{short_code}")
async def redirect_to_url(short_code: str):
    url = get_url(short_code)
    print(f"Redirecting to URL: {url}")
    if url:
        increment_click_count(short_code)
        print(f"Click count for {short_code}: {get_click_count(short_code)}")
        return {"url": url["long_url"]}
    else:
        return {"error": "Short code not found"}