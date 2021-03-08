import time
import schedule
import smbus
import requests
# pip install schedule

bus = smbus.SMBus(1)

def get_data(post=True):
    rh = bus.read_i2c_block_data(0x40, 0xE5, 2)
    time.sleep(0.1)
    humidity = ((rh[0] * 256 + rh[1]) * 125 / 65536.0) - 6

    temp = bus.read_i2c_block_data(0x40, 0xE3,2)
    time.sleep(0.1)
    cTemp = ((temp[0] * 256 + temp[1]) * 175.72 / 65536.0) - 46.85
    fTemp = cTemp * 1.8 + 32

    # ~ print ("Humidity %%RH: %.2f%%" %humidity)
    # ~ print ("Temperature Celsius: %.2fC" %cTemp)
    # ~ print ("Temperature Fahrenheit: %.2fF" %fTemp)
    print(humidity, fTemp)
    
    if post:
        # send post request to /_data
        key = "key"
        url = "http://localhost:5050/_data"
        
        try:
            r = requests.post(url, headers={'key': key}, data={'humid': humidity, 'temp': fTemp})
        except requests.exceptions.RequestException as e:
            print("Request error", e)
            
    
    return {'humid': humidity, 'temp': fTemp}
    #if r.status_code != requests.codes.ok:
    #    print("Error sending data:\n\t", r.json())

# ~ schedule.every().hour.do(get_data)
# ~ schedule.every().second.do(get_data)

if __name__ == "__main__":
    print("setting schedule")
    schedule.every(30).minutes.do(get_data)

    while True:
        schedule.run_pending()
        time.sleep(10)
        # ~ time.sleep(1)

