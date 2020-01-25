from flask import Flask
from urls import screen_share
app = Flask(__name__)
app.register_blueprint(screen_share)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8000", debug=True)