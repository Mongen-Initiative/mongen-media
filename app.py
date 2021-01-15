import os
from art import text2art
from logzero import logger
from io import BytesIO
from flask import Flask, request, jsonify, render_template, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
db = SQLAlchemy(app)

from data import crud


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/api/v1/send_file/", methods=["POST"])
def receive_file():
    logger.info("/receive_file/",)

    file = request.files.get("file")
    file_id = crud.Create.store_media_file(file.filename, file.read())

    data = {"message": "File stored successfully", "file_id": file_id}

    resp = jsonify(data)
    resp.status_code = 200

    return resp


@app.route("/api/v1/get_file/<int:media_id>", methods=["GET"])
def get_file_by_media_id(media_id):
    logger.info("/get_file_by_media_id/%i", media_id)

    file = crud.Read.file_by_media_id(media_id)

    return send_file(BytesIO(file.data), attachment_filename=file.name)


@app.route("/api/v1/delete_media_days_old", methods=["DELETE"])
def delete_media_days_old():
    params = request.get_json()
    days = params.get("days")
    logger.info("### DELETING MEDIA {} DAYS OLD ###".format(days))

    amount = crud.Delete.delete_media_older_than_days(days)

    data = {
        "message": "### {} media elements were deleted ###".format(amount),
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp


@app.errorhandler(404)
def notfound(error):
    data = {"message": "The endpoint requested was not found"}

    resp = jsonify(data)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    print("Mongen Initiative - Media Service")
    print(
        text2art(
            """Mongen Initiative
    Media Service""",
            font="Roman",
        )
    )
    app.run(host=os.getenv("HOST", "0.0.0.0"), port=os.getenv("PORT", 9090))
