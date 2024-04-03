from flask import Flask, session
from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix='/')

# main function
if __name__ == "__main__":
    app.secret_key = "esof_3675" # secret key for extra session
    app.run(debug=True)