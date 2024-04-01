from flask import Flask
from homepage import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix='/')

if __name__ == "__main__":
    app.run(debug=True)