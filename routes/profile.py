import os

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from werkzeug.utils import secure_filename

from extensions import db
from models.user import User

profile = Blueprint("profile", __name__)

UPLOAD_FOLDER = "static/uploads/avatars"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@profile.route("/profile")
def view_profile():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    user = db.session.get(User, session["user_id"])

    return render_template("profile.html", user=user)

@profile.route("/profile/upload", methods=["POST"])
def upload_picture():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    file = request.files.get("profile_picture")

    if not file or file.filename == "":
        return "No file selected."

    if not allowed_file(file.filename):
        return "Invalid file type."

    user = db.session.get(User, session["user_id"])

    extension = secure_filename(file.filename).rsplit(".", 1)[1].lower()

    filename = f"user_{user.id}.{extension}"

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    file.save(os.path.join(UPLOAD_FOLDER, filename))

    user.profile_picture = filename

    db.session.commit()

    return redirect(url_for("profile.view_profile"))