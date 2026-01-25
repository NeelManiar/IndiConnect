from flask import Blueprint

bp = Blueprint('feedback', __name__, url_prefix='/feedback')

from app.feedback import views, forms