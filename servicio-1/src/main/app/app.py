from urllib import response
from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server
import json

port = 8001

def simple_app(environ, start_response):
    setup_testing_defaults(environ)

    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]

    start_response(status, headers)
    response = {"mensaje":"test"}

    ret = [ bytes(json.dumps(response), 'utf-8') ]

    return ret

with make_server('', port, simple_app) as httpd:
    print("Serving on port {}...".format(port))
    httpd.serve_forever()