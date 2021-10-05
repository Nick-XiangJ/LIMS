import sys
sys.path.append('.../venv/Lib/site-packages')
from flask import Blueprint

admin = Blueprint("admin", __name__)

from . import api