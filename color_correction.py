import cv2
import numpy as np

def apply_white_balance(frame, white_balance):
    # Convert the frame to LAB color space
    lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)

    # Split the LAB channels
    L, A, B = cv2.split(lab)

    # Normalize the A and B channels with the white balance values
    A_balanced = np.uint8(np.clip((white_balance[1] / 128.0) * (A - 128) + 128, 0, 255))
    B_balanced = np.uint8(np.clip((white_balance[2] / 128.0) * (B - 128) + 128, 0, 255))

    # Merge the balanced channels and convert back to BGR color space
    balanced_lab = cv2.merge((L, A_balanced, B_balanced))
    balanced_bgr = cv2.cvtColor(balanced_lab, cv2.COLOR_LAB2BGR)

    return balanced_bgr
