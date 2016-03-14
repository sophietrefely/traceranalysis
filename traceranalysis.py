# Usability issues
#  - Files must be correctly formed
#  - Files must have the .csv extension (note, allow also .txt)

import csv
import numpy as np
import os

import csv
import numpy as np

### DEFINE DO_TRACER_ANALYSIS

def do_tracer_analysis(data, unlabeled):
    averages = np.average(unlabeled, axis=0).tolist() #average the unlabeled data by column

    diagonal_matrix = []
    num_rows = len(averages)
    # Make a copy of everything in averages in new list
    # Add zeros at the front to make values sit on diagonal
    # Slice the end to make it square
    for row_number in range(num_rows):
        averages_copy = list(averages)
        averages_zeros  = [0] * row_number + averages_copy
        averages_sliced = averages_zeros[:num_rows]
        diagonal_matrix.append(averages_sliced)

    diagonal_matrix = np.array(diagonal_matrix)
    print(diagonal_matrix)

    inverse = np.linalg.inv(diagonal_matrix)
    SUPERMAN = np.dot(data, inverse)

    # Numpy vector where <n>th element is the sum of row <n>
    data_rows = len(data)
    print(data_rows)
    row_sums = np.sum(SUPERMAN, axis=1)
    for row_number in range(data_rows):
        SUPERMAN[row_number, :] *= 100/row_sums[row_number]
    return SUPERMAN

### ENDDEFINE DO_TRACER_ANALYSIS

### DEFINE PREPARE_DATA_FOR_ANALYSIS

def prepare_data_for_analysis(all_data_input):
    # Read in data file line by line
    data = []
    for line in all_data_input.split('\n'):
        # If the line is a whitespace error from excel ignore it
        if line.isspace():
            continue
        #strip line to deal with trailing commas
        strip_line = line.rstrip(',')
        
        data_line = []
        for str_float in strip_line.split(','):
            if not str_float.isspace():
                data_line.append(float(str_float))
        data.append(data_line)
    data = np.array(data)
    return data

### ENDDEFINE PREPARE_DATA_FOR_ANALYSIS

### DEFINE PREPARE_UNLABELED_FOR_ANALYSIS

def prepare_unlabeled_for_analysis(user_unlabeled_data):
    unlabeled = np.array(
        list(csv.reader(user_unlabeled_data.split('\n'), delimiter=",")),
    ).astype(np.float)
    return unlabeled

### ENDDEFINE PREPARE_UNLABELED_FOR_ANALYSIS
    
# 1) Read all files in and identify keys e.g.
#    if there are files like:
#      [set-a_unlabeled, set-b_unlabeled, set-a_data, set-b_data]
#    produce
#      [set-a, set-b]
job_keys = set()
filenames = os.listdir()
for filename in filenames:
    basename = os.path.splitext(filename)[0]
    # Find just the basename
    basename = basename.replace('_unlabeled', '').replace('_data', '')
    job_keys.add(basename)

# 2) For all the possible job keys e.g. set-a, set-b, 3hb-coa, etc
#    open the files, get the data and run job
#    ignore job keys from random files that do not have the _unlabeled and _data
valid_jobs = set()
for job_key in job_keys:
    # Check that there exists <job_key>_unlabeled AND <job_key>_data
    unlabeled_fname = '{0}_unlabeled.csv'.format(job_key)
    data_fname = '{0}_data.csv'.format(job_key)
    # TODO maybe check for both .txt and .csv above for robustness
    if unlabeled_fname in filenames and data_fname in filenames:
        valid_jobs.add(job_key)

# 3) For each job  in valid_jobs, load into numpy, do analyis, write result
for job_key in valid_jobs:
    unlabeled_fname = '{0}_unlabeled.csv'.format(job_key)
    data_fname = '{0}_data.csv'.format(job_key)

    # Call function from tracerutils to prepare unlabeled data from CSV (or web)
    # Cleans up trailing commas, non numbers, etc
    text_from_unlabeled_file = open(unlabeled_fname).read()
    unlabeled = prepare_unlabeled_for_analysis(text_from_unlabeled_file)

    # Call function from tracerutils to prepare data from CSV (or web)
    # for analysis. Needs to strip trailing commas, fix non numbers etc.
    text_from_data_file = open(data_fname).read()    
    data = prepare_data_for_analysis(text_from_data_file)

    #print('averages:', averages)
    print('data:', data)

    result = do_tracer_analysis(data, unlabeled)
    
    # print to a file
    output_fname = '{0}_output.csv'.format(job_key)
    np.savetxt(output_fname, result, fmt='%.1f', delimiter=',')
