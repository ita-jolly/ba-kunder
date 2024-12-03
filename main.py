import os
import re
from flask import Flask, request, jsonify, make_response
import db_service
from flasgger import Swagger, swag_from
from dotenv import load_dotenv
from swagger.config import swagger_config

load_dotenv()

app = Flask(__name__)
swagger = Swagger(app, config=swagger_config)

db_service.init()


@app.route('/')
def index():
    return "Welcome to Kunder API"

@app.route('/kunder', methods=['GET'])
@swag_from('swagger/get_kunder.yml')
def get_kunder():
    kunder = db_service.get_kunder()

    if kunder is None:
        response = make_response({'message': 'Ingen kunder fundet'}, 404)
    else:
        response = make_response(kunder, 200)

    return response


@app.route('/kunder/<string:cpr>', methods=['GET'])
@swag_from('swagger/get_kunde.yml')
def get_kunde(cpr):
    # Check for cpr legitimacy
    if not re.match(r'^(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[0-2])\d{2}[-]?\d{4}$', str(cpr)):
        response = make_response({'message': 'CPR Invalid'}, 400)
        return response

    kunde = db_service.get_kunde(cpr)

    if kunde is None:
        response = make_response({'message': 'Kunde ikke fundet'}, 404)
    else:
        response = make_response(kunde, 200)

    return response


@app.route('/kunder', methods=['POST'])
@swag_from('swagger/create_kunde.yml')
def create_kunde():

    data = request.get_json()
    required_fields = ['cpr', 'navn', 'tlf', 'email', 'adresse']

    if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

    # Check if kunde already exists
    cpr = str(data['cpr'])
    kunder = db_service.get_kunder()
    if kunder is None:
        return jsonify({"error": "Could not communicate with the kunder database"}), 500

    matching_kunde = next((kunde for kunde in kunder if str(kunde['cpr']) == cpr), None)
    if matching_kunde:
        return jsonify({"error": f"Cpr {cpr} already exists in kunder database"}), 400

    # Check for cpr legitimacy
    if not re.match(r'^(0[1-9]|[12][0-9]|3[01])(0[1-9]|1[0-2])\d{2}[-]?\d{4}$', str(cpr)):
        response = make_response({'message': 'CPR Invalid'}, 400)
        return response

    # Check for tlf legitimacy
    tlf = str(data['tlf'])
    if len(tlf) != 8:
        response = make_response({'message': 'Telefonnummer Invalid'}, 400)
        return response

    # Check for email legitimacy
    email = data['email']
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        response = make_response({'message': 'Email Invalid'}, 400)
        return response

    ny_kunde = db_service.create_kunde(
        cpr=data['cpr'],
        navn=data['navn'],
        tlf=data['tlf'],
        email=data['email'],
        adresse=data['adresse']
    )

    response = make_response(jsonify(ny_kunde), 201)

    return response

if __name__ == '__main__':
    app.run(port=5002)
