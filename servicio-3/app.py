from flask import Flask, jsonify, render_template, request, redirect, url_for
#from flask_mysqldb import MySQL
import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import mysql.connector
import logging

##ESTE SERVICIO AUN NO SE ENCUENTRA MODULARIZADO, ENCAPSULADO NI TESTING.


## Se configuran logs para la app
logging.basicConfig(filename='record.log', 
    level=logging.INFO, 
    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


# INFLUX SETTINGS
token = "my-admin-token"
org = "tecnoandina"
bucket = "system"
url = "http://influx:8086"


# INITIALIZATION
app = Flask(__name__)


## Se inicializa conexion con mysql
## Se asignan las credenciales de dockercompose
## environment:
## - MYSQL_ROOT_PASSWORD=admin
## - MYSQL_DATABASE=tecnoandina
## - MYSQL_USER=admin
## - MYSQL_PASSWORD=admin


def sql_service():
    """METODO REALIZA CONEXION A BD"""

    cnxn = mysql.connector.connect(
        user= 'admin',
        password= 'admin',
        host= 'mysql',
        port= '3306',
        database= 'tecnoandina')

    cursor = cnxn.cursor(dictionary=True)

    try:

        cursor.execute("SHOW DATABASES;")

        cursor.fetchall()

        return cnxn,cursor

    except Exception as e:

        app.logger.info("ERROR: ", e)


## POST challenge/process
## POST challenge/send
## POST challenge/send
## Se hablitan los endpoints
## Se asignan las rutas
## json /challenge/process:
## {
##     "version": number,
##     "timeSearch": string
## }
## json /challenge/send:
## {
##     "version": number,
##     "type": string
## }


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

    return response


@app.errorhandler(404)
def page_not_found(e):

    return 'No se encontró la ruta especificada'


## Implementacionesy casos de uso
##
##
##
##
def update_filter(data_json):

    cnxn,cursor = sql_service()

    cursor = cnxn.cursor(dictionary=True) 

    cursor.execute("select * from alerts")

    data = cursor.fetchall()

    query = """ update tecnoandina.alerts set sended = %s """


    cnxn.commit()

    for registro in data:

        print("1registro",registro)

        #if registro.version == data_json['version']:
        cursor.execute(query, 'True')
    
    cnxn.close()


## Por tiempo no se termino este servicio
def normal_filter(data_json):

    pass

def send_to_db(data_request):
    
    data_influx = get_data_influx(data_request)

    cnxn,cursor = sql_service()

    updated = datetime.datetime.now()

    query = """ insert into tecnoandina.alerts (
        datetime,
        value,
        version,
        type,
        sended,
        created_at,
        updated_at) values (%s,%s,%s,%s,%s,%s,%s) """

    app.logger.info('Info level log')

    for registro in data_influx:

        tipo_1 = check_type_1(registro[0])

        #if data_influx['version'] == registro[0]:

        #Test para poblar tabla

        value = (str(updated), registro[0], registro[1], tipo_1, 'false', str(updated), str(updated))

        cursor.execute(query, value)

        cnxn.commit()

    cnxn.close()

    return {"mensaje": str(data_influx)}


def get_data_influx(data_request):

    with InfluxDBClient(url=url, token=token, org=org) as client:

        aux = data_request['timeSearch']

        number = aux[0:len(aux)-1]

        time = aux[len(aux)-1]

        if len(number) > 0 or len(number) < 3: 

            print("number",number) 

            query = 'from(bucket: "system") |> range(start: -{}{})'.format(number,time)

            print("query",query)

            tables = client.query_api().query(query, org=org)

            results = []

            for table in tables:

                for record in table.records:

                    results.append((record.get_value(), record.values.get(
                        "version"), record.get_time(), record.get_start(), record.get_stop()))
        else:

            return 'ERROR: No se pudo procesar los párametros'

        return results


## Metodos Utils
##


def check_type_1(valor):

    aux = 'BAJA'

    if valor > 200:
        aux = 'BAJA'
        if valor > 500:
            aux = 'MEDIA'
            if valor > 800:
                aux = 'ALTA'
    
    return aux