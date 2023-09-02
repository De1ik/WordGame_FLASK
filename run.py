import os

from applications import app

h = 37

# S_DEBUG = os.getenv('DB_HOST')
S_DEBUG = False
if __name__ == '__main__':
    app.run(debug=S_DEBUG)