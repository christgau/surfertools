#!/bin/python3
# MIT licence
# (c) Steffen Christgau <christgau@zib.de>

import sys
import struct
import argparse
import math


def read_palette(fn):
    with open(fn, 'r') as f:
        lines = f.readlines()

    m = 0
    palette = []
    for line in lines:
        if line.strip().startswith('#'):
            continue

        items = line.strip().split()
        palette.append({
            'start': float(items[0]),
            'end': float(items[4]),
            'start_col': (float(items[1]), float(items[2]), float(items[3])),
            'end_col': (float(items[5]), float(items[6]), float(items[7])),
        })

        m = max(m, max(float(x) for x in items[1:4] + items[5:8]))

    scale = 255 / m if m < 255 else 1

    for pi in palette:
        for n in ['start_col', 'end_col']:
            pi[n] = tuple([int(x * scale) for x in pi[n]])

    return palette


def get_color(v, palette):
    if not palette:
        gray = (min(int(abs(v/255)), 255))
        return (gray, gray, gray)

    retval = palette[0]['start_col']

    for pi in palette:
        s = pi['start']
        e = pi['end']
        start_col = pi['start_col']
        end_col = pi['end_col']

        if (s <= v) and (v <= e):
            k = abs((v - s) / (s - e))
            r = int(start_col[0] + (end_col[0] - start_col[0]) * k)
            g = int(start_col[1] + (end_col[1] - start_col[1]) * k)
            b = int(start_col[2] + (end_col[2] - start_col[2]) * k)

            return (r, g, b)
        elif (s > v):
            return retval

    return palette[-1]['end_col']


parser = argparse.ArgumentParser()
parser.add_argument('source')
parser.add_argument(
    '-l', '--log',
    help='apply log on each value', action='store_true')
parser.add_argument(
    '-n', '--normalize',
    help='normalize based on min and max', action='store_true')
parser.add_argument(
    '-p', '--palette',
    help='color palette to use', default=None)

args = parser.parse_args(sys.argv[1:])

src = sys.stdin.buffer if not args.source else open(args.source, 'rb')
dst = sys.stdout.buffer

header = src.read(4)
if header == b'DSBB':
    dims = struct.unpack('hh', src.read(4))
    boundaries = struct.unpack('d' * 6, src.read(8 * 6))

    n = dims[0] * dims[1]
    plane = struct.unpack('f' * n, src.read(4 * n))
elif header == b'DSAA':
    src.readline()
    dims = [int(x) for x in src.readline().split()]
    boundaries = [float(x) for x in src.readline().split()] + \
        [float(y) for y in src.readline().split()] + \
        [float(z) for z in src.readline().split()]

    plane = [float(i) for i in src.read().split()]
else:
    print("unsupported input file format", file=sys.stderr)
    sys.exit(1)

palette = read_palette(args.palette) if args.palette else None

if args.log:
    plane = [math.log10(v) if v > 0 else 0 for v in plane]

if args.normalize:
    lb = min(plane)
    ub = max(plane)
    plane = [(v - lb) / (ub - lb) for v in plane]

dst.write('P6\n{} {}\n255\n'.format(dims[0], dims[1]).encode('ascii'))
for v in plane:
    dst.write(struct.pack('BBB', *get_color(v, palette)))

