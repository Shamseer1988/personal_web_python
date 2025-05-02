from flask import render_template, request, jsonify, session, redirect, url_for
from flask import Blueprint
import requests

lights_bp = Blueprint('lights', __name__, url_prefix='/lights', template_folder='templates')

# Home Assistant API details
HA_URL = 'http://192.168.150.30:8123/api'
HA_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiIyOTQzYzIyNWI2MjU0YjNmOTNiOTE1ODI0ZTZiMmZiMCIsImlhdCI6MTc0NjEwNTgyNCwiZXhwIjoyMDYxNDY1ODI0fQ.NoIprJOJcAh0hCpiabWF4pBF1Bh2NLuqLmIiAYRp9Lw'

# Home Assistant API Headers
headers = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json"
}


# Route to the home page
@lights_bp.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    lights = get_light_entities()
    return render_template('lights.html', lights=lights)


# Route to toggle lights
@lights_bp.route('/toggle_light', methods=['POST'])
def toggle_light():
    entity_id = request.json['entity_id']
    response = requests.post(
        f"{HA_URL}/services/light/toggle",
        headers=headers,
        json={"entity_id": entity_id}
    )
    if response.status_code in [200, 201]:
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failed'}), 400


def get_light_entities():
    response = requests.get(f"{HA_URL}/states", headers=headers)
    lights = []
    if response.status_code == 200:
        for entity in response.json():
            if entity["entity_id"].startswith("light."):
                lights.append({
                    "entity_id": entity["entity_id"],
                    "friendly_name": entity["attributes"].get("friendly_name", entity["entity_id"]),
                    "state": entity["state"]
                })
    return lights
