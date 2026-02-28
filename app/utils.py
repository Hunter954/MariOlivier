import re

YOUTUBE_ID_RE = re.compile(
    r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|embed/|shorts/))([A-Za-z0-9_-]{11})"
)

def extract_youtube_id(url: str) -> str | None:
    if not url:
        return None
    m = YOUTUBE_ID_RE.search(url)
    return m.group(1) if m else None

def youtube_embed_url(url: str) -> str:
    vid = extract_youtube_id(url) or url.strip()
    # Privacy-enhanced mode
    return f"https://www.youtube-nocookie.com/embed/{vid}?rel=0&modestbranding=1"
