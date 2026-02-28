"""Seed demo seasons/episodes for quick UI preview.
Run: python scripts/seed_demo.py
"""
import os
from datetime import datetime
from app import create_app, db
from app.models import Season, Episode

app = create_app()

with app.app_context():
    if Season.query.count() > 0:
        print("Already has data; skipping.")
        raise SystemExit(0)

    s1 = Season(number=1, title="Temporada 1", description="Primeira temporada", is_published=True)
    db.session.add(s1)
    db.session.commit()

    # replace with your own unlisted ids/urls
    demo_ids = ["dQw4w9WgXcQ"]*5
    titles = ["O Presente", "O Recomeço", "O Recomeço", "O Recomeço", "O Recomeço"]
    durations = [43, 41, 41, 41, 41]
    for i, vid in enumerate(demo_ids, start=1):
        ep = Episode(
            season_id=s1.id,
            episode_number=i,
            title=titles[i-1],
            duration_minutes=durations[i-1],
            youtube_url=vid,
            aspect="vertical",
            is_published=True,
        )
        db.session.add(ep)

    for n in range(2,7):
        db.session.add(Season(number=n, title=f"Temporada {n}", is_published=True))
    db.session.commit()
    print("Seeded demo data.")
