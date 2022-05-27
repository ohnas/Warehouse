import os, sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
)

from flask import Blueprint, request, render_template, send_file
from werkzeug.utils import secure_filename

from forms import make_sample
from config import config

bp = Blueprint("sample", __name__, url_prefix="/sample")


@bp.route("/")
def sample():
    return render_template("sample.html")


@bp.route("/sample/upload/smartstore/", methods=["GET", "POST"])
def upload_smartstore_sample():
    if request.method == "POST":
        if request.files["smartstore_file"]:
            upload_file = request.files["smartstore_file"]
            upload_file_name = secure_filename(upload_file.filename)
            upload_file.save(
                os.path.join(
                    f"{config.BASE_DIR}/uploads/sample/smartstore/", upload_file_name
                )
            )

    return render_template("sample.html")


@bp.route("/sample/upload/todayhome/", methods=["GET", "POST"])
def upload_todayhome_sample():
    if request.method == "POST":
        if request.files["todayhome_file"]:
            print(request.files)
            upload_file = request.files["todayhome_file"]
            upload_file_name = secure_filename(upload_file.filename)
            upload_file.save(
                os.path.join(
                    f"{config.BASE_DIR}/uploads/sample/todayhome/", upload_file_name
                )
            )

    return render_template("sample.html")


@bp.route("/sample/export/smartstore/")
def export_to_smartstore_sample():
    upload_path = f"{config.BASE_DIR}/uploads/sample/smartstore/"
    upload_file_name = os.listdir(upload_path)[0]
    upload_file = os.path.join(upload_path, upload_file_name)

    generated_path = f"{config.BASE_DIR}/generated/smartstore/"
    make_sample(upload_file, generated_path)

    generated_file_name = os.listdir(generated_path)[0]
    generated_file = os.path.join(generated_path, generated_file_name)

    return send_file(
        f"{generated_file}",
        mimetype="application/vnd.ms-excel",
        as_attachment=True,
        attachment_filename=f"{generated_file_name}",
    )
