import cv2
import numpy as np
from colors import colors

class CircleColorDetector:
    def __init__(self, colors):
        self.colors = colors

    def get_color_name(self, color_rgb):
        color_diffs = []
        for color in self.colors:
            lab_color = cv2.cvtColor(np.uint8([[color_rgb]]), cv2.COLOR_RGB2LAB)[0][0]
            lab_color_ref = cv2.cvtColor(np.uint8([[color[3:6]]]), cv2.COLOR_RGB2LAB)[0][0]
            delta_e = cv2.norm(lab_color, lab_color_ref, cv2.NORM_L2)
            color_diffs.append((color[0], delta_e))

        min_diff_color = min(color_diffs, key=lambda x: x[1])
        return min_diff_color[0], min_diff_color[1]

    def get_average_color_within_circle(self, frame, x, y, r):
        circle_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        cv2.circle(circle_mask, (x, y), r, (255, 255, 255), -1)
        circle = cv2.bitwise_and(frame, frame, mask=circle_mask)
        mask_pixels = cv2.countNonZero(circle_mask)
        if mask_pixels == 0:
            return (0, 0, 0)
        y_indices, x_indices = np.where(circle_mask == 255)
        distances = np.sqrt((y_indices - y) ** 2 + (x_indices - x) ** 2)
        weights = 1 - distances / r
        weights = np.clip(weights, 0, 1)
        circle_values = frame[y_indices, x_indices]
        weighted_average_color = np.average(circle_values, axis=0, weights=weights)
        average_color = tuple(map(int, weighted_average_color))
        return average_color

    def detect_color(self, frame, click_point, radius):
        x, y = click_point
        average_color_within_circle = self.get_average_color_within_circle(frame, x, y, radius)
        color_name, color_rgb = self.get_color_name(average_color_within_circle)

        # Display the color name on the frame
        cv2.putText(frame, color_name, (frame.shape[1] // 40, frame.shape[0] - 180), cv2.FONT_HERSHEY_TRIPLEX, 3.75,
                    (38, 181, 181), 6)

        return color_name, color_rgb
