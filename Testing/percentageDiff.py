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

# Prompt the user until a valid case number (1-17 with optional decimals) or "test" is entered.
while True:
    case_input = input("Enter a case number (1-17 or with decimals, e.g. 1.1-1.9) or 'test' for temporary testing: ").strip().lower()

    if case_input == 'test':
        case_number = 'test'
        desc = "Test Case"
        file_case_str = "TestCase"
        break
    else:
        try:
            # Convert the input to a float to accept numbers like 1.1, 2.5, etc.
            case_value = float(case_input)
            # Accept only numbers from 1 up to (but not including) 18
            if 1 <= case_value < 18:
                # Set case_number as the float value (non-test)
                case_number = case_value
                # Use the integer part for mapping to a case description
                case_number_int = int(case_value)
                desc = case_mapping[case_number_int]
                # Format the file name:
                # If the input has a fractional part, include it; otherwise, use two-digit integer formatting.
                if case_value.is_integer():
                    file_case_str = f"{int(case_value):02d}"
                else:
                    frac_part = str(case_value).split('.')[1]
                    file_case_str = f"{case_number_int:02d}.{frac_part}"
                break
            else:
                print("Invalid input. Please enter a number between 1 and 17.9 (e.g. 1 or 1.5) or 'test'.")
        except ValueError:
            print("Invalid input. Please enter a valid number (e.g. 1, 1.5, etc.) or 'test'.")

# Define output file name and plot title based on the user input
if case_number != 'test':
    output_plot = f"Case{file_case_str} {desc}.png"
    plot_title = f"Case {file_case_str} Percentage Difference between Matlab and Python Data Points"
else:
    output_plot = "Test Case.png"
    plot_title = "Test Case Percentage Difference between Matlab and Python Data Points"

# File paths for the two CSV files
matlab_file = 'Matlab.csv'
python_file = 'Python.csv'

# Read Matlab.csv by skipping the extra header row (assuming the first row is an extra header)
matlab_data = pd.read_csv(matlab_file, skiprows=1, header=None, names=["Matlab"])

# Read Python.csv assuming it has no header row (adjust if necessary)
python_data = pd.read_csv(python_file, header=None, names=["Python"])

# Ensure both DataFrames have the same number of rows using the smaller length
min_len = min(len(matlab_data), len(python_data))
matlab_data = matlab_data.iloc[:min_len].reset_index(drop=True)
python_data = python_data.iloc[:min_len].reset_index(drop=True)

# Combine the two DataFrames side by side
data = pd.concat([matlab_data, python_data], axis=1)

# Function to safely convert a string to a complex number (replace 'i' with 'j')
def safe_complex(value):
    try:
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

# Function to calculate percentage and absolute error between two complex numbers
def compute_errors(a, b):
    mag_a = np.abs(a)
    mag_b = np.abs(b)
    abs_error = abs(mag_a - mag_b)
    if (mag_a + mag_b) == 0:
        percent_error = 0
    else:
        percent_error = 100 * abs_error / ((mag_a + mag_b) / 2)
    return percent_error, abs_error

# Apply the function to each row and store results
data[['Percent Error', 'Absolute Error']] = data.apply(
    lambda row: pd.Series(compute_errors(row['Matlab'], row['Python'])), axis=1
)

# --- Plot 1: Percentage Error ---
plt.figure(figsize=(10, 6))
plt.plot(data['Percent Error'], label='Percentage Error (%)', color='tab:blue', marker='o')
plt.xlabel('Index')
plt.ylabel('Percentage Error (%)')
plt.title(f"{plot_title} - Percentage Error")
plt.legend()
plt.grid(True)
plt.tight_layout()
percent_error_plot_file = output_plot.replace('.png', '_PercentageError.png')
plt.savefig(percent_error_plot_file)
plt.show()

# --- Plot 2: Absolute Error ---
plt.figure(figsize=(10, 6))
plt.plot(data['Absolute Error'], label='Absolute Error', color='tab:orange', marker='x')
plt.xlabel('Index')
plt.ylabel('Absolute Error')
plt.title(f"{plot_title} - Absolute Error")
plt.legend()
plt.grid(True)
plt.tight_layout()
absolute_error_plot_file = output_plot.replace('.png', '_AbsoluteError.png')
plt.savefig(absolute_error_plot_file)
plt.show()

# Save the error data to CSV
#csv_output_file = f"Case{file_case_str}_Errors.csv"
#data.to_csv(csv_output_file, index=False)

print(f"Percentage error plot saved as '{percent_error_plot_file}'")
print(f"Absolute error plot saved as '{absolute_error_plot_file}'")
#print(f"Error data saved as '{csv_output_file}'")
