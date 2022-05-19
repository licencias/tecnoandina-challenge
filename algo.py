# INFLUX SETTINGS
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
    version = data_json['version']
    time_search = data_json['timeSearch']
    data_influx, status = get_data_influx(version, time_search)
    print(data_influx)
    #cur = mysql.connection.cursor()
    return {"status": status}


def get_data_influx(version, search):
    with InfluxDBClient(url=url, token=token, org=org) as client:
        print("num,val", version, search)
        # if version:
        number = search[0:(len(search) - 1)]
        value = search[len(search)-1]
        print("num,val", number, value)

        query = 'from(bucket: "system") |> range(start: -1h) |> filter(fn: (r) => r["_measurement"] == "test06")'.format(
            number, value)
        print(query)
        tables = client.query_api.query(query, org=org)
        results = []
        if tables:
            for table in tables:
                for record in table.records:
                    # if record.value.get("version") == version:
                    results.append((record.get_value(), record.values.get(
                        "version"), record.get_time(), record.get_start(), record.get_stop()))
            return results, 'OK'
        else:
            return [], query
        # else:
        #     return [], 'No se pudo procesar los párametros'


# if __name__ == '__main__':
#     # run app in debug mode on port 5000
#     app.run(debug=True, port=port)
