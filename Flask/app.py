from flask import Flask, render_template, Response, request
import cv2
import serial

app = Flask(__name__)

# Initialize serial communication with the Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)

# Generator function that captures video frames and yields them for the stream
def gen_frames():  
    camera = cv2.VideoCapture(0)  # use 0 for web camera
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    # Return the main page, including the stream
    return render_template('index.html')

@app.route('/command', methods=['POST'])
def command():
    # Receive the command from the key press on the webpage and send to the Arduino
    key = request.form['key']
    if key == 'left':
        ser.write(b'L')
    elif key == 'right':
        ser.write(b'R')
    return '', 204

@app.route('/video_feed')
def video_feed():
    # Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
