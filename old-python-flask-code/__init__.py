import datetime
import settings

from api import get_user_data as data_handler
from flask import Flask, jsonify, make_response, render_template
from lib import utils

app = Flask(__name__)

@app.route("/")
def hello():
	display_data = utils.build_display_data()

	for i, score_pair in enumerate(display_data[1]):
		display_data[1][i][1]['scores_by_date'].sort(key=\
			lambda x: datetime.datetime.strptime(x[0], '%m/%d/%Y'))

	return render_template('index.html',
						   year=display_data[0],
						   scores=display_data[1])


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
