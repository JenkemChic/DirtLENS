import cv2
import numpy as np
import sys
import time

from gps_helper import get_current_position
from circle_color_detector import CircleColorDetector

sys.path.append('colors.py')
import colors

detector_circle_radius = 80
color_detector = CircleColorDetector()

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        frame = param['frame']

        # Draw a bright yellow circle around the clicked point
        cv2.circle(frame, (x, y), detector_circle_radius, (22, 240, 0), 2)

        # Detect the color at the clicked point
        color_name, color_rgb = color_detector.detect_color(frame, (x, y), detector_circle_radius)

        # Retrieve GPS data and display it on the screen
        try:
            lat, long = get_current_position()
            gps_info = f"Latitude: {lat:.6f}  Longitude: {long:.6f}"
        except Exception as e:
            print(f"Failed to retrieve GPS data: {e}")
            gps_info = "GPS data unavailable"
        cv2.putText(frame, gps_info, (frame.shape[1] - 600, 70), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (255, 255, 255), 2)

        cv2.imshow('frame', frame)
        time.sleep(2)

cap = cv2.VideoCapture(0)
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', click_event, param={'frame': None})

while True:
    ret, frame = cap.read()
    cv2.imshow('frame', frame)
    cv2.setMouseCallback('frame', click_event, param={'frame': frame})

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
