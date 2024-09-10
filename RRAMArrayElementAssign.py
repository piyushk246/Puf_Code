import pandas as pd
import math

class RRAMArrayElementAssign:
    def __init__(self, excel_path, usecols='B', skiprows=None):
        self.excel_path = excel_path
        self.usecols = usecols
        self.skiprows = skiprows if skiprows is not None else []
        self.data = None

    def load_data(self):
        # Read the Excel file and extract data as a flattened array
        df = pd.read_excel(self.excel_path, usecols=self.usecols, skiprows=self.skiprows)
        self.data = df.to_numpy().flatten()

    def populate(self, rram_array):
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() before populating the array.")
        
        index = 0
        for i in range(rram_array.rows):
            for j in range(rram_array.columns):
                if index < len(self.data):
                    rram_array.set_value(i, j, self.data[index])
                    index += 1
                else:
    
                    break
    def populate_with_blocks(self, rram_array, num_blocks):
        """
        Populates the RRAM array by dividing it into the specified number of blocks
        and assigning data to each block.

        Parameters:
        - rram_array: The RRAM array object with 'rows', 'columns', and 'set_value' method.
        - num_blocks: The number of blocks to divide the array into.
        """
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() before populating the array.")
        
        if num_blocks <= 0:
            raise ValueError("Number of blocks must be a positive integer.")
        
        total_elements = rram_array.rows * rram_array.columns
        block_size = math.ceil(total_elements / num_blocks)

        index = 0
        for block in range(num_blocks):
            for i in range(rram_array.rows):
                for j in range(rram_array.columns):
                    if index < (block + 1) * block_size and index < len(self.data):
                        rram_array.set_value(i, j, self.data[index])
                        index += 1
                    elif index < (block + 1) * block_size:
                        # If data is insufficient, you can decide to set a default value or repeat data
                        rram_array.set_value(i, j, self.data[index % len(self.data)])
                        index += 1
            # Optionally, you can add block-specific operations here

        # If there are remaining elements after assigning all blocks
        while index < total_elements:
            i = index // rram_array.columns
            j = index % rram_array.columns
            rram_array.set_value(i, j, self.data[index % len(self.data)])
            index += 1
                

# Example usage
# populator = RRAMArrayElementAssign(r'C:\Users\Piyush\Desktop\sem3\PUF\Code\fig5(b).xlsx', usecols='B', skiprows=[1, 2])

# # Load the data from the Excel sheet
# populator.load_data()

# print("All is the done")