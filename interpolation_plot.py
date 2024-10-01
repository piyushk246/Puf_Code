import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Load the CSV data into a DataFrame
df = pd.read_csv('interpolated_data.csv')  # Ensure the path to your file is correct

# Extract x and y values
x = df.iloc[:, 4]  # First column (x values)
y = df.iloc[:, 5]  # Second column (y values)

# Calculate the mean and standard deviation of y values
mean_y = np.mean(y)
std_dev_y = np.std(y, ddof=0)  # Population standard deviation; use ddof=1 for sample

print("Mean of Y:", mean_y)
print("Standard Deviation of Y:", std_dev_y)

# Generate a range of x values for plotting the CDF
x_range = np.linspace(mean_y - 4 * std_dev_y, mean_y + 4 * std_dev_y, 1000)

# Calculate the CDF values using the normal distribution
cdf_values = norm.cdf(x_range, loc=mean_y, scale=std_dev_y)



# Create the first plot for Y vs. X
plt.figure(0)
# plt.figure(figsize=(7, 6))
plt.plot(x, y, marker='', linestyle='-', color='b', label='Y vs. X')
# plt.axhline(mean_y, color='r', linestyle='--', label='Mean of Y')  # Add mean line
plt.title('Plot of Y vs. X')
plt.xlabel('X values at Voltage = -1.7V')
plt.ylabel('Y values')
# plt.grid()
plt.legend()
plt.savefig('YvsX.png',dpi=300)
# plt.show(block=True)  # Display without blocking

# Create the second plot for the CDF
plt.figure(1)
# plt.figure(figsize=(7, 6))
plt.plot(x_range, cdf_values, color='b', label='CDF of Y')
plt.axhline(0.5, color='r', linestyle='--', label='Mean of Y')  # Add mean line
plt.axvline(mean_y, color='r', linestyle='--', label='Mean of Y')  # Add mean line
plt.title('Cumulative Distribution Function (CDF) using Mean and Std Dev')
plt.xlabel('Y values')
plt.ylabel('Cumulative Probability')
plt.annotate(f'Mean: {mean_y:.2f}', xy=(mean_y, 0.5), xytext=(mean_y, 0.6), arrowprops=dict(facecolor='black', arrowstyle='->'))
# plt.grid()
plt.legend()
plt.savefig('CDF.png',dpi=300)
plt.show(block=True)  # Display without blocking


########################################################
##########all the interploated data plots###############
########################################################

# import pandas as pd
# import matplotlib.pyplot as plt

# # Load the CSV data into a DataFrame
# df = pd.read_csv('interpolated_data.csv')  # Adjust the file path as necessary

# # Plotting all x_new vs y_new pairs
# # plt.figure(figsize=(12, 8))

# # Loop through each pair of x_new and y_new
# for i in range(1, 9):  # Assuming you have 8 datasets as shown in the image
#     x_new = df[f'x_new{i}']  # Get the ith x_new column
#     y_new = df[f'y_new{i}']  # Get the ith y_new column
#     plt.plot(x_new, y_new, marker='', linestyle='-', label=f'Y{i}_new vs. X{i}')

# # Customize the plot
# plt.title('Plot of Y_new vs. X_new for Multiple Datasets')
# plt.xlabel('X_new values')
# plt.ylabel('Y_new values')
# # plt.axhline(0, color='gray', linestyle='--', linewidth=0.7)  # Optional: Add a horizontal line at y=0
# # plt.grid()
# plt.legend()
# # plt.tight_layout()
# plt.savefig('multiple_datasets.png',dpi=300)
# plt.show()

