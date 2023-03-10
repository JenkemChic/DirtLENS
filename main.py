import cv2
import numpy as np
import sys
import time

from gps_helper import get_current_position


sys.path.append('colors.py')
import colors


def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        frame = param['frame']
        pixel = frame[y, x]
        r = pixel[2]
        g = pixel[1]
        b = pixel[0]

        # Find the closest color by comparing the RGB values
        closest_color = min(colors.colors, key=lambda x: sum([abs(x[3] - r), abs(x[4] - g), abs(x[5] - b)]))
        color_name = closest_color[0]

        # Display the color name on the frame
        cv2.putText(frame, color_name, (frame.shape[1] // 40, frame.shape[0] - 180), cv2.FONT_HERSHEY_TRIPLEX, 3.75,
                    (38, 181, 181), 6)

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