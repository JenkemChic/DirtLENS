import cv2
import numpy as np
import sys
import time

from gps_helper import get_current_position
from circle_color_detector import CircleColorDetector

import colors

detector_circle_radius = 80
color_detector = CircleColorDetector(colors.colors)

data_displayed = False
display_start_time = None
display_duration = 3
last_clicked_position = None
color_name = None

def click_event(event, x, y, flags, param):
    global data_displayed, display_start_time, last_clicked_position, color_name

    if event == cv2.EVENT_LBUTTONDOWN:
        frame = param['frame']
        color_name, color_rgb = color_detector.detect_color(frame, (x, y), 10)

        if color_name is not None:
            data_displayed = True
            display_start_time = time.time()
            last_clicked_position = (x, y)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if data_displayed:
        elapsed_time = time.time() - display_start_time
        if elapsed_time < display_duration:
            x, y = last_clicked_position
            cv2.circle(frame, (x, y), detector_circle_radius, (57, 255, 20), 3)
            if color_name is not None:
                cv2.putText(frame, color_name, (frame.shape[1] // 40, frame.shape[0] - 180),
                            cv2.FONT_HERSHEY_TRIPLEX, 3.75, (38, 181, 181), 6)

                try:
                    lat, long = get_current_position()
                    gps_info = f"Latitude: {lat:.6f}  Longitude: {long:.6f}"
                except Exception as e:
                    print(f"Failed to retrieve GPS data: {e}")
                    gps_info = "GPS data unavailable"

                cv2.putText(frame, gps_info, (frame.shape[1] - 600, 70), cv2.FONT_HERSHEY_TRIPLEX, 1.5,
                            (255, 255, 255), 2)
        else:
            data_displayed = False

    cv2.imshow('frame', frame)
    cv2.setMouseCallback('frame', click_event, {'frame': frame})

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
