from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class Job:
    id: str
    title: str
    employer: str
    location: str
    salary: str
    description: str
    url: str
    source: str
    employer_type: str = "unknown"
    score: int = 0
    matched_keywords: List[str] = field(default_factory=list)
    priority: str = "normal"
    status: str = "new"
    scraped_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    deadline: Optional[str] = None
