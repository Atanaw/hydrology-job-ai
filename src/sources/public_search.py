import requests
from bs4 import BeautifulSoup
from src.models import Job
from src.utils.text import clean_text, extract_location, extract_salary, make_job_id
from src.utils.robots import allowed

class PublicSearchSource:
    """Generic low-risk public search-page parser. It only extracts obvious anchors and snippets.
    Use only for pages allowed by robots.txt and site terms.
    """
    def __init__(self, source_config):
        self.cfg = source_config

    def fetch(self):
        url = self.cfg["url"]
        if not allowed(url):
            print(f"Skipping due to robots.txt or unavailable robots: {self.cfg['name']}")
            return []
        headers = {"User-Agent": "HydrologyJobAIPro/1.0"}
        r = requests.get(url, headers=headers, timeout=25)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        jobs = []
        for a in soup.select("a[href]")[:80]:
            title = clean_text(a.get_text(" "))
            href = a.get("href", "")
            if not title or len(title) < 8:
                continue
            if href.startswith("/"):
                from urllib.parse import urljoin
                href = urljoin(url, href)
            parent = a.find_parent()
            desc = clean_text(parent.get_text(" ") if parent else title)
            location = extract_location(desc)
            salary = extract_salary(desc)
            employer = self.cfg.get("name", "Not specified")
            jid = make_job_id(title, employer, location, href)
            jobs.append(Job(id=jid, title=title, employer=employer, location=location, salary=salary, description=desc, url=href, source=self.cfg["name"], employer_type=self.cfg.get("employer_type", "unknown")))
        return jobs
