import time
import drawSvg
import numpy as np

from converters.base import Base


class RandomLinifier(Base):
    DEFAULT_LINE_COUNT = 1000
    DEFAULT_COLOR_TOLERANCE = 256 // 2
    DEFAULT_STROKE_WIDTH = 1

    def _convert(self, output_image_path: str, **kwargs):
        line_count: int = kwargs.get('line_count', self.DEFAULT_LINE_COUNT)
        color_tolerance: int = kwargs.get('color_tolerance', self.DEFAULT_COLOR_TOLERANCE)
        stroke_width: int = kwargs.get('stroke_width', self.DEFAULT_STROKE_WIDTH)

        width = self._input_image.width
        height = self._input_image.height
        sx_seq = np.random.randint(0, width, size=line_count)
        ex_seq = np.random.randint(0, width, size=line_count)
        for i in range(0, line_count):
            while sx_seq[i] - ex_seq[i] == 0:
                sx_seq[i] = np.random.randint(0, width)
                ex_seq[i] = np.random.randint(0, width)
        sy_seq = np.random.randint(0, height, size=line_count)
        ey_seq = np.random.randint(0, height, size=line_count)

        start_time = time.time()
        for i in range(0, line_count):
            start_ith_time = time.time()

            sx, ex = min(sx_seq[i], ex_seq[i]), max(sx_seq[i], ex_seq[i])
            delta_x = ex_seq[i] - sx_seq[i]

            sy, ey = min(sy_seq[i], ey_seq[i]), max(sy_seq[i], ey_seq[i])
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
