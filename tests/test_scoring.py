from src.utils.scoring import JobScorer
from src.models import Job

cfg = {
    "include_keywords": {"primary": ["hydrology", "flood risk"], "secondary": ["GIS"]},
    "exclude_terms": ["sales"],
    "location_preferences": {"high": ["UK"], "medium": []},
    "seniority_terms": {"senior": ["senior"]}
}

def test_score():
    scorer = JobScorer(cfg)
    job = Job(id="1", title="Hydrologist", employer="Test", location="UK", salary="", description="Flood risk and GIS", url="x")
    assert scorer.passes_filter(job)
    score, kws, priority = scorer.score(job)
    assert score > 70
