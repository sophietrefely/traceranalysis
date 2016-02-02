# Usability issues
#  - Files must be correctly formed
#  - Files must have the .csv extension (note, allow also .txt)

import csv
import numpy as np
import os

# 1) Read all files in and identify keys e.g.
#    if there are files like:
#      [set-a_averages, set-b_averages, set-a_data, set-b_data]
#    produce
#      [set-a, set-b]
job_keys = set()
filenames = os.listdir()
for filename in filenames:
    basename = os.path.splitext(filename)[0]
    # Find just the basename
    basename = basename.replace('_averages', '').replace('_data', '')
    job_keys.add(basename)

# 2) For all the possible job keys e.g. set-a, set-b, 3hb-coa, etc
#    open the files, get the data and run job
#    ignore job keys from random files that do not have the _averages and _data
valid_jobs = set()
for job_key in job_keys:
    # Check that there exists <job_key>_averages AND <job_key>_data
    averages_fname = '{0}_averages.csv'.format(job_key)
    data_fname = '{0}_data.csv'.format(job_key)
    # TODO maybe check for both .txt and .csv above for robustness
    if averages_fname in filenames and data_fname in filenames:
        valid_jobs.add(job_key)

# 3) For each job  in valid_jobs, load into numpy, do analyis, write result
for job_key in valid_jobs:
    averages_fname = '{0}_averages.csv'.format(job_key)
    data_fname = '{0}_data.csv'.format(job_key)

    averages = list(csv.reader(open(averages_fname, "r"), delimiter=","))[0]

    # Read in data file line by line
    data = []
    for line in open(data_fname):
        data_line = []
        for str_float in line.split(','):
            if not str_float.isspace():
                data_line.append(float(str_float))
        data.append(data_line)
    data = np.array(data)

    # Old way - had issues with whitespace
    #data = np.loadtxt(open(data_fname, "r"), delimiter=",")

    print('averages:', averages)
    print('data:', data)

    # Remove potential accidental " " in data and convert to float
    float_averages = []
    for number in averages:
        if not number.isspace():
            float_number = float(number)
            float_averages.append(float_number)
    print('averages:', float_averages)

    diagonal_matrix = []
    num_rows = len(float_averages)
    # Make a copy of everything in averages in new list
    # Add zeros at the front to make values sit on diagonal
    # Slice the end to make it square
    for row_number in range(num_rows):
        averages_copy = list(float_averages)
        averages_zeros  = [0] * row_number + averages_copy
        averages_sliced = averages_zeros[:num_rows]
        diagonal_matrix.append(averages_sliced)

    diagonal_matrix = np.array(diagonal_matrix)
    print(diagonal_matrix)

    inverse = np.linalg.inv(diagonal_matrix)
    result = np.dot(data, inverse)

    # Numpy vector where <n>th element is the sum of row <n>
    data_rows = len(data)
    print(data_rows)
    row_sums = np.sum(result, axis=1)
    for row_number in range(data_rows):
        result[row_number, :] *= 100/row_sums[row_number]

    # print to a file
    output_fname = '{0}_output.csv'.format(job_key)
    np.savetxt(output_fname, result, fmt='%.1f', delimiter=',')
