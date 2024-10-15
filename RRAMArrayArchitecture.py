import pandas as pd
import numpy as np
import math
import random
# import scipy.sparse as sparse
import os

class RRAMArrayArchitecture:
    def __init__(self, rows, columns, filename='array.dat'):
        self.rows = rows
        self.columns = columns
        # self.array = np.memmap(filename, dtype='float32', mode='w+', shape=(rows, columns))
        self.array = [[None for _ in range(columns)] for _ in range(rows)]

    def display_architecture(self):
        print(f"RRAM Array Architecture: {self.rows} x {self.columns} (Rows x Columns)\n")
        for row in self.array:
            print(row)

    def get_array(self):
        return self.array
    
    def set_value(self, row, col, value):
        if 0 <= row < self.rows and 0 <= col < self.columns:
            self.array[row][col] = value
        else:
            print("Error: Row or column is out of bounds.")


# class RRAMArrayElementAssign:
#     def __init__(self, excel_path, usecols, skiprows=None):
#         self.excel_path = excel_path
#         self.usecols = usecols
#         self.skiprows = skiprows if skiprows is not None else []
#         self.data = None


#     def load_data_shuffle (self):
#         # Read the Excel file and extract data as a flattened array
#         df = pd.read_excel(self.excel_path, usecols=self.usecols, skiprows=self.skiprows)
#         self.data = df.to_numpy().flatten()
#         random.shuffle(self.data)

#     def load_data(self):
#         # Read the Excel file and extract data as a flattened array
#         df = pd.read_excel(self.excel_path, usecols=self.usecols, skiprows=self.skiprows)
#         self.data = df.to_numpy().flatten()

#     def populate_wo(self, rram_array):
#         if self.data is None:
#             raise ValueError("Data not loaded. Call load_data() before populating the array.")
        
#         index = 0
#         for i in range(rram_array.rows):
#             for j in range(rram_array.columns):
#                 if index < len(self.data):
#                     rram_array.set_value(i, j, self.data[index])
#                     index += 1
#                 else:
#                     break
                
#     def populate(self, rram_array):
#         if self.data is None:
#             raise ValueError("Data not loaded. Call load_data() before populating the array.")
        
#         index = 0
#         data_length = len(self.data)
#         for i in range(rram_array.rows):
#             for j in range(rram_array.columns):
#                 # Use modulus to repeat data from the beginning if needed
#                 rram_array.set_value(i, j, self.data[index % data_length])
#                 index += 1
                
#     def populate_with_blocks(self, rram_array, num_blocks):
#         if self.data is None:
#             raise ValueError("Data not loaded. Call load_data() before populating the array.")
        
#         if num_blocks <= 0:
#             raise ValueError("Number of blocks must be a positive integer.")
        
#         data_length = len(self.data)
#         total_elements = rram_array.rows * rram_array.columns
#         block_size = total_elements // num_blocks

#         # Create a list to store the 2D arrays (blocks)
#         blocks = [np.zeros((rram_array.rows, rram_array.columns), dtype=object) for _ in range(num_blocks)]
#         data_index = 0

#         for block_num in range(num_blocks):
#             for i in range(rram_array.rows):
#                 for j in range(rram_array.columns):
#                     if block_num * block_size + (i * rram_array.columns + j) < (block_num + 1) * block_size:
#                         blocks[block_num][i][j] = self.data[data_index % data_length]
#                         data_index += 1

#         # Fill any remaining cells in each block by wrapping around
#         for block_num in range(num_blocks):
#             for i in range(rram_array.rows):
#                 for j in range(rram_array.columns):
#                     if blocks[block_num][i][j] == 0:
#                         blocks[block_num][i][j] = self.data[data_index % data_length]
#                         data_index += 1

#         return blocks
    
#     def populate_with_random_data(self, rram_array, num_blocks):
#         if self.data is None:
#             raise ValueError("Data not loaded. Call load_data() before populating the array.")
        
#         if num_blocks <= 0:
#             raise ValueError("Number of blocks must be a positive integer.")
        
#         data_length = len(self.data)
#         total_elements = rram_array.rows * rram_array.columns
#         block_size = total_elements // num_blocks

#         # Create a list to store the 2D arrays (blocks)
#         blocks = [np.zeros((rram_array.rows, rram_array.columns), dtype=object) for _ in range(num_blocks)]
#         data_index = 0

#         for block_num in range(num_blocks):
#             for i in range(rram_array.rows):
#                 for j in range(rram_array.columns):
#                     if block_num * block_size + (i * rram_array.columns + j) < (block_num + 1) * block_size:
#                         blocks[block_num][i][j] = self.data[data_index % data_length]
#                         data_index += 1
#         return blocks
    
    

