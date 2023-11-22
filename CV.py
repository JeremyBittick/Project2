import cv2
import cv2.aruco as aruco
import numpy as np
import requests

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Define the ArUco dictionary
aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
aruco_params = aruco.DetectorParameters_create()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect ArUco markers
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

    if np.all(ids is not None):
        for i in range(0, len(ids)):
            # Get the center of the ArUco marker
            cX = int((corners[i][0][0][0] + corners[i][0][2][0]) / 2)
            cY = int((corners[i][0][0][1] + corners[i][0][2][1]) / 2)
            
            # Check if the marker is to the left or right of the center of the frame
            frame_center = frame.shape[1] // 2
            position = 'L' if cX < frame_center else 'R'
            
            # Format the data as <tag_id><L/R>
            tag_info = f"{ids[i][0]}{position}"
            
            # Send the tag information to the Flask server
            try:
                response = requests.post('http://<raspberry-pi-ip>:5000/receive_data', data=tag_info)
                print(f"Sent data to server: {tag_info}, Response: {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"Failed to send data to server: {e}")

    # Display the resulting frame
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
