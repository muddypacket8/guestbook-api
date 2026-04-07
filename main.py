from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_NAME = "em.db"


# ---------------------------
# DATABASE SETUP
# ---------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------------------
# HELPERS
# ---------------------------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------
# API ROUTES
# ---------------------------

# GET all wishes
@app.route('/wishes', methods=['GET'])
def get_wishes():
    conn = get_db_connection()
    wishes = conn.execute(
        "SELECT * FROM wishes ORDER BY id DESC"
    ).fetchall()
    conn.close()

    return jsonify([dict(row) for row in wishes])


# POST a new wish
@app.route('/wishes', methods=['POST'])
def add_wish():
    data = request.get_json()

    name = data.get('name')
    message = data.get('message')

    if not name or not message:
        return jsonify({"error": "Name and message required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO wishes (name, message, created_at)
        VALUES (?, ?, ?)
    """, (name, message, datetime.utcnow().isoformat()))

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "id": new_id,
        "name": name,
        "message": message
    })


# ---------------------------
# RUN SERVER
# ---------------------------
app = Flask(__name__)
CORS(app)