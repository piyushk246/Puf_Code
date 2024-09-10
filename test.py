import numpy as np
import pandas as pd
import h5py

class RRAMArrayArchitecture:
    def __init__(self, rows, columns, chunk_size=2048, filename='array.h5'):
        self.rows = rows
        self.columns = columns
        self.chunk_size = chunk_size
        self.filename = filename
        self.file = h5py.File(filename, 'w')
        # Create a dataset with chunked storage
        self.dataset = self.file.create_dataset(
            'array',
            (rows, columns),
            dtype='float32',
            chunks=(chunk_size, chunk_size),
            compression='gzip'
        )

    def set_value(self, row, col, value):
        if 0 <= row < self.rows and 0 <= col < self.columns:
            self.dataset[row, col] = value
        else:
            print("Error: Row or column is out of bounds.")

    def get_array(self):
        return self.dataset[:]
    
    def display_architecture(self):
        print(f"RRAM Array Architecture: {self.rows} x {self.columns} (Rows x Columns)")
        print(f"Chunk Size: {self.chunk_size} x {self.chunk_size}")
        print(f"Dataset Shape: {self.dataset.shape}")
        print(f"Compression: {self.dataset.compression}")
        
        # Display a preview of the array (top-left corner)
        preview_size = min(self.rows, 10)  # Preview top 10 rows or fewer if less than 10
        print("\nArray Preview (Top-Left Corner):")
        print(self.dataset[:preview_size, :preview_size])

    def close(self):
        self.file.close()

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

    # def populate(self, rram_array):
    #     if self.data is None:
    #         raise ValueError("Data not loaded. Call load_data() before populating the array.")
        
    #     index = 0
    #     for i in range(rram_array.rows):
    #         for j in range(rram_array.columns):
    #             if index < len(self.data):
    #                 rram_array.set_value(i, j, self.data[index])
    #                 index += 1
    #             else:
    #                 break
                
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

    def dump_to_h5(self, rram_array):
        # Ensure the data is loaded and the array is populated before dumping
        if self.data is None:
            raise ValueError("Data not loaded. Call load_data() before dumping to .h5 file.")
        rram_array.close()

# Example usage
rram = RRAMArrayArchitecture(262144, 262144, chunk_size=2048) 
populator = RRAMArrayElementAssign(r'C:\Users\Piyush\Desktop\sem3\PUF\Code\fig5(b).xlsx', usecols='B', skiprows=[1, 2])
populator.load_data()
populator.populate(rram)

# Dump the data into the .h5 file
populator.dump_to_h5(rram)