class RRAMArrayElementAssign:
    def __init__(self, file_path, usecols, skiprows=None):
        self.file_path = file_path
        self.usecols = usecols
        self.skiprows = skiprows if skiprows is not None else []
        self.data = None

    def load_data_shuffle(self):
        self.load_data()
        random.shuffle(self.data)

    def load_data(self):
        # Determine the file type based on the file extension
        file_extension = os.path.splitext(self.file_path)[1].lower()

        # print(file_extension)
        
        if file_extension == '.xlsx' or file_extension == '.xls':
            # Read the Excel file
            df = pd.read_excel(self.file_path, usecols=self.usecols, skiprows=self.skiprows)
        elif file_extension == '.csv':
            # Read the CSV file
            df = pd.read_csv(self.file_path, usecols=self.usecols, skiprows=self.skiprows)
        else:
            raise ValueError("Unsupported file type. Please use an Excel or CSV file.")

        self.data = df.to_numpy().flatten()

    def populate_wo(self, rram_array):
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
                
    def populate(self, rram_array):
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() before populating the array.")
        
        index = 0
        data_length = len(self.data)
        for i in range(rram_array.rows):
            for j in range(rram_array.columns):
                # Use modulus to repeat data from the beginning if needed
                rram_array.set_value(i, j, self.data[index % data_length])
                index += 1
                
    def populate_with_blocks(self, rram_array, num_blocks):
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() before populating the array.")
        
        if num_blocks <= 0:
            raise ValueError("Number of blocks must be a positive integer.")
        
        data_length = len(self.data)
        total_elements = rram_array.rows * rram_array.columns
        block_size = total_elements // num_blocks

        # Create a list to store the 2D arrays (blocks)
        blocks = [np.zeros((rram_array.rows, rram_array.columns), dtype=object) for _ in range(num_blocks)]
        data_index = 0

        for block_num in range(num_blocks):
            for i in range(rram_array.rows):
                for j in range(rram_array.columns):
                    if block_num * block_size + (i * rram_array.columns + j) < (block_num + 1) * block_size:
                        blocks[block_num][i][j] = self.data[data_index % data_length]
                        data_index += 1

        # Fill any remaining cells in each block by wrapping around
        for block_num in range(num_blocks):
            for i in range(rram_array.rows):
                for j in range(rram_array.columns):
                    if blocks[block_num][i][j] == 0:
                        blocks[block_num][i][j] = self.data[data_index % data_length]
                        data_index += 1

        return blocks
    
    def populate_with_random_data(self, rram_array, num_blocks):
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() before populating the array.")
        
        if num_blocks <= 0:
            raise ValueError("Number of blocks must be a positive integer.")
        
        data_length = len(self.data)
        total_elements = rram_array.rows * rram_array.columns
        block_size = total_elements // num_blocks

        # Create a list to store the 2D arrays (blocks)
        blocks = [np.zeros((rram_array.rows, rram_array.columns), dtype=object) for _ in range(num_blocks)]
        data_index = 0

        for block_num in range(num_blocks):
            for i in range(rram_array.rows):
                for j in range(rram_array.columns):
                    if block_num * block_size + (i * rram_array.columns + j) < (block_num + 1) * block_size:
                        blocks[block_num][i][j] = self.data[data_index % data_length]
                        data_index += 1
        return blocks

    

# if __name__ == "__main__":
#     # Example usage
#     # assigner = RRAMArrayElementAssign(r'C:\Users\Piyush\Desktop\sem3\PUF\Puf_Code\fig5(b).xlsx', usecols='B', skiprows=[1, 2])
#     assigner = RRAMArrayElementAssign(r'./testLogic/datasulff.csv', usecols=[0], skiprows=[0, 1])
#     # Load the data from the Excel sheet
#     assigner.load_data()
#     # assigner.load_data_shuffle()
#     rram = RRAMArrayArchitecture(8, 8) # for the 64 bits

#     assigner.populate(rram)
    
#     rram.display_architecture()
    # array = rram.get_array()
    # print("Returned Array:")
    # print(array)

# #input the row and columns
# row = int(input("Enter the row: "))
# columns = int(input("Enter the columns: "))

# # Example usage
# rram = RRAMArrayArchitecture(row, columns)
# rram.display_architecture()

# rram = RRAMArrayArchitecture(262144, 262144) # for the 64 bits

# rram = RRAMArrayArchitecture(16, 16)
# rram.display_architecture()

# array = rram.get_array()
# print("Returned Array:")
# print(array)

# assigner = RRAMArrayElementAssign(r'C:\Users\Piyush\Desktop\sem3\PUF\Code\fig5(b).xlsx', usecols='B', skiprows=[1, 2])

# Load the data from the Excel sheet
# assigner.load_data()

# assigner.populate(rram)

# array = rram.get_array()
# column_names = [f'BL_{i+1}' for i in range(len(array[0]))]
# index_names = [f'WL_{i+1}' for i in range(len(array[0]))]

# # print(column_names)   
# df = pd.DataFrame(array,columns=column_names,index=index_names)
# df.to_excel('output.xlsx')

# rram.set_value(2, 2, 3)
# rram.display_architecture()

# array_= assigner.populate_with_blocks(rram, num_blocks=2)

# print("\tarray_0\n",array_[0])
# print("\tarray_1\n",array_[1])
# populator.populate(rram)

# rram.display_architecture()