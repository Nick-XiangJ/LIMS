import sys
sys.path.append('.../venv/Lib/site-packages')
from flask import Blueprint

main = Blueprint("main", __name__)

from . import api