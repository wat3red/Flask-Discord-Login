import os
import string
from datetime import timedelta
from os import _exit

from flask import Flask, flash
from flask_discord import DiscordOAuth2Session
from flask_session import Session
from settings import Settings
from redis import Redis

SECRET_KEY_LENGTH = 32

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "false"

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(SECRET_KEY_LENGTH)
app.config["SESSION_TYPE"] = "filesystem"
#app.config["SESSION_REDIS"] = Redis(host="localhost", port=6379)
app.config["SESSION_PERMANENT"] = True
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///info.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Session(app)

settings = Settings()
app.config["DISCORD_CLIENT_ID"] = settings.DISCORD_CLIENT_ID
app.config["DISCORD_CLIENT_SECRET"] = settings.DISCORD_CLIENT_SECRET
app.config["DISCORD_REDIRECT_URI"] = settings.DISCORD_REDIRECT_URI


def create_app():
    return app


def setup_discord(app):
    try:
        discord = DiscordOAuth2Session(app)
        return discord
    except Exception as e:
        flash("Something went wrong with OAuth2Session: " + str(e), "error")
        _exit(1)
