from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from .. import db
from ..models import Season, Episode, User
from ..forms import SeasonForm, EpisodeForm

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

def admin_only():
    if not current_user.is_authenticated or not current_user.is_admin:
        abort(403)

@admin_bp.get("/")
@login_required
def index():
    admin_only()
    seasons = Season.query.order_by(Season.number.desc()).all()
    episodes = Episode.query.order_by(Episode.created_at.desc()).limit(10).all()
    users = User.query.order_by(User.created_at.desc()).limit(10).all()
    return render_template("admin/index.html", seasons=seasons, episodes=episodes, users=users)

@admin_bp.get("/temporadas/nova")
@login_required
def season_new():
    admin_only()
    form = SeasonForm()
    form.is_published.data = True
    return render_template("admin/season_form.html", form=form, mode="new")

@admin_bp.post("/temporadas/nova")
@login_required
def season_new_post():
    admin_only()
    form = SeasonForm()
    if not form.validate_on_submit():
        flash("Revise os campos.", "error")
        return render_template("admin/season_form.html", form=form, mode="new"), 400
    s = Season(
        number=form.number.data,
        title=form.title.data,
        description=form.description.data,
        thumbnail_url=form.thumbnail_url.data,
        is_published=bool(form.is_published.data),
    )
    db.session.add(s)
    db.session.commit()
    flash("Temporada criada.", "success")
    return redirect(url_for("admin.index"))

@admin_bp.get("/temporadas/<int:season_id>/editar")
@login_required
def season_edit(season_id: int):
    admin_only()
    s = Season.query.get_or_404(season_id)
    form = SeasonForm(obj=s)
    return render_template("admin/season_form.html", form=form, mode="edit", season=s)

@admin_bp.post("/temporadas/<int:season_id>/editar")
@login_required
def season_edit_post(season_id: int):
    admin_only()
    s = Season.query.get_or_404(season_id)
    form = SeasonForm()
    if not form.validate_on_submit():
        flash("Revise os campos.", "error")
        return render_template("admin/season_form.html", form=form, mode="edit", season=s), 400
    s.number = form.number.data
    s.title = form.title.data
    s.description = form.description.data
    s.thumbnail_url = form.thumbnail_url.data
    s.is_published = bool(form.is_published.data)
    db.session.commit()
    flash("Temporada atualizada.", "success")
    return redirect(url_for("admin.index"))

@admin_bp.post("/temporadas/<int:season_id>/delete")
@login_required
def season_delete(season_id: int):
    admin_only()
    s = Season.query.get_or_404(season_id)
    db.session.delete(s)
    db.session.commit()
    flash("Temporada removida.", "success")
    return redirect(url_for("admin.index"))

@admin_bp.get("/episodios/novo")
@login_required
def episode_new():
    admin_only()
    form = EpisodeForm()
    # quick: allow prefill season_id
    sid = request.args.get("season_id", type=int)
    if sid:
        form.season_id.data = sid
    form.is_published.data = True
    form.aspect.data = "vertical"
    return render_template("admin/episode_form.html", form=form, mode="new")

@admin_bp.post("/episodios/novo")
@login_required
def episode_new_post():
    admin_only()
    form = EpisodeForm()
    if not form.validate_on_submit():
        flash("Revise os campos.", "error")
        return render_template("admin/episode_form.html", form=form, mode="new"), 400

    season = Season.query.get(form.season_id.data)
    if not season:
        flash("Temporada não encontrada (ID inválido).", "error")
        return render_template("admin/episode_form.html", form=form, mode="new"), 400

    ep = Episode(
        season_id=season.id,
        episode_number=form.episode_number.data,
        title=form.title.data,
        description=form.description.data,
        duration_minutes=form.duration_minutes.data,
        youtube_url=form.youtube_url.data,
        thumbnail_url=form.thumbnail_url.data,
        aspect=form.aspect.data,
        is_published=bool(form.is_published.data),
        release_at=form.release_at.data,
    )
    db.session.add(ep)
    db.session.commit()
    flash("Episódio criado.", "success")
    return redirect(url_for("admin.index"))

@admin_bp.get("/episodios/<int:episode_id>/editar")
@login_required
def episode_edit(episode_id: int):
    admin_only()
    ep = Episode.query.get_or_404(episode_id)
    form = EpisodeForm(obj=ep)
    form.season_id.data = ep.season_id
    return render_template("admin/episode_form.html", form=form, mode="edit", ep=ep)

@admin_bp.post("/episodios/<int:episode_id>/editar")
@login_required
def episode_edit_post(episode_id: int):
    admin_only()
    ep = Episode.query.get_or_404(episode_id)
    form = EpisodeForm()
    if not form.validate_on_submit():
        flash("Revise os campos.", "error")
        return render_template("admin/episode_form.html", form=form, mode="edit", ep=ep), 400

    season = Season.query.get(form.season_id.data)
    if not season:
        flash("Temporada não encontrada (ID inválido).", "error")
        return render_template("admin/episode_form.html", form=form, mode="edit", ep=ep), 400

    ep.season_id = season.id
    ep.episode_number = form.episode_number.data
    ep.title = form.title.data
    ep.description = form.description.data
    ep.duration_minutes = form.duration_minutes.data
    ep.youtube_url = form.youtube_url.data
    ep.thumbnail_url = form.thumbnail_url.data
    ep.aspect = form.aspect.data
    ep.is_published = bool(form.is_published.data)
    ep.release_at = form.release_at.data
    db.session.commit()
    flash("Episódio atualizado.", "success")
    return redirect(url_for("admin.index"))

@admin_bp.post("/episodios/<int:episode_id>/delete")
@login_required
def episode_delete(episode_id: int):
    admin_only()
    ep = Episode.query.get_or_404(episode_id)
    db.session.delete(ep)
    db.session.commit()
    flash("Episódio removido.", "success")
    return redirect(url_for("admin.index"))

@admin_bp.get("/usuarios")
@login_required
def users():
    admin_only()
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=users)

@admin_bp.post("/usuarios/<int:user_id>/toggle_admin")
@login_required
def toggle_admin(user_id: int):
    admin_only()
    u = User.query.get_or_404(user_id)
    if u.id == current_user.id:
        flash("Você não pode remover seu próprio admin.", "error")
        return redirect(url_for("admin.users"))
    u.is_admin = not u.is_admin
    db.session.commit()
    flash("Permissão atualizada.", "success")
    return redirect(url_for("admin.users"))
