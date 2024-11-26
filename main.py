import os
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


# @app.route('/gettemplate', methods=['GET'])
# @swag_from('swagger/get_template.yml')
# def get_guests():
#  return "got template"

if __name__ == '__main__':
    app.run()
