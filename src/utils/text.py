import hashlib
import re
from bs4 import BeautifulSoup

def clean_text(value: str) -> str:
    if not value:
        return ""
    value = BeautifulSoup(value, "html.parser").get_text(" ")
    value = re.sub(r"\s+", " ", value).strip()
    return value

def normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (value or "").lower()).strip()

def make_job_id(title: str, employer: str, location: str, url: str) -> str:
    raw = "|".join([normalize(title), normalize(employer), normalize(location), url.strip().lower()])
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:24]

def extract_salary(text: str) -> str:
    patterns = [r"£\s?\d{2,3}[,]?\d{0,3}\s?(?:-|to)?\s?£?\s?\d{0,3}[,]?\d{0,3}", r"\d{2,3}k\s?(?:-|to)?\s?\d{0,3}k"]
    for p in patterns:
        m = re.search(p, text or "", re.I)
        if m:
            return m.group(0)
    return "Not specified"

def extract_location(text: str) -> str:
    places = ["Swindon", "Bristol", "Exeter", "Reading", "Oxford", "Cambridge", "London", "Cardiff", "Birmingham", "Manchester", "Leeds", "Remote", "Hybrid", "United Kingdom", "UK", "Scotland", "Wales"]
    text_low = (text or "").lower()
    for p in places:
        if p.lower() in text_low:
            return p
    return "Not specified"
