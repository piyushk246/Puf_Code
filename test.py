import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, shapiro, probplot

# Load the data
df = pd.read_csv("matrix.csv").to_numpy().flatten()

# Calculate mean and standard deviation
mean = np.mean(df)
std = np.std(df)

# Print mean and standard deviation
print("Mean:", mean)
print("Standard Deviation:", std)

# Perform Shapiro-Wilk test for normality
shapiro_test = shapiro(df)
print("Shapiro-Wilk Test Statistic:", shapiro_test.statistic)
print("Shapiro-Wilk Test p-value:", shapiro_test.pvalue)

# Set up the figure and axes
fig, axs = plt.subplots(1, 2, figsize=(12, 6))

# Histogram
axs[0].hist(df, bins=10, edgecolor='k', density=True, alpha=0.6)
axs[0].set_title('Histogram with Gaussian Fit')
axs[0].set_xlabel('Data Values')
axs[0].set_ylabel('Density')

# Create a range of x values for the Gaussian plot
xmin, xmax = axs[0].get_xlim()  # Get the current x limits
x = np.linspace(xmin, xmax, 100)

# Calculate the Gaussian distribution
p = norm.pdf(x, mean, std)

# Plot the Gaussian curve
axs[0].plot(x, p, 'k', linewidth=2)

# Q-Q Plot
probplot(df, dist="norm", plot=axs[1])
axs[1].set_title('Q-Q Plot')

# Adjust layout and show the plots
plt.tight_layout()
plt.show()