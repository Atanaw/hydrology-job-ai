from src.models import Job
from src.utils.text import make_job_id

HYDROLOGY_QUERIES = ["hydrologist", "flood risk", "water resources", "catchment", "climate resilience"]

class ManualURLSource:
    """Creates monitored-source records for career sites that need manual/APify/API search.
    These appear in the dashboard so the user can click and review them.
    """
    def __init__(self, source_config):
        self.cfg = source_config

    def fetch(self):
        jobs = []
        for q in HYDROLOGY_QUERIES[:2]:
            title = f"Check {self.cfg['name']} for {q} roles"
            employer = self.cfg["name"].replace(" Careers", "").replace(" Jobs", "")
            location = "United Kingdom"
            desc = f"Manual or approved-connector check recommended for {q}, hydrology, flood risk, water resources, catchment management and environmental roles."
            url = self.cfg["url"]
            jid = make_job_id(title, employer, location, url + q)
            jobs.append(Job(id=jid, title=title, employer=employer, location=location, salary="Not specified", description=desc, url=url, source=self.cfg["name"], employer_type=self.cfg.get("employer_type", "unknown")))
        return jobs
