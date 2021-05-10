import argparse
import sys

parser = argparse.ArgumentParser(description="Does some awesome things.")
parser.add_argument('message', type=str, help="pass a message into the script")

if __name__ == '__main__':
    args = parser.parse_args(sys.argv[1:])
    print args.message