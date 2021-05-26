import math
import time
from typing import Tuple, Iterator

import drawSvg
import numpy as np

from converters.base import Base


class RandomCircler(Base):
    DEFAULT_CIRCLE_COUNT = 1000
    DEFAULT_COLOR_TOLERANCE = 256 // 2
    DEFAULT_MIN_CIRCLE_RADIUS = 5
    DEFAULT_MAX_CIRCLE_RADIUS = 50
    DEFAULT_PADDING_BETWEEN_CIRCLES = 0
    DEFAULT_ALLOW_OVERLAPING = False
    DEFAULT_MAX_OVERLAP_TRIES = 1000

    def __points_in_circle(
            self, cx: int, cy: int, radius: int
    ) -> Iterator[Tuple[int, int]]:
        for rx in range(0, radius+1):
            for ry in range(0, radius+1):
                yield cx + rx, cy + ry

    def __circle_overlaps_existing_circles(
        self, x: int, y: int,
        radius: int, padding: int = DEFAULT_PADDING_BETWEEN_CIRCLES
    ) -> bool:
        for x_i, y_i, radius_i in self.circles:
            distance = math.sqrt((x - x_i) * (x - x_i) + (y - y_i) * (y - y_i))
            if distance <= radius + radius_i + padding:
                return True
        return False

    def __circle_is_tolerated(self, cx, cy, radius, color_tolerance):
        width = self._input_image.width
        height = self._input_image.height
        rs = []
        gs = []
        bs = []
        for x_i, y_i in self.__points_in_circle(cx=cx, cy=cy, radius=radius):
            if 0 <= x_i < width and 0 <= y_i < height:
                r, g, b = self._input_image.getpixel(xy=(x_i, y_i))
                rs.append(r)
                gs.append(g)
                bs.append(b)
        r_std_dev = np.std(rs)
        g_std_dev = np.std(gs)
        b_std_dev = np.std(bs)
        tolerated = (r_std_dev + g_std_dev + b_std_dev)/3.0 < color_tolerance
        if tolerated:
            return True, np.mean(rs), np.mean(gs), np.mean(bs)
        return False, None, None, None

    def _convert(self, output_image_path: str, **kwargs):
        circle_count: int = kwargs.get('circle_count', self.DEFAULT_CIRCLE_COUNT)
        color_tolerance: int = kwargs.get('color_tolerance', self.DEFAULT_COLOR_TOLERANCE)
        min_circle_radius: int = kwargs.get('min_circle_radius', self.DEFAULT_MIN_CIRCLE_RADIUS)
        max_circle_radius: int = kwargs.get('max_circle_radius', self.DEFAULT_MAX_CIRCLE_RADIUS)
        allow_overlaping: bool = kwargs.get('allow_overlaping', self.DEFAULT_ALLOW_OVERLAPING)
        padding_between_circles: bool = kwargs.get('padding_between_circles', self.DEFAULT_PADDING_BETWEEN_CIRCLES)
        max_overlap_tries: int = kwargs.get('max_overlap_tries', self.DEFAULT_MAX_OVERLAP_TRIES)

        min_circle_radius, max_circle_radius = (
            min(min_circle_radius, max_circle_radius),
            max(min_circle_radius, max_circle_radius)
        )

        width = self._input_image.width
        height = self._input_image.height

        random_x_seq = np.random.randint(0, width, size=circle_count)
        random_y_seq = np.random.randint(0, height, size=circle_count)

        self.circles = []
        for i in range(0, circle_count):
            start_time = time.time()
            last_legal_circle = None
            cx = random_x_seq[i]
            cy = random_y_seq[i]
            radius = min_circle_radius
            tolerated, r, g, b = self.__circle_is_tolerated(cx, cy, radius, color_tolerance)
            overlaps = not allow_overlaping and self.__circle_overlaps_existing_circles(x=cx, y=cy, radius=radius,
                                                                                        padding=padding_between_circles)
            overlap_count = 0
            while (allow_overlaping or not overlaps) and tolerated and radius < max_circle_radius:
                last_legal_circle = (cx, cy, radius, r, g, b)
                tolerated, r, g, b = self.__circle_is_tolerated(cx, cy, radius, color_tolerance)
                overlaps = not allow_overlaping and self.__circle_overlaps_existing_circles(x=cx, y=cy, radius=radius)
                radius += 1
                if overlaps:
                    overlap_count += 1
                if overlap_count > max_overlap_tries:
                    break

            if last_legal_circle:
                cx, cy, radius, r, g, b = last_legal_circle
                self.circles.append((cx, cy, radius))
                avg_rgb_color = f"rgb({int(r)}, {int(g)}, {int(b)})"
                figure = drawSvg.Circle(
                    cx, -cy, radius,
                    fill=avg_rgb_color,
                    stroke=avg_rgb_color,
                    stroke_width=1
                )
                self._output_img.append(figure)

            spent_time = time.time() - start_time
            self._logger.info(
                f"{i+1}th circle ({cx}, {cy}) of radius {radius} computed in {spent_time} s"
            )
