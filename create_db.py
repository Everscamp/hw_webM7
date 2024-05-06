import psycopg2
import configparser
# in case you don't have a db

config = configparser.ConfigParser()
config.read('config.ini')

user = config.get('DEV_DB', 'USER')
password = config.get('DEV_DB', 'PASSWORD')
domain = config.get('DEV_DB', 'DOMAIN')
port = config.get('DEV_DB', 'PORT')
db = config.get('DEV_DB', 'DB_NAME')

conn = psycopg2.connect(dbname=db, user=user, password=password, host=domain)
cursor = conn.cursor()
 
conn.autocommit = True

sql = "CREATE DATABASE test"
 
cursor.execute(sql)
print("DB was created")
 
cursor.close()
conn.close()