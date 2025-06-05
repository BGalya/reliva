from flask import Flask, jsonify, request, make_response
from generate_response import GenerateResponse
from main import GeminiObject

app = Flask(__name__)
import json

# @app.route('/', methods=['GET'])
# def home():
#     return 'ברוך הבא לשרת Flask 🎉'

gemini_object = ""


@app.route('/init', methods=['POST', 'OPTIONS'])
def chat_screen():
    reply = gemini_object.init_chat()
    response = make_response(jsonify({"message": reply}))
    add_headers(response)
    return response

@app.route('/message', methods=['POST', 'OPTIONS'])
def get_response():
    if request.method == 'OPTIONS':
        response = make_response()
    else:
        data = request.get_json()
        user_message = data.get('message', '')
        print(f"User said: {user_message}")

        reply = gemini_object.response(user_message)

        response = make_response(jsonify({"message": reply}))

    add_headers(response)
    return response

@app.route('/exit', methods=['POST', 'OPTIONS'])
def exit():
    gemini_object.end_chat()
    return None

def add_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, FETCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response


if __name__ == '__main__':
    gemini_object = GeminiObject()
    app.run(host='0.0.0.0', port=5000)
