from flask import Flask, jsonify
from club_deportivo_encuentro.constants import BASE_URL

app = Flask(__name__)

app.register_blueprint(socios_bp, url_prefix=BASE_URL)
app.register_blueprint(deportes_bp, url_prefix=BASE_URL)
app.register_blueprint(canchas_bp, url_prefix=BASE_URL)
app.register_blueprint(reservas_bp, url_prefix=BASE_URL)

@app.route("/")
def ping():
    return jsonify({"mensaje": "API del Club Deportivo en línea"}), 200

app.run(host="0.0.0.0", port=8080, debug=True)
