import numpy as np
import csv

def flatten_column_major(testResults):
    def recursive_flatten(item):
        """Recursively flatten nested lists and arrays."""
        if isinstance(item, list):
            return [sub_item for element in item for sub_item in recursive_flatten(element)]
        elif isinstance(item, np.ndarray):
            return recursive_flatten(item.tolist())
        else:
            return [item]

    # Calculate the maximum number of rows and columns in the testResults
    num_rows = len(testResults)
    max_cols = max(len(sublist) if isinstance(sublist, list) else 1 for sublist in testResults)

    # Use column-major logic to traverse and collect items
    flattened_list = []

    col = 0
    while col < max_cols:
        for row in range(num_rows):
            if col < len(testResults[row]):  # Add only if the current column exists in the row
                current_item = testResults[row][col]

                # Special handling for 'modalAnalysis' or nested lists/arrays
                if isinstance(current_item, (list, np.ndarray)):
                    # Traverse the sublist column-major
                    sub_rows = len(current_item)
                    sub_cols = max(
                        len(sub_item) if isinstance(sub_item, list) else 1
                        for sub_item in current_item
                    )

                    for sub_col in range(sub_cols):
                        for sub_row in range(sub_rows):
                            sub_item = current_item[sub_row]

                            # Check if sub_item is iterable and sub_col exists
                            if isinstance(sub_item, (list, np.ndarray)) and sub_col < len(sub_item):
                                deeper_item = sub_item[sub_col]

                                # Handle deeper nested structures like "Participation Factor"
                                if isinstance(deeper_item, (list, np.ndarray)):
                                    deeper_rows = len(deeper_item)
                                    deeper_cols = max(
                                        len(d_item) if isinstance(d_item, list) else 1
                                        for d_item in deeper_item
                                    )

                                    for deeper_col in range(deeper_cols):
                                        for deeper_row in range(deeper_rows):
                                            if isinstance(deeper_item[deeper_row], (list, np.ndarray)) and deeper_col < len(deeper_item[deeper_row]):
                                                flattened_list.extend(recursive_flatten(deeper_item[deeper_row][deeper_col]))
                                            elif deeper_col == 0:  # Include scalar values in the first column
                                                flattened_list.extend(recursive_flatten(deeper_item[deeper_row]))
                                else:
                                    flattened_list.extend(recursive_flatten(deeper_item))
                            elif sub_col == 0:  # Include scalar values in the first column
                                flattened_list.extend(recursive_flatten(sub_item))
                else:
                    flattened_list.extend(recursive_flatten(current_item))
        col += 1

    # Convert 1D list to nx1 list (column vector)
    column_vector = [[item] for item in flattened_list]

    # Filter to keep only numeric values (int, float, complex)
    numeric_column_vector = [
        [item[0]] for item in column_vector
        if isinstance(item[0], (int, float, complex))
    ]

    print("Flatten list:", column_vector)
    print("Flatten list:", len(column_vector))
    print("Output vector is:", numeric_column_vector)
    print("Output vector length is:", len(numeric_column_vector))
    unique_types = set(type(item[0]) for item in column_vector)
    print("Unique data types in the output list:", unique_types)
    unique_types2 = set(type(item[0]) for item in numeric_column_vector)
    print("Unique data types in the numeric output list:", unique_types2)

    # Save to CSV, formatting complex numbers as "a+bj"
    with open('python.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for row in numeric_column_vector:
            # Format complex numbers as "a+bj"
            formatted_row = [
                str(value).replace('(', '').replace(')', '') if isinstance(value, complex) else value
                for value in row
            ]
            csv_writer.writerow(formatted_row)

        print("Filtered and saved column vector to CSV.")

    return numeric_column_vector

