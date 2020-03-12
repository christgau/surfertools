#!/bin/python3

import sys
import struct
import argparse
import math

def read_surfer_file(fn):
    src = open(fn, 'rb')
    header = src.read(4)
    if header == b'DSBB':
        dims = struct.unpack('hh', src.read(4))
        boundaries = struct.unpack('d' * 6, src.read(8 * 6))

        n = dims[0] * dims[1]
        return (dims[0], dims[1], struct.unpack('f' * n, src.read(4 * n)))
    elif header == b'DSAA':
        src.readline()
        dims = [int(x) for x in src.readline().split()]
        boundaries = [float(x) for x in src.readline().split()] + \
            [float(y) for y in src.readline().split()] + \
            [float(z) for z in src.readline().split()]

        return (dims[0], dims[1], [float(i) for i in src.read().split()])
    else:
        print("unsupported input file format", file=sys.stderr)
        sys.exit(1)


parser = argparse.ArgumentParser()
parser.add_argument('reference')
parser.add_argument('comparand')
parser.add_argument('-dx', '--deltax', default=0)
parser.add_argument('-dy', '--deltay', default=0)

args = parser.parse_args(sys.argv[1:])

xa, ya, va = read_surfer_file(args.reference)
xb, yb, vb = read_surfer_file(args.comparand)

if not xa == xb:
    print("inputs differ in x size ({} vs {})".format(xa, xb), file=sys.stderr)

if not ya == yb:
    print("inputs differ in y size ({} vs {})".format(ya, yb), file=sys.stderr)

excesses = 0
max_rel_delta = 0
EXCESS_THRESHOLD = 0.00

# for i in range(xa * ya):

dx = int(args.deltax)
dy = int(args.deltay)

print("max_ref: {}, min_ref: {}", max(va), min(va))
print("max_v:   {}, min_v:   {}", max(vb), min(vb))

diff_pair = (None, None)

for y in range(dy, min(ya, yb)):
    for x in range(dx, min(xa, xb)):
#        if x + args.deltax < xa and y + args.deltay < ya:
        idx_ref = (y - dy) * xa + (x - dx)
#        idx_ref = (y) * xa + (x)
        idx_c = y * xb + x

        delta = abs(vb[idx_c] - va[idx_ref])
        if va[idx_ref] != 0:
            r = delta / abs(va[idx_ref])
            if (r > EXCESS_THRESHOLD):
                excesses = excesses + 1
                if r > max_rel_delta:
                    max_rel_delta = r
                    diff_pair = (va[idx_ref], vb[idx_c])
        elif delta != 0:
            print('detected delta of {}, but cannot compute relative error'.format(delta))


if excesses == 0:
    sys.exit(0)
else:
    print("inputs differ at {} points (max rel. delta = {})".format(
        excesses, max_rel_delta))
    print(diff_pair)
    sys.exit(4)
