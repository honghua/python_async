from argparse import ArgumentParser
import time

parser = ArgumentParser()
parser.add_argument("time", type=int, default=3)

args = parser.parse_args()

for _ in range(args.time):
    print(".", end=" ", flush=True)
    time.sleep(1)

print("done")

