import os
from flask import Flask, request, jsonify
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
  return "Welcome to API"


# @app.route('/gettemplate', methods=['GET'])
# @swag_from('swagger/get_template.yml')
# def get_guests():
#  return "got template"

if __name__ == '__main__':
    app.run()
