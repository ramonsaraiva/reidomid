import json

from flask import Flask
from flask import send_from_directory
from flask import request
from flask import jsonify

from flask.ext.restful import Api

from models import db
from models import Summoner

from resources import authenticate

from resources import Summoners
from resources import SummonersVerification

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update({
	'SECRET_KEY': 'x1x1x1',
	'SQLALCHEMY_DATABASE_URI': 'postgresql://rdm:rdm@localhost/rdm'
})

db.init_app(app)
api = Api(app)

api.add_resource(Summoners, '/api/summoners/', '/api/summoners/<int:id>/')
api.add_resource(SummonersVerification, '/api/summoners/<int:id>/verification/')

@app.route('/auth/', methods=['POST'])
def auth():
	data = json.loads(request.data)
	if 'login' and 'password' in data:
		if Summoner.authenticate(data['login'], data['password']):
			return jsonify(data)
	return authenticate()

@app.route('/')
def send_template():
	return send_from_directory('templates', 'base.html')

@app.route('/<path:path>')
def send_static(path):
	return send_from_directory('static', path)

@app.cli.command()
def drop():
	db.drop_all()

@app.cli.command()
def create():
	db.create_all()
