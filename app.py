from flask_restx import Api


from . import create_app

app = create_app()
api = Api(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
