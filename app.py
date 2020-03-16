# dependencies
from flask import Flask
from flask_cors import CORS
# import routes
from config.routes import routes
# Create instance Flask
app = Flask(__name__)
# config cors
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000"]}})
# add routes to app
app.register_blueprint(routes)

if __name__ == '__main__':
    app.run(debug=True)
