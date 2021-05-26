import argparse
import datetime
from converters.random_circler import RandomCircler

DEFAULT_LINIFER_SEED = 1234

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True)
    parser.add_argument("-s", "--seed", type=int, required=False,
                        default=DEFAULT_LINIFER_SEED)
    parser.add_argument("-cc", "--circle_count", type=int, required=False,
                        default=RandomCircler.DEFAULT_CIRCLE_COUNT)
    parser.add_argument("-mincr", "--min_circle_radius", type=int, required=False,
                        default=RandomCircler.DEFAULT_MIN_CIRCLE_RADIUS)
    parser.add_argument("-maxcr", "--max_circle_radius", type=int, required=False,
                        default=RandomCircler.DEFAULT_MAX_CIRCLE_RADIUS)
    parser.add_argument("-tol", "--color_tolerance", type=int, required=False,
                        default=RandomCircler.DEFAULT_COLOR_TOLERANCE)
    parser.add_argument("-ov", "--allow_overlaping", default=False, action='store_true')
    parser.add_argument("-nov", "-forbid_overlaping", default=True, action='store_false')
    parser.add_argument("-pad", "--padding_between_circles", type=int, required=False,
                        default=RandomCircler.DEFAULT_PADDING_BETWEEN_CIRCLES)
    parser.add_argument("-mov", "-max_overlap_tries", type=int, required=False,
                        default=RandomCircler.DEFAULT_MAX_OVERLAP_TRIES)

    parser.add_argument(
        "-o", "--output", type=str, required=False,
        default=f"output.{datetime.datetime.utcnow().isoformat()}.svg")
    args = parser.parse_args()
    image_converter = RandomCircler(input_image_path=args.input)
    image_converter.set_random_seed(seed=args.seed)
    image_converter.convert(output_image_path=args.output,
                            circle_count=args.circle_count,
                            min_circle_radius=args.min_circle_radius,
                            max_circle_radius=args.max_circle_radius,
                            color_tolerance=args.color_tolerance,
                            allow_overlaping=args.allow_overlaping)


