# Usability issues
#  - Files must be correctly formed
#  - Files must have the .csv extension (note, allow also .txt)

import csv
import numpy as np
import os

from website.tracerutils import (
    do_tracer_analysis,
    prepare_data_for_analysis,
    prepare_unlabeled_for_analysis
)
    
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
