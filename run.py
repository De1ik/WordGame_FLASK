import os

from applications import app

# S_DEBUG = os.getenv('DB_HOST')
S_DEBUG = True
if __name__ == '__main__':
    app.run(debug=S_DEBUG)