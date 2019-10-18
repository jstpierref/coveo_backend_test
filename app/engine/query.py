import app.engine.utils as utils

class Query:
	def __init__(self, request_args):
		self.q = utils.standardize(request_args.get('q'))
		self.lat = request_args.get('latitude')
		self.lon = request_args.get('longitude')
