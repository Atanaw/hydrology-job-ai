from src.sources.rss_source import RSSSource
from src.sources.public_search import PublicSearchSource
from src.sources.manual_url import ManualURLSource
from src.sources.apify_source import ApifySource

SOURCE_CLASSES = {
    "rss": RSSSource,
    "public_search": PublicSearchSource,
    "manual_url": ManualURLSource,
    "apify": ApifySource,
}

class SourceManager:
    def __init__(self, source_config):
        self.sources = [s for s in source_config.get("sources", []) if s.get("enabled", False)]

    def fetch_all(self):
        all_jobs = []
        for cfg in self.sources:
            cls = SOURCE_CLASSES.get(cfg.get("type"))
            if not cls:
                continue
            try:
                jobs = cls(cfg).fetch()
                print(f"{cfg['name']}: {len(jobs)} records")
                all_jobs.extend(jobs)
            except Exception as e:
                print(f"Source failed: {cfg.get('name')} | {e}")
        return all_jobs
