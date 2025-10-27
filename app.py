from flask import Flask,render_template,session,redirect,url_for,request,flash,jsonify
from werkzeug.security import generate_password_hash, check_password_hash

import sqlite3
import pickle
import numpy as np
import pytz
from datetime import datetime

DB_PATH = "database.db"

def create_db(path="database.db"):
    conn = sqlite3.connect(path)
    c = conn.cursor()
    # users table
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    ''')
    # predictions history
    c.execute('''
    CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        area FLOAT,      
        bedrooms INTEGER,
        bathrooms INTEGER,
        stories INTEGER,
        parking INTEGER,
        mainroad TEXT,
        guestroom TEXT,
        hotwaterheating TEXT,
        airconditioning TEXT,
        furnishingstatus TEXT,
        predicted_price REAL,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    ''')
    # add default user: username: admin , password: password123
    try:
        pw_hash = generate_password_hash("password123")
        c.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("admin", pw_hash))
    except Exception as e:
        # user exists
        pass
    conn.commit()
    conn.close()
    print(f"Created database (or ensured exists) at {path}. Default user: admin / password123")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
app.secret_key = "replace_this_with_a_random_secret_key" 

def prediction(list):
    filename ='model/predictor.pickle'
    with open(filename, 'rb') as file:
        model = pickle.load(file)
    pred_value = model.predict([list])
    return pred_value

@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            flash("Login successful", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    # fetch user's prediction history (latest 10)
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM predictions WHERE user_id = ? ORDER BY created_at DESC LIMIT 10", (session["user_id"],)).fetchall()
    conn.close()
    history = [dict(r) for r in rows]
    return render_template("dashboard.html", username=session.get("username"), history=history)
@app.route("/predict")
def predict_page():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    return render_template("predict.html")

@app.route("/predict", methods=["POST","GET"])
def api_predict():
    pred = 0
    slt_timezone = pytz.timezone("Asia/Colombo")
    created_at = datetime.now(slt_timezone).strftime("%Y-%m-%d %H:%M:%S")
    if not session.get("user_id"):
        return jsonify({"error": "Unauthorized"}), 401
    
    if request.method == 'POST':
        area = request.form['area']
        bedrooms = request.form['bedrooms']
        bathrooms = request.form['bathrooms']
        stories = request.form['stories']
        parking = request.form['parking']
        mainroad = request.form['mainroad']
        guestroom = request.form['guestroom']
        hotwaterheating = request.form['hotwaterheating']
        airconditioning = request.form['airconditioning']
        furnishingstatus = request.form['furnishingstatus']

   

        feature_list = []

        feature_list.append(int(area))
        feature_list.append(int(bedrooms))
        feature_list.append(int(bathrooms))
        feature_list.append(int(stories))
        feature_list.append(int(parking))
    
        mainfoad_list = ['yes','no']
        guestroom_list = ['yes','no']
        hotwaterheating_list = ['yes','no']
        airconditioning_list = ['yes','no']
        furnishingstatus_list = ['furnished','semi-furnished','unfurnished']
    
        def traverse_list(lst, value):
            for item in lst:
                if item == value:
                    feature_list.append(1)
                else:
                    feature_list.append(0)
        traverse_list(mainfoad_list, mainroad)
        traverse_list(guestroom_list, guestroom)
        traverse_list(hotwaterheating_list, hotwaterheating)
        traverse_list(airconditioning_list, airconditioning)
        traverse_list(furnishingstatus_list, furnishingstatus)

        pred = prediction(feature_list)
        pred = np.round(pred[0], 2)

        # save in DB
        conn = get_db_connection()
        conn.execute(
            "INSERT INTO predictions (user_id, area, bedrooms, bathrooms, stories, parking, mainroad, guestroom, hotwaterheating, airconditioning, furnishingstatus,predicted_price,created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (session["user_id"], area, bedrooms, bathrooms, stories, parking, mainroad, guestroom, hotwaterheating, airconditioning, furnishingstatus,pred,created_at)
                )
        conn.commit()
        conn.close()
    
    return render_template("predict.html", pred=pred)
    ##return jsonify({"predicted_price": pred})

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Provide username and password", "danger")
            return redirect(url_for("register"))
        pw_hash = generate_password_hash(password)
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, pw_hash))
            conn.commit()
            flash("User created. Please login.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash("Username already exists", "danger")
            return redirect(url_for("register"))
        finally:
            conn.close()
    return render_template("login.html", show_register=True)

# Simple register route (optional)

if __name__ == '__main__':
    create_db()
    
    app.run(debug=True)