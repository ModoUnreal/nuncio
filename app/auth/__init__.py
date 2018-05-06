from flask import Blueprint

# Any routes using the bp blueprint has the endpoint '/auth/<endpoint-name>'
bp = Blueprint('auth', __name__)

from . import forms, routes
