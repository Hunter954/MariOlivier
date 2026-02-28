from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    IntegerField,
    TextAreaField,
    SelectField,
    DateTimeField,
)
from wtforms.validators import DataRequired, Email, Length, Optional, URL, EqualTo

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=128)])
    remember = BooleanField("Manter conectado")


class RegisterForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=255)])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=6, max=128)])
    confirm_password = PasswordField(
        "Confirmar senha",
        validators=[
            DataRequired(),
            EqualTo("password", message="As senhas não conferem."),
            Length(min=6, max=128),
        ],
    )


class SeasonForm(FlaskForm):
    number = IntegerField("Número da temporada", validators=[DataRequired()])
    title = StringField("Título", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Descrição", validators=[Optional()])
    thumbnail_url = StringField("Thumbnail (URL)", validators=[Optional(), Length(max=2000)])
    is_published = BooleanField("Publicada?")


class EpisodeForm(FlaskForm):
    season_id = IntegerField("ID da Temporada", validators=[DataRequired()])
    episode_number = IntegerField("Número do episódio", validators=[DataRequired()])
    title = StringField("Título", validators=[DataRequired(), Length(max=200)])
    description = TextAreaField("Descrição", validators=[Optional()])
    duration_minutes = IntegerField("Duração (min)", validators=[Optional()])
    youtube_url = StringField("Link do YouTube (unlisted)", validators=[DataRequired(), Length(max=2000)])
    thumbnail_url = StringField("Thumbnail (URL)", validators=[Optional(), Length(max=2000)])
    aspect = SelectField(
        "Formato",
        choices=[("vertical", "Stories/Reels (9:16)"), ("horizontal", "Horizontal (16:9)")],
        validators=[DataRequired()],
    )
    is_published = BooleanField("Publicado?")
    release_at = DateTimeField(
        "Data/Hora de liberação (opcional)", validators=[Optional()], format="%Y-%m-%d %H:%M"
    )
