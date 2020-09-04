# import files
from flask import Flask, render_template, request, session, url_for, redirect
import requests
import os
import json
import logging

from services.user_service import UserService

app = Flask(__name__)
LEX_PROXY_URL = os.getenv("LEX_PROXY_URL", "")


@app.route("/")
def home():
    if "session_token" in session:
        return render_template("index.html")
    print("Going to Login")
    return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    req = request.form
    username = req.get("uname")
    password = req.get("psw")

    user_svc = UserService()
    try:
        login_info = user_svc.login(username, password)
        
        id_token = login_info.get("IdToken")
        lex_token = id_token[:80]
        # Creating Lex user session to talk to bot using the same ID token of Cognito
        payload = {"user_id": lex_token}
        payload_json = json.dumps(payload)
        headers = { 'Content-Type': 'application/json' }
        response = requests.request("POST", f"{LEX_PROXY_URL}/create_session", headers=headers, data = payload_json)
        response_json = response.json()
        print(f"INFO {response_json}")
        session["session_token"] = id_token
        session["lex_token"] = lex_token
        return redirect(url_for('home'))
    except Exception as e:
        logging.warning(e)
        return redirect(url_for('login'))


@app.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    if request.method == 'GET':
        return render_template("sign_in.html")
    
    req = request.form
    user_svc = UserService()

    username = req.get("uname")
    password = req.get("psw")
    email = req.get("email")
    try:
        user_svc.create_user(username, password, email)
        return redirect(url_for('login'))
    except Exception as e:
        print(e)
        return redirect(url_for('sign_in'))


@app.route("/get")
def get_bot_response():
    user_text = request.args.get('msg')
    user_id = session["lex_token"]
    payload = {"user_id": user_id, "text": user_text}
    payload_json = json.dumps(payload)
    headers = { 'Content-Type': 'application/json' }

    response = requests.request("POST", f"{LEX_PROXY_URL}/send_message", headers=headers, data = payload_json)
    response_json = response.json()

    return str(response_json.get("output")) 

if __name__ == "__main__": 
    app.secret_key = os.urandom(24)
    app.run(debug=True, host='0.0.0.0')