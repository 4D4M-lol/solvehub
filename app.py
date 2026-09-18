from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return "Hello, SolveHub!"

@app.route("/create-user/<username>")
def create_user(username):
    user = User(username=username)

    db.session.add(user)
    db.session.commit()

    return f"Created user: {username}"

if __name__ == "__main__":
    app.run(debug=True)