import cv2
import numpy as np
import sys
import time
from logo import display_logo

from gps_helper import get_current_position
from circle_color_detector import CircleColorDetector

import colors

detector_circle_radius = 95
color_detector = CircleColorDetector(colors.colors)

def cardinal_direction(latitude, longitude):
    if latitude > 0:
        lat_direction = 'N'
    else:
        lat_direction = 'S'

    if longitude > 0:
        long_direction = 'E'
    else:
        long_direction = 'W'

    return f"{lat_direction}{long_direction}"

def click_event(event, x, y, flags, param):
    global data_displayed, start_time, last_click_x, last_click_y, top_right_clicks
    if event == cv2.EVENT_LBUTTONDOWN:
        if x > frame.shape[1] - 100 and y < 100:
            top_right_clicks += 1
            if top_right_clicks == 3:
                cv2.destroyAllWindows()
                sys.exit()
        else:
            top_right_clicks = 0

        data_displayed = True
        start_time = time.time()
        last_click_x = x
        last_click_y = y

cap = cv2.VideoCapture(0)

window_name = 'frame'
cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

logo_path = 'logo.png'
display_logo(window_name, logo_path, cap)

data_displayed = False
start_time = None
last_click_x = None
last_click_y = None
top_right_clicks = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if data_displayed:
        elapsed_time = time.time() - start_time
        if elapsed_time > 3:
            data_displayed = False

    original_frame = frame.copy()

    if data_displayed and last_click_x is not None and last_click_y is not None:
        x, y = last_click_x, last_click_y
        color_name, color_rgb = color_detector.detect_color(original_frame, (x, y), detector_circle_radius)
        if color_name is not None:
            center_x = frame.shape[1] // 2
            color_text_size, _ = cv2.getTextSize(color_name, cv2.FONT_HERSHEY_COMPLEX, 3.75, 6)

            # Draw color name with a fat black border
            for i in range(-6, 7):
                for j in range(-6, 7):
                    cv2.putText(frame, color_name,
                                (center_x - color_text_size[0] // 2 + i, color_text_size[1] + 20 + j),
                                cv2.FONT_HERSHEY_COMPLEX, 3.75, (0, 0, 0), 5, cv2.LINE_AA)
            cv2.putText(frame, color_name, (center_x - color_text_size[0] // 2, color_text_size[1] + 20),
                        cv2.FONT_HERSHEY_COMPLEX, 3.75, (255, 255, 255), 5, cv2.LINE_AA)

            lat, long = get_current_position()
            cardinal_dir = cardinal_direction(lat, long)
            gps_info = f"{cardinal_dir} Wall"
            gps_text_size, _ = cv2.getTextSize(gps_info, cv2.FONT_HERSHEY_COMPLEX, 1.75, 3)

            # Draw GPS info with a fat black border
            for i in range(-4, 5):
                for j in range(-4, 5):
                    cv2.putText(frame, gps_info,
                                (int(frame.shape[1] / 3 - gps_text_size[0] / 3) + i,
                                 frame.shape[0] - gps_text_size[1] - 10 + j),
                                cv2.FONT_HERSHEY_COMPLEX, 2.75, (0, 0, 0), 3, cv2.LINE_AA)
            cv2.putText(frame, gps_info,
                        (int(frame.shape[1] / 3 - gps_text_size[0] / 3), frame.shape[0] - gps_text_size[1] - 10),
                        cv2.FONT_HERSHEY_COMPLEX, 2.75, (255, 255, 255), 3, cv2.LINE_AA)

            cv2.circle(frame, (x, y), detector_circle_radius, (0, 255, 0), 2)

    cv2.imshow('frame', frame)
    cv2.setMouseCallback('frame', click_event)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
