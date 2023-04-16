import cv2
import numpy as np
import time
import os

def display_logo(window_name, logo_path, cap):
    ret, frame = cap.read()
    if ret:
        if os.path.isfile(logo_path):
            logo = cv2.imread(logo_path)
            logo = cv2.resize(logo, (frame.shape[1], frame.shape[0]))
            cv2.imshow(window_name, logo)
            cv2.waitKey(1000)  # Wait 1 second

            fade_out_logo(window_name, logo)
    else:
        print("Error: Failed to read frame from the camera.")

def fade_out_logo(window_name, logo, fade_duration=2.0):
    start_time = time.time()
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > fade_duration:
            break

        alpha = 1 - elapsed_time / fade_duration
        overlay = np.zeros(logo.shape, dtype=np.uint8)
        cv2.addWeighted(logo, alpha, overlay, 1 - alpha, 0, logo)

        cv2.imshow(window_name, logo)
        cv2.waitKey(1)
