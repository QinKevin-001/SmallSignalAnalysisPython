import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Mapping of case numbers to descriptive names
case_mapping = {
    1: "Droop Simplified Infinite",
    2: "Droop Infinite",
    3: "Droop Plant Infinite",
    4: "GFL Infinite",
    5: "GFL Plant Infinite",
    6: "VSM Infinite",
    7: "VSM Plant Infinite",
    8: "Droop Droop",
    9: "Droop Plant Droop Plant",
    10: "Droop VSM",
    11: "Droop Plant VSM Plant",
    12: "VSM VSM",
    13: "VSM Plant VSM Plant",
    14: "Droop SG",
    15: "Droop Plant SG",
    16: "VSM SG",
    17: "VSM Plant SG"
}

# Prompt the user until a valid case number (1-17) is entered.
while True:
    try:
        case_number = int(input("Enter a case number (1-17): "))
        if 1 <= case_number <= 17:
            break
        else:
            print("Invalid input. Please enter a number between 1 and 17.")
    except ValueError:
        print("Invalid input. Please enter a valid integer between 1 and 17.")

# Create file name and title based on the user input
desc = case_mapping[case_number]
# File name: e.g., "Case01 Droop Simplified Infinite.png"
output_plot = f"Case{case_number:02d} {desc}.png"
# Plot title: e.g., "Case 01 Percentage Difference between Matlab and Python Data Points"
plot_title = f"Case {case_number:02d} Percentage Difference between Matlab and Python Data Points"

# File paths for the two CSV files
matlab_file = 'Matlab.csv'
python_file = 'Python.csv'

# Read Matlab.csv by skipping the extra header row.
# We assume the first row in Matlab.csv is the extra header ("Data").
matlab_data = pd.read_csv(matlab_file, skiprows=1, header=None, names=["Matlab"])

# Read Python.csv assuming it has no header row (adjust if necessary)
python_data = pd.read_csv(python_file, header=None, names=["Python"])

# Ensure both DataFrames have the same number of rows by using the smaller length
min_len = min(len(matlab_data), len(python_data))
matlab_data = matlab_data.iloc[:min_len].reset_index(drop=True)
python_data = python_data.iloc[:min_len].reset_index(drop=True)

# Combine the two DataFrames side by side
data = pd.concat([matlab_data, python_data], axis=1)

# Function to safely convert a string to a complex number (replace 'i' with 'j')
def safe_complex(value):
    try:
        # Remove any extra spaces and replace 'i' with 'j'
        value = str(value).strip().replace('i', 'j')
        return complex(value)
    except (ValueError, TypeError):
        return np.nan

# Convert the data in both columns to complex numbers
data['Matlab'] = data['Matlab'].apply(safe_complex)
data['Python'] = data['Python'].apply(safe_complex)

# Drop rows with invalid or missing complex numbers
data = data.dropna(subset=['Matlab', 'Python'])
if data.empty:
    raise ValueError("No valid data available for comparison after cleaning.")

# Function to calculate the percentage difference between two complex numbers
def percentage_difference_complex(a, b):
    mag_a = np.abs(a)
    mag_b = np.abs(b)
    # If both magnitudes are zero, define the difference as 0%
    if (mag_a + mag_b) == 0:
        return 0
    return 100 * abs((mag_a - mag_b) / ((mag_a + mag_b) / 2))

# Calculate the percentage difference for each row (point-to-point comparison)
percentage_diff = data.apply(lambda row: percentage_difference_complex(row['Matlab'], row['Python']), axis=1)

# Plot the percentage differences as a scatter plot with the user-defined title
plt.figure(figsize=(10, 6))
plt.scatter(range(len(percentage_diff)), percentage_diff, label='Percentage Difference')
plt.xlabel('Index')
plt.ylabel('Percentage Difference (%)')
plt.title(plot_title)
plt.legend()
plt.grid(True)
plt.savefig(output_plot)
plt.show()

print(f"Plot saved as '{output_plot}' with title '{plot_title}'.")
