import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.main_routes import register_routes

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    register_routes(app)
    return app


app = create_app()

if __name__ == "__main__":
    host = os.getenv("SERVER_HOST", "127.0.0.1")
    port = int(os.getenv("SERVER_PORT", 5000))
    app.run(debug=True, host=host, port=port)


