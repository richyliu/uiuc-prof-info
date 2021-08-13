import sys
import argparse


def main(*args):
    parser = argparse.ArgumentParser()

    args = parser.parse_args(args)



if __name__ == "__main__":
    main(*sys.argv[1:])
