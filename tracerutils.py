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
