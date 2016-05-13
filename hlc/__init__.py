import settings

from flask import Flask, jsonify, make_response

app = Flask(__name__)

@app.route("/")
def hello():
	return "In development: Healthy Living Challenge"


@app.route("/api/test", methods=['GET'])
def test_json():
	response = make_response(jsonify({'stuff': [1, 2, 3, 'hedgehog']}))
	response.headers['Access-Control-Allow-Origin'] = "*"
	# return jsonify({"yes": "no"})
	return response

if __name__ == "__main__":
	app.debug = settings.ENABLE_DEBUG
	app.run()

