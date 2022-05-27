import os, sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
)

from flask import Blueprint, request, render_template, send_file
from werkzeug.utils import secure_filename

from forms import make_waybill
from config import config

bp = Blueprint("waybill", __name__, url_prefix="/waybill")


@bp.route("/")
def waybill():
    return render_template("waybill.html")


@bp.route("/waybill/upload/", methods=["GET", "POST"])
def upload_waybill():
    if request.method == "POST":
        upload_file = request.files["waybill_file"]
        upload_file_name = secure_filename(upload_file.filename)
        upload_file.save(
            os.path.join(f"{config.BASE_DIR}/uploads/waybill/", upload_file_name)
        )
    return render_template("waybill.html")


@bp.route("/waybill/export/")
def export_to_waybill():
    path1 = f"{config.BASE_DIR}/uploads/waybill/"
    file_name1 = os.listdir(path1)[0]
    file1 = os.path.join(path1, file_name1)

    path2 = f"{config.BASE_DIR}/uploads/sample/"
    file_name2 = os.listdir(path2)[0]
    file2 = os.path.join(path2, file_name2)
    make_waybill(file1, file2)
    return send_file(
        f"{file2}",
        mimetype="application/vnd.ms-excel",
        as_attachment=True,
        attachment_filename=f"{file2}",
    )
