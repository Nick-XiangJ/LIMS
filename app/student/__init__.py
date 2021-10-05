import sys
sys.path.append('.../venv/Lib/site-packages')
from flask import Blueprint

student = Blueprint("student", __name__)
from . import api