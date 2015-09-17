from flask import Flask
from flask import current_app

from flask.ext.sqlalchemy import SQLAlchemy

from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Summoner(db.Model):
	id = db.Column(db.Integer, primary_key=True)

	email = db.Column(db.String(256), unique=True)
	password = db.Column(db.String(160))
	verified = db.Column(db.Boolean(), default=False)

	rid = db.Column(db.Integer)
	name = db.Column(db.Unicode(32))
	level = db.Column(db.Integer)
	tier = db.Column(db.String(32))
	division = db.Column(db.String(3))
	lp = db.Column(db.Integer)
	validated = db.Column(db.Boolean(), default=False)

	games = db.Column(db.Integer)
	wins = db.Column(db.Integer)
	points = db.Column(db.Integer)

	def __init__(self, data):
		self.email = data['email']
		self.set_password(data['password'])
		self.rid = data['id']
		self.name = data['name']
		self.level = data['summonerLevel']

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password, password)

	@staticmethod
	def authenticate(email, password):
		first = Summoner.query.get(1)
		summoner = Summoner.query.filter(Summoner.email == email).first()
		if not summoner:
			return False
		return summoner.check_password(password)

	def update_league(self, data):
		solo = data[str(self.rid)][0]
		entry = solo['entries'][0]

		self.tier = solo['tier']
		self.division = entry['division']
		self.lp = entry['leaguePoints']

	@property
	def serialize(self):
		return {
			'id': self.id,
			'rid': self.rid,
			'name': self.name,
			'level': self.level,
			'tier': self.tier,
			'division': self.division,
			'lp': self.lp,
			'validated': self.validated
		}
