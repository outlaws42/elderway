from flask import Blueprint

bp = Blueprint('qsg', __name__)

from app.qsg import routes
