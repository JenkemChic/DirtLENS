import cv2
import numpy as np
from colors import colors


class CircleColorDetector:
    def __init__(self, colors):
        self.colors = colors

    def get_color_name(self, color_rgb):
        color_diffs = []
        for color in self.colors:
            diff = sum([abs(color[i + 3] - color_rgb[i]) for i in range(3)])
            color_diffs.append((color[0], diff))

        min_diff_color = min(color_diffs, key=lambda x: x[1])
        return min_diff_color[0], min_diff_color[1]

    def get_average_color_within_circle(self, frame, x, y, r):
        circle_mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        cv2.circle(circle_mask, (x, y), r, (255, 255, 255), -1)
        circle = cv2.bitwise_and(frame, frame, mask=circle_mask)
        mask_pixels = cv2.countNonZero(circle_mask)
        if mask_pixels == 0:
            return (0, 0, 0)
        circle_sum = cv2.sumElems(circle)
        circle_sum = np.array(circle_sum)
        average_color = tuple(map(lambda x: int(x / mask_pixels), circle_sum))
        return average_color

    def detect_color(self, frame, click_point, radius):
        x, y = click_point
        average_color_within_circle = self.get_average_color_within_circle(frame, x, y, radius)
        color_name, color_rgb = self.get_color_name(average_color_within_circle)

        # Display the color name on the frame
        cv2.putText(frame, color_name, (frame.shape[1] // 40, frame.shape[0] - 180), cv2.FONT_HERSHEY_TRIPLEX, 3.75,
                    (38, 181, 181), 6)

        return color_name, color_rgb
