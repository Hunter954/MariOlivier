from datetime import datetime
from flask import Blueprint, render_template, abort, request
from flask_login import login_required, current_user
from ..models import Season, Episode
from ..utils import youtube_embed_url

main_bp = Blueprint("main", __name__)

@main_bp.get("/")
@login_required
def home():
    # Temporada atual = maior number publicada
    seasons = Season.query.filter_by(is_published=True).order_by(Season.number.desc()).all()
    current_season = seasons[0] if seasons else None

    continue_episode = None
    if current_season:
        continue_episode = (
            Episode.query.filter_by(season_id=current_season.id, is_published=True)
            .order_by(Episode.episode_number.asc())
            .first()
        )

    upcoming_eps = []
    if current_season:
        q = Episode.query.filter_by(season_id=current_season.id, is_published=True)
        # Se tiver release_at futuro, prioriza próximos; senão pega próximos por número
        now = datetime.utcnow()
        future = q.filter(Episode.release_at.isnot(None), Episode.release_at > now).order_by(Episode.release_at.asc()).limit(4).all()
        if future:
            upcoming_eps = future
        else:
            # pega eps 2..5 como no layout
            upcoming_eps = q.order_by(Episode.episode_number.asc()).offset(1).limit(4).all()

    next_seasons = Season.query.filter(Season.is_published == True).order_by(Season.number.asc()).all()
    return render_template(
        "main/home.html",
        user=current_user,
        current_season=current_season,
        continue_episode=continue_episode,
        upcoming_eps=upcoming_eps,
        next_seasons=next_seasons,
    )

@main_bp.get("/temporadas")
@login_required
def temporadas():
    seasons = Season.query.filter_by(is_published=True).order_by(Season.number.asc()).all()
    return render_template("main/temporadas.html", seasons=seasons, user=current_user)

@main_bp.get("/temporada/<int:season_id>")
@login_required
def temporada_detail(season_id: int):
    season = Season.query.get_or_404(season_id)
    if not season.is_published and not current_user.is_admin:
        abort(404)
    episodes = Episode.query.filter_by(season_id=season.id).order_by(Episode.episode_number.asc()).all()
    return render_template("main/temporada_detail.html", season=season, episodes=episodes, user=current_user)

@main_bp.get("/assistir/<int:episode_id>")
@login_required
def assistir(episode_id: int):
    ep = Episode.query.get_or_404(episode_id)
    if (not ep.is_published or not ep.season.is_published) and (not current_user.is_admin):
        abort(404)
    embed = youtube_embed_url(ep.youtube_url)
    return render_template("main/watch.html", ep=ep, embed_url=embed, user=current_user)
