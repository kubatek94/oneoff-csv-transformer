#!/usr/bin/env python3

import os
import sys
import glob
import csv


def line_to_mean(line):
    return line.split(',', 2)[1]


def skip_to(file, needle):
    line = ''
    while not line.startswith(needle):
        line = file.readline()
    return line


def file_to_row(file):
    r = line_to_mean(skip_to(file, 'R Mean'))
    t = line_to_mean(skip_to(file, 'T Mean'))
    return [r, t, os.path.basename(file.name)]


def dir_to_rows(dir_path):
    rows = []
    csv_glob = os.path.join(os.path.abspath(dir_path), '*.csv')
    for path in glob.glob(csv_glob):
        with open(path, 'r') as f:
            rows.append(file_to_row(f))
    return rows


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('Usage: %s <input_path> <output_file>' % sys.argv[0])

    input_path = sys.argv[1]
    if not os.path.isdir(input_path):
        sys.exit('Input path "%s" is not a directory.' % input_path)

    output_file = sys.argv[2]
    if os.path.exists(output_file):
        sys.exit('Output file "%s" already exists.' % output_file)

    all_rows = dir_to_rows(input_path)
    with open(output_file, 'w', newline='') as of:
        writer = csv.writer(of)
        writer.writerow(['temperature', 'resistance', 'filename'])
        for row in all_rows:
            writer.writerow(row)

