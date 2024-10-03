import numpy as np

# Given values
start = 5.3
end = 9.3
steps = 1000

# Create an array with values from start to end divided into steps
values = np.linspace(start, end, steps)

# Simulating how it would look like in an Excel column format
for i, value in enumerate(values):
    print(f"A{i+1}: {value}:.2f ")

import pandas as pd

# Save the values into a CSV file
df = pd.DataFrame(values, columns=["Values"])
df.to_csv("values.csv", index_label="Index")
