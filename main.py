from src.utils.config_loader import load_yaml
from src.sources.manager import SourceManager
from src.utils.scoring import JobScorer
from src.storage.database import Database
from src.storage.sheets import GoogleSheetsClient
from src.alerts.emailer import EmailAlert
from src.ai.drafter import AIDrafter


def main():
    source_cfg = load_yaml("config/sources.yml")
    keyword_cfg = load_yaml("config/keywords.yml")

    source_manager = SourceManager(source_cfg)
    scorer = JobScorer(keyword_cfg)
    db = Database()
    sheets = GoogleSheetsClient()
    drafter = AIDrafter()
    emailer = EmailAlert()

    raw_jobs = source_manager.fetch_all()
    matched = []

    for job in raw_jobs:
        if scorer.passes_filter(job):
            score, keywords, priority = scorer.score(job)
            job.score = score
            job.matched_keywords = keywords
            job.priority = priority
            matched.append(job)

    new_jobs = db.upsert_jobs(matched)
    alert_jobs = [j for j in new_jobs if j.score >= 70]
    high_jobs = [j for j in new_jobs if j.score >= 85]

    drafts = drafter.generate_for_jobs(alert_jobs)

    sheets.append_jobs(new_jobs)
    sheets.append_drafts(drafts)
    sheets.update_summary(db.counts())

    emailer.send(alert_jobs)

    print("SUMMARY")
    print(f"Raw records: {len(raw_jobs)}")
    print(f"Matched: {len(matched)}")
    print(f"New: {len(new_jobs)}")
    print(f"Alerts: {len(alert_jobs)}")
    print(f"High priority: {len(high_jobs)}")

if __name__ == "__main__":
    main()
