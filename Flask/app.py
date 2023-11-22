from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML template for the index page
index_html = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ARUCO Tag Receiver</title>
</head>
<body>
    <h1>ARUCO Tag Receiver Server</h1>
    <p>Send tag information to this server using the /receive_data endpoint.</p>
</body>
</html>
'''

@app.route('/')
def index():
    # Render the index HTML page
    return render_template_string(index_html)

@app.route('/receive_data', methods=['POST'])
def receive_data():
    data = request.data.decode('utf-8')  # Decode data from bytes to string
    tag_id, position = data[:-1], data[-1]  # Split the tag ID and position

    # Here you would add the logic to handle the received data

    # This is a placeholder for a response
    return f'Received tag ID: {tag_id} with position: {position}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
