from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

from config.flask_mail import MAIL_PASSWORD, MAIL_PORT, MAIL_SERVER, MAIL_USE_SSL, MAIL_USE_TLS, MAIL_USERNAME

from routes.user_routes import user_bp
from routes.story_routes import story_bp
from routes.message_routes import message_bp
from routes.tags_routes import tags_bp

from config.database import db, database_url
from config.cloudinary import cloudinary
from config.open_ai import openai

app = Flask(__name__)

# Enable CORS
CORS(app)

# Initialize Flask-Mail
mail = Mail(app)

# Initialize SQLAlchemy (if needed)
db = SQLAlchemy(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = MAIL_SERVER
app.config['MAIL_PORT'] = MAIL_PORT
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD
app.config['MAIL_USE_TLS'] = MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = MAIL_USE_SSL
print("Connected to Mail successfully.")

# Production mode
app.debug = app.config.get('DEBUG', False)

# Set SQLALCHEMY_DATABASE_URI to your TiDB URI
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

# Disable SQLALCHEMY_TRACK_MODIFICATIONS warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Increase the pool size to, for example, 20
app.config['SQLALCHEMY_POOL_SIZE'] = 100

# Production mode
app.debug = app.config.get('DEBUG', True)

if app.debug:
    print("The Flask app is running in debug mode.")

try:
    # Attempt to connect to the database
    if db.engine.connect():
        print("Connected to the database successfully.")
except Exception as e:
    print("Failed to connect to the database. Error:", str(e))

# Check if cloudinary is configured
if cloudinary.config():
    print("Connected to Cloudinary successfully.")

# Check if openapi is configured
if openai.api_key:
    print("Connected to OpenAI successfully.")

# Production mode
app.debug = app.config.get('DEBUG', False)

if app.debug:
    print("The Flask app is running in debug mode.")

# Register the blueprint after the 'db_conn' setup


@app.route('/')
def index():
    # You can access the database within this route function
    # Your database operations should be here
    return "Server is running, and the database is connected."


app.register_blueprint(user_bp)
app.register_blueprint(story_bp)
app.register_blueprint(message_bp)
app.register_blueprint(tags_bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
