import argparse
if __name__ == "__main__":
 # Argument Parsing
    parser = argparse.ArgumentParser(
        description='Tool for auto-screenshotting',
        prog="autopeeper.py",
        usage='%(prog)s [options]'
    )
    parser.add_argument('-v','--verbose', help='turn on verbose mode')
    parser.add_argument('-s','--single', help='scan a single url')
    parser.add_argument('-f', help='input target file')
    parser.add_argument('-o', help='output destination')
    parser.parse_args()

