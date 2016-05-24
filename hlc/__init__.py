import datetime
import settings

from api import get_user_data as data_handler
from flask import Flask, jsonify, make_response, render_template
from lib import utils

app = Flask(__name__)

@app.route("/")
def hello():
	scores = utils.assemble_score_dict()
	scores_arr = [person for person in scores['scores'].iteritems()]
	for person in scores_arr:
		person[1]['ordinal'] = \
			utils.ordinal(person[1]['ranking'])
	scores_arr.sort(key=lambda x: x[1]['ranking'])
	year = datetime.datetime.now().year
	return render_template('index.html', year=year, scores=scores_arr)


@app.route("/api/data", methods=['GET'])
def deliver_user_data():
	start_time = datetime.datetime.now()
	response = make_response(data_handler.get_user_data())
	delta = datetime.datetime.now() - start_time
	print 'Score building took: {}'.format(delta)
	response.headers['Access-Control-Allow-Origin'] = "*"
	return response


@app.route("/api/test", methods=['GET'])
def test_json():
	response = make_response(jsonify({'stuff': [1, 2, 3, 'hedgehog']}))
	response.headers['Access-Control-Allow-Origin'] = "*"
	# return jsonify({"yes": "no"})
	return response


if __name__ == "__main__":
	app.debug = settings.ENABLE_DEBUG
	app.run()
