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


@app.route('/kunder/<int:cpr>', methods=['GET'])
@swag_from('swagger/get_kunde.yml')
def get_kunde(cpr):
    # Check for cpr legitimacy
    if len(str(cpr)) != 10:
        response = make_response({'message': 'CPR skal være 10 cifre'}, 400)
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

    cpr = data.get('cpr')
    navn = data.get('navn')
    tlf = data.get('tlf')
    email = data.get('email')
    adresse = data.get('adresse')

    if cpr is None or navn is None or tlf is None or email is None or adresse is None:
        response = make_response({'message': 'Alle felter skal udfyldes'}, 400)
        return response

    # Check for duplicates
    kunde = db_service.get_kunde(cpr)
    if kunde is not None:
        response = make_response({'message': 'Kunde eksisterer allerede'}, 400)
        return response

    # Check for cpr legitimacy
    if not re.match(r'^(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])\d{2}[-]?\d{4}$', str(cpr)):
        response = make_response({'message': 'CPR Invalid'}, 400)
        return response

    # Check for tlf legitimacy
    if len(tlf) != 8:
        response = make_response({'message': 'Telefonnummer Invalid'}, 400)
        return response

    # Check for email legitimacy
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        response = make_response({'message': 'Email Invalid'}, 400)
        return response

    ny_kunde = db_service.create_kunde(cpr, navn, tlf, email, adresse)

    response = make_response(jsonify(ny_kunde), 201)

    return response

if __name__ == '__main__':
    app.run(port=5002)
