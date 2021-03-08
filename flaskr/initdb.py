import sqlite3
import sys


drop = raw_input("Reinitialize the database? This will drop the current data. (y/n/q): ").lower() 
if drop == "y":
    import sensor
    from pytz import timezone
    from datetime import datetime
    
    conn = sqlite3.connect('flaskr/database.db')
    db = conn.cursor()

    db.execute("DROP TABLE IF EXISTS readings")
    db.execute("""CREATE TABLE readings (
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            datetime TEXT NOT NULL
        )""")
    
    dat = sensor.get_data(False)
    _temp = dat['temp']
    _humid = dat['humid']
    tz = timezone('EST')
    db.execute("INSERT INTO readings (temperature, humidity, datetime) VALUES (?, ?, ?);", (_temp, _humid, datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")))
    
    conn.commit()
    conn.close()

elif drop == "q":
    sys.exit()
    
else:
    print("Continuing without reset db")

# cursor = db.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cursor.fetchall())

