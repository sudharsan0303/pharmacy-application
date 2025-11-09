from flask import Flask, render_template
from auth.routes import auth
import os

app = Flask(__name__)

# Set the secret key from an environment variable or fallback to a default
app.secret_key = os.getenv('FLASK_SECRET_KEY', os.urandom(24))

# Register the auth blueprint
app.register_blueprint(auth)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # Use the specified IP and port
    app.run(host='127.0.0.2', port=5001, debug=True)