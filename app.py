import os

from flask import Flask, session
from dotenv import load_dotenv

from extensions import db
from routes.main import main
from routes.auth import auth
from routes.profile import profile

load_dotenv()

app: Flask = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(profile)

with app.app_context():
    db.create_all()

@app.cli.command("reset-db")
def reset_db():
    db.drop_all()
    db.create_all()

    print("Database reset.")

if __name__ == "__main__":
    app.run(debug=True)