import logging
import tempfile
import time

import drawSvg
import numpy as np
from PIL import Image


class Base(object):
    _logger = None

    @classmethod
    def __init_logger(cls):
        if cls._logger is None:
            cls._logger = logging.getLogger(__name__)
            cls._logger.setLevel(level=logging.DEBUG)
            logger_console_handler = logging.StreamHandler()
            logger_console_handler.setLevel(logging.DEBUG)
            logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            logger_console_handler.setFormatter(logger_formatter)
            cls._logger.addHandler(logger_console_handler)

    def __new__(cls, *args, **kwargs):
        cls.__init_logger()
        return super().__new__(cls)

    def __init__(self, input_image_path: str, mode: str = "RGB"):
        self._input_image_path = input_image_path
        self._input_image: Image.Image = Image.open(self._input_image_path).convert(mode)
        width: int = self._input_image.width
        height: int = self._input_image.height
        self._output_img = drawSvg.Drawing(width=width, height=height,
                                           origin=(0, -height), displayInline=False)

    def __save_output_image(self, output_image_path: str):
        if output_image_path.endswith('.png'):
            self._output_img.savePng(output_image_path)
        elif output_image_path.endswith(".jpg") or output_image_path.endswith(".jpeg"):
            with tempfile.NamedTemporaryFile() as temp_file:
                self._output_img.savePng(temp_file.name)
                rgb_img = Image.open(temp_file.name).convert('RGB')
                rgb_img.save(output_image_path)
        else:
            self._output_img.saveSvg(output_image_path)

    def _convert(self, output_image_path: str, **kwargs):
        raise NotImplementedError()

    @classmethod
    def set_random_seed(cls, seed: int):
        np.random.seed(seed)

    def convert(self, output_image_path: str, **kwargs):
        start_time = time.time()
        self._convert(output_image_path=output_image_path, **kwargs)
        end_time = time.time()
        self._logger.info(
            f"{self.__class__.__name__}.convert spent time {end_time-start_time} s")

        self.__save_output_image(output_image_path=output_image_path)

