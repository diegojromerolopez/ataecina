import argparse
import datetime
from converters.random_linifier import RandomLinifier

DEFAULT_LINIFER_SEED = 1234

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True)
    parser.add_argument("-s", "--seed", type=int, required=False,
                        default=DEFAULT_LINIFER_SEED)
    parser.add_argument("-lc", "--line_count", type=int, required=False,
                        default=RandomLinifier.DEFAULT_LINE_COUNT)
    parser.add_argument("-sw", "--stroke_width", type=int, required=False,
                        default=RandomLinifier.DEFAULT_STROKE_WIDTH)
    parser.add_argument("-tol", "--color_tolerance", type=int, required=False,
                        default=RandomLinifier.DEFAULT_COLOR_TOLERANCE)
    parser.add_argument(
        "-o", "--output", type=str, required=False,
        default=f"output.{datetime.datetime.utcnow().isoformat()}.svg")
    args = parser.parse_args()
    image_converter = RandomLinifier(input_image_path=args.input)
    image_converter.set_random_seed(seed=args.seed)
    image_converter.convert(output_image_path=args.output,
                            line_count=args.line_count,
                            stroke_width=args.stroke_width,
                            color_tolerance=args.color_tolerance)


