from datetime import datetime, timezone

all_codes = {}

def save(code, url, ):
    all_codes[code] = {
        "long_url": url,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "click_count": 0,
    }

def get_url(code):
    return all_codes.get(code, None)

def exists(code):
    return code in all_codes

def increment_click_count(code):
    if code in all_codes:
        print(f"Incrementing click count for {code}. Current count: {all_codes[code]['click_count']}")
        all_codes[code]['click_count'] += 1
        return all_codes[code]['click_count']
    return None

def get_click_count(code):
    if code in all_codes:
        print(f"Click count for {code}: {all_codes[code]['click_count']}")
        return all_codes[code]['click_count']
    return None

def delete_all_codes():
    all_codes.clear()

if __name__ == "__main__":
    from code_generator import random_code_generator, generate_unique_code
    for i in range(3):
        code = generate_unique_code(8)
        save(code, f"https://example.com/{i}")
        print(code, get_url(code))
        increment_click_count(code)
        print("after click:", get_url(code)["click_count"])
    delete_all_codes()