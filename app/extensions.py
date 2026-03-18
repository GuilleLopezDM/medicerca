"""Extensiones compartidas de Flask para MediCerca."""

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

bd = SQLAlchemy()
gestor_login = LoginManager()
