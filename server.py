from flask import Flask
from wsgiref.simple_server import make_server

app = Flask(__name__)
STUDENT_ID = 14


@app.route(f'/api/v1/hello-world-{STUDENT_ID}')
def hello_world():
    return f'Hello, World! - {STUDENT_ID}'


with make_server('', 5000, app) as server:
    print(f'http://localhost:5000/api/v1/hello-world-{STUDENT_ID}')
    server.serve_forever()
