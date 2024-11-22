import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# File path
file_path = 'MvP.csv'  # Update with the path to your file

# Function to calculate percentage difference for complex numbers
def percentage_difference_complex(value1, value2):
    magnitude1 = np.abs(value1)
    magnitude2 = np.abs(value2)
    # Avoid division by zero
    if (magnitude1 + magnitude2) == 0:
        return 0  # Define as 0% difference when both magnitudes are 0
    return 100 * abs((magnitude1 - magnitude2) / ((magnitude1 + magnitude2) / 2))

# Convert columns to complex numbers safely and clean up terms
def safe_complex(value):
    try:
        value = str(value).replace('i', 'j')  # Replace 'i' with 'j' for Python compatibility
        return complex(value)
    except (ValueError, TypeError):
        return np.nan  # Assign NaN for malformed strings

# Read the CSV file into a DataFrame
data = pd.read_csv(file_path)

# Specify the columns to compare
column1 = 'Matlab'
column2 = 'Python'

# Ensure the columns exist in the DataFrame
if column1 not in data.columns or column2 not in data.columns:
    raise ValueError(f"Columns {column1} and/or {column2} not found in the CSV file.")

# Convert columns to complex numbers using safe_complex()
data[column1] = data[column1].apply(safe_complex)
data[column2] = data[column2].apply(safe_complex)

# Drop rows with invalid complex numbers (NaN or non-convertible)
data = data.dropna(subset=[column1, column2])
if data.empty:
    raise ValueError("All rows have been dropped due to invalid data in the columns.")

# Calculate the percentage difference for each corresponding point
percentage_diff = data.apply(lambda row: percentage_difference_complex(row[column1], row[column2]), axis=1)

# Raw percentage differences list
percentage_diff_list_raw = percentage_diff.tolist()

# Clean the list (remove NaN values)
percentage_diff_list_clean = [x for x in percentage_diff_list_raw if not np.isnan(x)]

# Plotting the percentage difference
plt.figure(figsize=(10, 6))
plt.plot(percentage_diff, label='Percentage Difference', marker='o')
plt.xlabel('Index')
plt.ylabel('Percentage Difference (%)')
plt.title('Percentage Difference (Magnitude) between Two Columns of Complex Numbers')
plt.legend()
plt.grid(True)
output_plot = 'percentage_difference_complex_plot.png'
plt.savefig(output_plot)
