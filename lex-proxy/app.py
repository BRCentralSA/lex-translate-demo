from flask import Flask, render_template, jsonify, \
    request, Response, redirect, url_for, session

from services.aws_services import *


# Flask configurations
app = Flask(__name__)


@app.route('/send_message/', methods=['POST'])
@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_id = data["user_id"]
    text = data["text"]

    lex_client = lex_aws_connection()
    translate_client = translate_aws_connection()

    text_to_post = translate_text(translate_client, text, "pt", "en")
    response_back = post_text_to_bot(lex_client, user_id, text_to_post)
    translated_response = translate_text(translate_client, response_back, "en", "pt")
    response = {"input": text, "output": translated_response}

    return jsonify(response)


@app.route('/create_session', methods=['POST'])
def start_new_session():
    data = request.get_json()
    user_id = data["user_id"]
    lex_client = lex_aws_connection()

    create_session(lex_client, user_id)
    response = {"session": user_id}
    return jsonify(response)


@app.route('/health/', methods=['GET'])
def health():
    response = {"Health": "OK"}
    return jsonify(response)


app.run(debug=True, host='0.0.0.0')