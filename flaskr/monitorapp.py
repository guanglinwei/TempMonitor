from flask import Flask
from flask import (
    request, render_template, jsonify, Response, g
)

import sqlite3
from datetime import datetime
from pytz import timezone
import os
# from multiprocessing import Pool

tz = timezone('EST')

db = sqlite3.connect('./flaskr/database.db', check_same_thread=False)
print("Database connected")

app = Flask(__name__)

# Database setup
# ~ DATABASE = 'flaskr/database.db'

# ~ def get_db():
    # ~ db = getattr(g, '_database', None)
    # ~ if db is None:
        # ~ print("is none")
        # ~ g._database = sqlite3.connect(DATABASE)
        # ~ db = g._database
        # ~ print(db)
    # ~ return db

# ~ @app.teardown_appcontext
# ~ def close_connection(exception):
    # ~ db = getattr(g, '_database', None)
    # ~ if db is not None:
        # ~ db.close()
def get_db():
    # ~ db = sqlite3.connect('./flaskr/database.db')
    return db

@app.route('/')
def main():
    # from db
    db = get_db().cursor()
    # data = db.execute("SELECT * FROM readings LIMIT 48;").fetchall()
    data = db.execute("SELECT * FROM readings;").fetchall()
    # ~ print(data)
    # ~ print(db.execute("SELECT COUNT(*) FROM readings;").fetchone())
    data = [{'temperature': d[0], 'humidity': d[1], 'datetime': str(d[2])} for d in data]
 
    return render_template('index.html', data=data, currentTime=str(datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")))


@app.route('/_data', methods=['POST'])
def _data():
    db = get_db().cursor()

    if request.headers.get("key") != "key":
        return Response("{'message':'Not Authorized'}", status=401, mimetype='application/json')

    _temp = request.form.get('temp')
    _humid = request.form.get('humid')

    try:
        _temp = float(_temp)
        _humid = float(_humid)
    except (ValueError, KeyError, TypeError) as e:
        return Response("{'message':'Data not float'}", status=400, mimetype='application/json')
 
    db.execute("INSERT INTO readings (temperature, humidity, datetime) VALUES (?, ?, ?);", (_temp, _humid, datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")))
    count = db.execute("SELECT COUNT(*) FROM readings;").fetchone()[0]

    MAXREADINGS = 8760
    count = int(count)
    if count > MAXREADINGS:
        db.execute("DELETE FROM readings ORDER BY datetime ASC LIMIT ?;", (count - MAXREADINGS,))
    
    return Response("{'message':'success'}", status=200, mimetype='application/json')

if __name__ == "__main__":
    print("running")
    app.run(host="0.0.0.0", port="5050")
    #os
    #the_other_process = subprocess.call(['python', '/sensor.py'])

