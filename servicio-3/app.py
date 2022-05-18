from flask import Flask, jsonify, render_template, request, redirect, url_for
#from flask_mysqldb import MySQL
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#INFLUX SETTINGS
token = "my-admin-token"
org = "tecnoandina"
bucket = "system"
url = "http://influx:8086"

# INITIALIZATION
app = Flask(__name__)

# MYSQL APP INITIALIZATION
# app.config['MYSQL_HOST'] = 'mysql:3306'
# app.config['MYSQL_USER'] = 'admin'
# app.config['MYSQL_PASSWORD'] = 'admin'
# app.config['MYSQL_DB'] = 'tecnoandina'
# mysql = MySQL(app)

# SETTINGS
#app.secret_key = "mysecretkey"

@app.route('/')
def view_dashboard():
    return 'conectado al fin!'

@app.route("/challenge/process", methods=['POST'])
def challenge_process():

    response = send_to_db(request.json)

    return response


@app.route('/challenge/search')
def form_example():
    return 'challenge/search'


@app.route('/challenge/send')
def json_example():
    return 'challenge/send'


@app.errorhandler(404)
def page_not_found(e):
    return 'No se encontró la ruta especificada'

# backend


def send_to_db(data_json):
    data_influx = get_data_influx()
    print(data_influx)
    #cur = mysql.connection.cursor()
    version = data_json['version']
    timeSearch = data_json['timeSearch']
    return {"mensaje": "test"}

def get_data_influx():
    with InfluxDBClient(url=url, token=token, org=org) as client:
        query = f'SELECT * FROM test06'
        response = client.query(query)

# if __name__ == '__main__':
#     # run app in debug mode on port 5000
#     app.run(debug=True, port=port)
