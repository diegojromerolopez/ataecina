import time
from typing import Tuple, List

import drawSvg
import numpy as np

from converters.base import Base


class Linifier(Base):
    DEFAULT_LINE_COUNT = 1000
    DEFAULT_COLOR_TOLERANCE = 256 // 2
    DEFAULT_STROKE_WIDTH = 1
    DEFAULT_ALLOW_LINE_INTERSECTIONS = False

    def _convert(self, output_image_path: str, **kwargs):
        line_count: int = kwargs.get('line_count', self.DEFAULT_LINE_COUNT)
        color_tolerance: int = kwargs.get('color_tolerance', self.DEFAULT_COLOR_TOLERANCE)
        stroke_width: int = kwargs.get('stroke_width', self.DEFAULT_STROKE_WIDTH)
        allow_line_intersections: int = kwargs.get('allow_line_intersections',
                                                   self.DEFAULT_ALLOW_LINE_INTERSECTIONS)

        width = self._input_image.width
        height = self._input_image.height

        start_time = time.time()
        for i in range(0, line_count):
            start_ith_time = time.time()
            delta_x = 0
            sx = None
            ex = None
            while delta_x == 0:
                sx = np.random.randint(0, width)
                ex = np.random.randint(0, width)
                sx, ex = min(sx, ex), max(sx, ex)
                delta_x = ex - sx

            sy = np.random.randint(0, height)
            ey = np.random.randint(0, height)
            sy, ey = min(sy, ey), max(sy, ey)
            delta_y = ey - sy

            slope = delta_y / delta_x
            independent_term = sy - slope * sx
            rs = []
            gs = []
            bs = []
            actual_ex = None
            actual_ey = None

            line_found = False
            line_start = sx
            line_stop = ex + 1
            while not line_found:
                if line_start >= line_stop:
                    break
                for xi in range(line_start, line_stop):
                    yi = slope * xi + independent_term
                    r, g, b = self._input_image.getpixel(xy=(xi, yi))
                    r_std_dev = np.std(rs + [r])
                    g_std_dev = np.std(gs + [g])
                    b_std_dev = np.std(bs + [b])
                    if (r_std_dev + g_std_dev + b_std_dev)/3.0 < color_tolerance:
                        actual_ex = xi
                        actual_ey = yi
                        rs.append(r)
                        gs.append(g)
                        bs.append(b)
                    else:
                        break

                if rs and gs and bs:
                    line_found = True
                    avg_r_color = np.mean(rs)
                    avg_g_color = np.mean(gs)
                    avg_b_color = np.mean(bs)
                    avg_rgb_line_color = f"rgb({int(avg_r_color)}, {int(avg_g_color)}, {int(avg_b_color)})"
                    figure = drawSvg.Line(
                        sx, -sy, actual_ex, -actual_ey,
                        fill=avg_rgb_line_color,
                        stroke=avg_rgb_line_color,
                        stroke_width=stroke_width
                    )
                    self._output_img.append(figure)
                else:
                    line_start += 1

            self._logger.debug(f"{time.time() - start_ith_time} s spent in iteration {i + 1}")

        self._logger.info(f"{time.time() - start_time} s spent")
