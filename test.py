import numpy as np
import sys

def parse_instance():
    # Read the input from stdin
    lines = sys.stdin.readlines()

    # Extract the row and column values
    row_values = np.array([int(x) for x in lines[0].split()[1:]])
    column_values = np.array([int(x) for x in lines[1].split()[1:]])

    # Extract the number of hints
    num_hints = int(lines[2])

    # Extract the hints and store them in a numpy array
    hints = np.zeros(num_hints, dtype=object)
    for i in range(num_hints):
        hint_line = lines[i + 3].split()
        hints[i] = np.array([int(hint_line[1]), int(hint_line[2]), hint_line[3]])

    return row_values, column_values, hints

# Testing the function
rows, columns, hints = parse_instance()
print("Rows:", rows)
print("Columns:", columns)
print("Hints:", hints)
print(hints[1])