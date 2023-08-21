import os

from .app import app

S_DEBUG = os.getenv('DB_HOST')

if __name__ == '__main__':
    app.run(debug=S_DEBUG)