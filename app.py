from flask import Flask

from detection import detection

app = Flask(__name__)
app.register_blueprint(detection, url_prefix='/api')



if __name__ == '__main__':
    app.run()
