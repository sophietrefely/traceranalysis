from io import StringIO
import numpy as np

from traceranalysis import do_tracer_analysis 

# Create text stream as though we loaded files
# of unlabeled, and labeled data
unlabeled_as_stream = StringIO("""\
8.20E+05    1.73E+05    6.91E+03    0.00E+00    0.00E+00    0.00E+00    0.00E+00
8.21E+05    1.70E+05    8.95E+03    0.00E+00    0.00E+00    0.00E+00    0.00E+00
8.09E+05    1.80E+05    1.12E+04    3.18E+02    2.17E+02    0.00E+00    0.00E+00\
""")

labeled_as_stream = StringIO("""\
5.05E+05    1.04E+05    3.44E+05    7.40E+04    1.24E+05    1.17E+04    1.63E+04
4.97E+05    1.07E+05    3.48E+05    7.79E+04    1.21E+05    5.54E+03    8.94E+03
5.81E+05    1.21E+05    4.11E+05    9.17E+04    1.37E+05    1.37E+04    1.69E+04\
""")

# Load them into numpy arrays using conveneitn loadtxt function
unlabeled_as_numpy_array = np.loadtxt(unlabeled_as_stream)
labeled_as_numpy_array = np.loadtxt(labeled_as_stream)

# Confirm they have the correct shapes on load
print('unlabeled shape:', unlabeled_as_numpy_array.shape)
print('labeled shape:', labeled_as_numpy_array.shape)

# Use our library to get the result
result = do_tracer_analysis(
    labeled_as_numpy_array, unlabeled_as_numpy_array
)

# Make printed array easy to read, suppres scientific notation
np.set_printoptions(precision=2, suppress=True)

# Print out results
print('Our result:')
print(result)
