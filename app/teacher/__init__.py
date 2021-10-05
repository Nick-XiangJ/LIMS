import sys
sys.path.append('.../venv/Lib/site-packages')
from flask import Blueprint

teacher = Blueprint("teacher", __name__)

from . import api