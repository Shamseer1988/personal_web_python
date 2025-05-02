from flask import Flask, render_template, request, redirect, url_for, session, flash
import datetime, json, http.client
from urllib.parse import urlparse
from flask import Blueprint
import requests

frigate_bp = Blueprint('frigate', __name__, url_prefix='/frigate', template_folder='templates')


def convert_to_epoch(datetime_str):
    dt = datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M")
    return int(dt.timestamp())


@frigate_bp.route("/", methods=["GET", "POST"])
def frigate_export():
    if request.method == "POST":
        # Get form data
        server_url = request.form.get("server")
        camera_name = request.form.get("camera")
        playback = request.form.get("playback")
        source = request.form.get("source")
        name = request.form.get("name")
        image_path = request.form.get("image_path")

        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")

        try:
            start_timestamp = convert_to_epoch(start_time)
            end_timestamp = convert_to_epoch(end_time)

            parsed_url = urlparse(f"https://{server_url}")
            host = parsed_url.netloc or parsed_url.path
            conn = http.client.HTTPSConnection(host)

            payload = json.dumps({
                "playback": playback,
                "source": source,
                "name": name,
                "image_path": image_path
            })

            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }

            api_path = f"/api/export/{camera_name}/start/{start_timestamp}/end/{end_timestamp}"

            conn.request("POST", api_path, payload, headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")

            if res.status >= 200 and res.status < 300:
                flash(f"Export Successful: {name}", "success")
            else:
                flash(f"Export Failed! Server returned status {res.status}: {data}", "danger")

        except Exception as e:
            flash(f"Error: {str(e)}", "danger")
    return redirect(url_for('dashboard'))
