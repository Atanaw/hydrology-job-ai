import os
import requests
from src.models import Job
from src.utils.text import clean_text, extract_salary, make_job_id

class ApifySource:
    """Compliant connector for LinkedIn/Indeed/Reed/Totaljobs/CV-Library/Monster through Apify.
    You must provide an APIFY_TOKEN and confirm actor terms.
    Actor input schemas vary; edit build_actor_input for your selected actor.
    """
    def __init__(self, source_config):
        self.cfg = source_config
        self.token = os.getenv("APIFY_TOKEN")

    def build_actor_input(self):
        return {
            "keywords": "hydrologist OR flood risk OR water resources OR catchment management",
            "location": "United Kingdom",
            "maxItems": 25,
            "action": "search"
        }

    def fetch(self):
        if not self.token:
            print(f"Skipping {self.cfg['name']}: APIFY_TOKEN missing")
            return []
        actor = self.cfg.get("actor")
        if not actor:
            return []
        url = f"https://api.apify.com/v2/acts/{actor.replace('/', '~')}/run-sync-get-dataset-items?token={self.token}"
        r = requests.post(url, json=self.build_actor_input(), timeout=120)
        r.raise_for_status()
        items = r.json()
        jobs = []
        for item in items:
            title = clean_text(item.get("title") or item.get("jobTitle") or "")
            employer = clean_text(item.get("company") or item.get("employer") or "Not specified")
            location = clean_text(item.get("location") or "United Kingdom")
            desc = clean_text(item.get("description") or item.get("snippet") or "")
            job_url = item.get("url") or item.get("link") or item.get("jobUrl") or ""
            salary = clean_text(item.get("salary") or extract_salary(desc))
            if not title or not job_url:
                continue
            jid = make_job_id(title, employer, location, job_url)
            jobs.append(Job(id=jid, title=title, employer=employer, location=location, salary=salary, description=desc, url=job_url, source=self.cfg["name"], employer_type=self.cfg.get("employer_type", "mixed")))
        return jobs
