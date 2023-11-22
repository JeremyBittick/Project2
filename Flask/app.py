from flask import Flask, render_template, request
import serial
from serial.serialutil import SerialException

app = Flask(__name__)

# Attempt to connect to the serial port
try:
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
except SerialException:
    print("Serial port error: Unable to open '/dev/ttyACM0'")
    ser = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    key = request.form['key']
    if ser is not None:
        if key == 'left':
            ser.write(b'L')
        elif key == 'right':
            ser.write(b'R')
    else:
        print("Serial port not available.")
    return '', 204

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', debug=True)
    finally:
        if ser is not None:
            ser.close()
