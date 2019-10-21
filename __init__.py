from flask import Flask 
from host.config import Config
from flask_mysqldb import MySQL 

app = Flask(__name__,template_folder= '../host/templates')
app.config.from_object(Config)

app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='impact25'
app.config['MYSQL_DB']='DBMS'


from host import routes