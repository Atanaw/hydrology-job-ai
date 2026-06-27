from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

_CACHE = {}

def allowed(url: str, user_agent: str = "HydrologyJobAIPro") -> bool:
    try:
        parsed = urlparse(url)
        root = f"{parsed.scheme}://{parsed.netloc}"
        robots_url = root + "/robots.txt"
        if robots_url not in _CACHE:
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            _CACHE[robots_url] = rp
        return _CACHE[robots_url].can_fetch(user_agent, url)
    except Exception:
        return False
