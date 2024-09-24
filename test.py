import pandas as pd

class DataPopulator:
    def __init__(self, excel_path, skiprows=0):
        self.excel_path = excel_path
        self.skiprows = skiprows

    def populate_different_columns(self, rram_array, column_mapping):
        # Read the Excel file to get the correct column names
        df_all = pd.read_excel(self.excel_path, skiprows=self.skiprows)
        print("Available columns:", df_all.columns)

        for portion, col in column_mapping.items():
            if col not in df_all.columns:
                raise ValueError(f"Column '{col}' not found in the Excel file")

            # Load data for the specific column
            df = pd.read_excel(self.excel_path, usecols=[df_all.columns.get_loc(col)], skiprows=self.skiprows)
            data = df.to_numpy().flatten()

            # Determine where to populate this data based on the portion
            sub_array_size = (rram_array.rows * rram_array.columns) // len(column_mapping)
            start_index = portion * sub_array_size
            end_index = start_index + len(data)

            # Populate the array in the specified portion
            index = 0
            for j in range(rram_array.columns):
                for i in range(rram_array.rows):
                    array_index = j * rram_array.rows + i
                    if start_index <= array_index < end_index and index < len(data):
                        rram_array.set_value(i, j, data[index])
                        index += 1
                    elif array_index >= end_index:
                        break

# Example usage
class RRAMArray:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.array = [[0 for _ in range(columns)] for _ in range(rows)]

    def set_value(self, row, col, value):
        self.array[row][col] = value

# Initialize the RRAM array
rram_array = RRAMArray(4, 4)

# Define the column mapping (portion: column index)
column_mapping = {0: "A", 1: "B", 2: "C", 3: "D"}

# Create an instance of DataPopulator and populate the array
data_populator = DataPopulator('./data.xlsx')
data_populator.populate_different_columns(rram_array, column_mapping)

# Print the populated array
for row in rram_array.array:
    print(row)
