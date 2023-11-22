from flask import Flask, render_template, request
import serial

app = Flask(__name__)
ser = serial.Serial('/dev/ttyACM0', 9600)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    key = request.form['key']
    if key == 'left':
        ser.write(b'L')
    elif key == 'right':
        ser.write(b'R')
    return '', 204

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
