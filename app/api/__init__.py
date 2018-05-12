from flask import Flask, Blueprint
from flask_restplus import Api, Resource, fields

api_bp = Blueprint('api', __name__)

api = Api(api_bp, version='1.0', title='Nuncio Api', description='The Nuncio api.')
