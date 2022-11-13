from flask import Flask
from blueprint import *

app = Flask(__name__)

app.register_blueprint(api_blueprint)

if __name__ == '__main__':
    app.run(port=5000, debug=True)




