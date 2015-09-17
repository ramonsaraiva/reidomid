from functools import wraps

from flask import request
from flask import Response
from flask import jsonify

from flask.ext.restful import Resource
from flask.ext.restful import reqparse

from models import db
from models import Summoner

from riotwatcher import RiotWatcher
from riotwatcher import BRAZIL

def watcher():
	return RiotWatcher('1201f800-aced-4abb-9083-714dcf58a36e', default_region=BRAZIL)

def authenticate():
	return Response(
	'Could not verify your access level for that URL.\n'
	'You have to login with proper credentials', 401,
	{'WWW-Authenticate': 'xBasic realm="Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or not Summoner.authenticate(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated

class Summoners(Resource):
	def __init__(self):
		self.reqparse = reqparse.RequestParser()
		self.reqparse.add_argument('name', type=str, location='json', required=True)
		self.reqparse.add_argument('email', type=str, location='json', required=True)
		self.reqparse.add_argument('password', type=str, location='json', required=True)

	def get(self, id=None):
		if id:
			return jsonify(Summoner.query.get_or_404(id).serialize)
		return jsonify(summoners=[s.serialize for s in Summoner.query.all()])

	def post(self):
		data = self.reqparse.parse_args()

		w = watcher()
		riot_summoner = w.get_summoner(name=data['name'])
		if not riot_summoner:
			return jsonify(error='error') # not implemented

		data.update(riot_summoner)
		summoner = Summoner(data)
		db.session.add(summoner)
		db.session.commit()
		return jsonify(summoner.serialize)

class SummonersVerification(Resource):
	decorators = [requires_auth]

	def post(self, id):
		summoner = Summoner.query.filter(
				Summoner.id == id,
				Summoner.email == request.authorization.username).first()

		if not summoner:
			return 'Summoner not found', 404

		w = watcher()
		runepages = w.get_rune_pages([summoner.rid])
		first_runepage_name = runepages[str(summoner.rid)]['pages'][0]['name']

		if first_runepage_name != 'reidomid':
			return jsonify(error='error') # not implemented

		league = w.get_league_entry([summoner.rid])
		summoner.update_league(league)
		summoner.validated = True
		db.session.commit()

		return jsonify(summoner.serialize)
