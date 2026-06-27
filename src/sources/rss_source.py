import feedparser
from src.models import Job
from src.utils.text import clean_text, extract_location, extract_salary, make_job_id

class RSSSource:
    def __init__(self, source_config):
        self.cfg = source_config

    def fetch(self):
        feed = feedparser.parse(self.cfg["url"])
        jobs = []
        for entry in feed.entries:
            title = clean_text(entry.get("title", ""))
            url = entry.get("link", "")
            desc = clean_text(entry.get("summary", entry.get("description", "")))
            employer = clean_text(entry.get("author", "Not specified")) or "Not specified"
            location = extract_location(f"{title} {desc}")
            salary = extract_salary(desc)
            jid = make_job_id(title, employer, location, url)
            jobs.append(Job(id=jid, title=title, employer=employer, location=location, salary=salary, description=desc, url=url, source=self.cfg["name"], employer_type=self.cfg.get("employer_type", "unknown")))
        return jobs
