import cv2
import numpy as np
import white_balance

video_capture = cv2.VideoCapture(0)

# Set the white balance
print("Setting white balance. Click on the live video to set the white balance.")
white_balance.set_white_balance(video_capture)
print("White balance has been set.")

# Start the main loop
while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Apply the white balance correction
    b_ratio, g_ratio, r_ratio = white_balance.get_white_balance(video_capture)
    frame[:, :, 0] = np.uint8(np.clip(frame[:, :, 0] * b_ratio, 0, 255))
    frame[:, :, 1] = np.uint8(np.clip(frame[:, :, 1] * g_ratio, 0, 255))
    frame[:, :, 2] = np.uint8(np.clip(frame[:, :, 2] * r_ratio, 0, 255))

    # Display the resulting frame
    cv2.imshow('Video', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
video_capture.release()
cv2.destroyAllWindows()
