from flask import Blueprint

bp = Blueprint('resource', __name__, url_prefix='/resource')

from app.resource import views, forms