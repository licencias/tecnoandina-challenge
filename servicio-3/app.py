from flask import Flask, jsonify, render_template, request, redirect, url_for
#from flask_mysqldb import MySQL
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import mysql.connector

# INFLUX SETTINGS
token = "my-admin-token"
org = "tecnoandina"
bucket = "system"
url = "http://influx:8086"

# INITIALIZATION
app = Flask(__name__)

config = {
    'user': 'admin',
    'password': 'admin',
    'host': 'mysql',
    'port': '3306',
    'database': 'challenge'
}


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
def challenge_search():

    response = normal_filter(request.json)

    return response


@app.route('/challenge/send')
def challenge_send():

    response = update_filter(request.json)

    return 'challenge/send'


@app.errorhandler(404)
def page_not_found(e):
    return 'No se encontró la ruta especificada'

# backend
def update_filter(data_json):
    connection = mysql.connector.connect(
        user= 'admin',
        password= 'admin',
        host= 'mysql',
        port= '3306',
        database= 'tecnoandina')

    cursor = connection.cursor(dictionary=True)

    data = cursor.execute("select * from tecnoandina")
    connection.commit()
    for registro in data:
        print("1registro",registro)
        #if registro.version == data_json['version']:
        #insertar registro

def normal_filter(data_json):
    pass

def send_to_db(data_json):
    connection = mysql.connector.connect(
        user= 'admin',
        password= 'admin',
        host= 'mysql',
        port= '3306',
        database= 'tecnoandina')
    cursor = connection.cursor(dictionary=True)

    data_influx = get_data_influx()
    print("tengo data", data_influx)

    for registro in data_influx:
        print("1registro",registro)
        #if registro.version == data_json['version']:
        #insertar registro
    

    #connection.close()

    return {"mensaje": str(data_influx)}


def get_data_influx():
    with InfluxDBClient(url=url, token=token, org=org) as client:
        query = 'from(bucket: "system") |> range(start: -1h)'
        tables = client.query_api().query(query, org=org)
        results = []
        for table in tables:
            for record in table.records:
                results.append((record.get_value(), record.values.get(
                    "version"), record.get_time(), record.get_start(), record.get_stop()))
        return results
