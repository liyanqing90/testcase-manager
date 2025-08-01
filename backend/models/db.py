from flask import current_app
from flask_mysqldb import MySQL
 
def get_db():
    return current_app.extensions['mysql'] 