import pandas as pd
import numpy as np
import random

# Load the Excel file
# df = pd.read_excel(r'./testLogic/data.xlsx',skiprows=1)
# df = pd.read_excel(r"C:\\Users\\Piyush\\Desktop\\sem3\\PUF\\RRAM_DATA\\generated_skewed_gaussian_data.xlsx")
df = pd.read_excel(r"./testLogic/generated_skewed_gaussian_data.xlsx")
# print(df    )

# Convert the DataFrame to a NumPy array and flatten it into a 1D list
x1 = df.to_numpy().flatten().tolist()

print("max:",max(x1))
print("min:",min(x1))


print("length of the all data ",len(x1))
# Shuffle the 1D list randomly
random.shuffle(x1)


# Print the results
print("This is the merged and shuffled data:")
print(len(x1))

data = pd.DataFrame({"res": x1})
# data.to_sql('data.db', con=engine, if_exists='replace', index=False)
# data.to_excel('./testLogic/datasulff.xlsx', index=False, header=False)
data.to_csv('./testLogic/datasulff.csv', index=False, header=False)
