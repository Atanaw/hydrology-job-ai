from typing import Dict, List, Tuple
from src.utils.text import normalize

WEIGHTS = {"title": 0.40, "description": 0.30, "location": 0.10, "seniority": 0.10, "employer": 0.10}

class JobScorer:
    def __init__(self, keyword_config: Dict):
        self.primary = keyword_config["include_keywords"]["primary"]
        self.secondary = keyword_config["include_keywords"].get("secondary", [])
        self.exclude_terms = keyword_config.get("exclude_terms", [])
        self.location_high = keyword_config.get("location_preferences", {}).get("high", [])
        self.location_medium = keyword_config.get("location_preferences", {}).get("medium", [])
        self.seniority = keyword_config.get("seniority_terms", {})

    def matched(self, text: str) -> List[str]:
        norm = normalize(text)
        kws = []
        for kw in self.primary + self.secondary:
            if normalize(kw) in norm:
                kws.append(kw)
        return sorted(set(kws))

    def excluded(self, text: str) -> bool:
        norm = normalize(text)
        return any(normalize(term) in norm for term in self.exclude_terms)

    def passes_filter(self, job) -> bool:
        full = f"{job.title} {job.description}"
        if self.excluded(full):
            return False
        title_matches = self.matched(job.title)
        desc_matches = self.matched(job.description)
        return bool(title_matches) or len(desc_matches) >= 2

    def score(self, job) -> Tuple[int, List[str], str]:
        title_matches = self.matched(job.title)
        desc_matches = self.matched(job.description)
        matched = sorted(set(title_matches + desc_matches))
        title_score = min(len(title_matches) / 3, 1) * 100
        desc_score = min(len(desc_matches) / 8, 1) * 100
        loc_norm = normalize(job.location)
        if any(normalize(x) in loc_norm for x in self.location_high):
            location_score = 100
        elif any(normalize(x) in loc_norm for x in self.location_medium):
            location_score = 75
        else:
            location_score = 45
        full_norm = normalize(f"{job.title} {job.description}")
        senior_terms = self.seniority.get("senior", [])
        seniority_score = 70 if any(normalize(x) in full_norm for x in senior_terms) else 100
        employer_score = 100 if job.employer_type in ["water_company", "consultancy", "university", "public", "international"] else 60
        score = int(round(title_score*WEIGHTS["title"] + desc_score*WEIGHTS["description"] + location_score*WEIGHTS["location"] + seniority_score*WEIGHTS["seniority"] + employer_score*WEIGHTS["employer"]))
        priority = "high" if score >= 85 else "alert" if score >= 70 else "normal"
        return score, matched, priority
