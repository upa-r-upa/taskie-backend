from flask import Flask, request
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
