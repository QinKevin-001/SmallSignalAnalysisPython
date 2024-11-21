import matplotlib  # Import matplotlib first
matplotlib.use('Agg')  # Use non-GUI backend

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
# Adjust pandas display options
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', 1000)  # Set a wider display width
pd.set_option('display.max_colwidth', None)  # Don't truncate column content
pd.set_option('display.precision', 12)

def percDiff():
    # Function to calculate percentage difference for complex numbers
    def percentage_difference_complex(value1, value2):
        magnitude1 = np.abs(value1)
        magnitude2 = np.abs(value2)
        return 100 * abs((magnitude1 - magnitude2) / ((magnitude1 + magnitude2) / 2))

    # Convert columns to complex numbers safely and clean up terms
    def safe_complex(value):
        try:
            value = str(value).replace('i', 'j')  # Replace 'i' with 'j' for Python compatibility
            complex_value = complex(value)  # Convert to a complex number
            real_part = complex_value.real
            imag_part = complex_value.imag

            # Remove zero parts from the representation
            if real_part == 0 and imag_part != 0:
                return complex(0, imag_part)
            elif imag_part == 0 and real_part != 0:
                return complex(real_part, 0)
            return complex_value
        except (ValueError, TypeError):
            return np.nan  # Assign NaN for malformed strings

    # Read the CSV file into a DataFrame
    file_path = 'MvP.csv'  # Replace with your actual file path
    data = pd.read_csv(file_path)

    # Specify the columns to compare
    column1 = 'Matlab'  # Replace with your first column name
    column2 = 'Python'  # Replace with your second column name

    # Ensure the columns exist in the DataFrame
    if column1 not in data.columns or column2 not in data.columns:
        raise ValueError(f"Columns {column1} and/or {column2} not found in the CSV file.")

    # Convert columns to complex numbers using safe_complex()
    data[column1] = data[column1].apply(safe_complex)
    data[column2] = data[column2].apply(safe_complex)

    # Drop rows with invalid complex numbers (NaN or non-convertible)
    data = data.dropna(subset=[column1, column2])

    # Calculate the percentage difference for each corresponding point
    percentage_diff = percentage_difference_complex(data[column1], data[column2])

    # Plotting the percentage difference
    plt.figure(figsize=(10, 6))
    plt.plot(percentage_diff, label='Percentage Difference', marker='o')
    plt.xlabel('Index')
    plt.ylabel('Percentage Difference (%)')
    plt.title('Percentage Difference (Magnitude) between Two Columns of Complex Numbers')
    plt.legend()
    plt.grid(True)

    # Save the plot to a file
    output_plot = 'percentage_difference_complex_plot.png'
    plt.savefig(output_plot)
    print(f"Percentage difference plot saved as {output_plot}")

    # Generate a list of percentage differences
    percentage_diff_list = percentage_diff.tolist()

    # Sort the list from largest to smallest
    sorted_percentage_diff = sorted(percentage_diff_list, reverse=True)

    # Display the results
    #print("Original Percentage Differences:")
    #print(percentage_diff_list)

    #print("\nSorted Percentage Differences (Largest to Smallest):")
    #print(sorted_percentage_diff)

    # Optional: Create a DataFrame to display sorted differences with indices and corresponding values
    comparison_df = pd.DataFrame({
        'Index': range(len(percentage_diff_list)),
        'Percentage Difference (%)': percentage_diff_list,
        'Matlab': data[column1].tolist(),
        'Python': data[column2].tolist()
    }).sort_values(by='Percentage Difference (%)', ascending=False).reset_index(drop=True)

    # Display the updated DataFrame
    print("\nSorted DataFrame of Percentage Differences with Corresponding Values:")
    print(comparison_df)

if __name__ == "__main__":
    percDiff()