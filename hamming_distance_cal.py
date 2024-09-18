import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast

class HammingDistanceCalculator:        

    def __init__(self, csv_path, usecols=None, skiprows=1):
        self.csv_path = csv_path
        self.usecols = usecols if usecols is not None else [1]  
        self.skiprows = skiprows if skiprows is not None else []
        self.data = None
        # Read the CSV file and extract data from the specified column
        df = pd.read_csv(self.csv_path, usecols=self.usecols, skiprows=self.skiprows)
        self.data = df.iloc[:, 0].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x).tolist()
        
        # print(self.data[0])
        # print(self.data) 


    def hamming_distance(self, response1, response2):
        # response1_bin = f'{response1:032b}'  # 32-bit binary format
        # response2_bin = f'{response2:032b}'  # 32-bit binary format
        return sum(r1 != r2 for r1, r2 in zip(response1, response2))
    
    # def hd_calculator(self):
    #     ham_dis = []
    #     # for i in range(len(self.data)):
    #     #     for j in range(i+1, len(self.data)):
    #     #         hamming_dist = self.hamming_distance(self.data[i], self.data[j])
    #     #         ham_dis.append(hamming_dist)  # Append inside the loop

    #     for i in range(100):
    #         for j in range(i+1, 100):
    #             hamming_dist = self.hamming_distance(self.data[i], self.data[j])
    #             ham_dis.append(hamming_dist)  # Append inside the loop
    #     return ham_dis
            
    def inter_chip(self):
        distances = []
        # pufs = len(self.data)
        pufs = 6000
        s = 0

        # Ensure the binary_responses are in a NumPy array format
        responses = np.asarray(self.data)

        # Calculate Hamming distances between all pairs of responses
        for i in range(pufs - 1):
            for j in range(i + 1, pufs):
                dist = self.hamming_distance(responses[i], responses[j])
                s += dist
                distances.append(dist)

        # Calculate inter-chip Hamming distance (in percentage form)
        inter_hd = (2 * s * 100) / (pufs * (pufs - 1) * len(responses[0]))

        # Normalize distances to percentage form
        distances = [(dist * 100 / len(responses[0])) for dist in distances]

        # Save distances to an Excel file
        # df_dis = pd.DataFrame(distances)
        # df_dis.to_excel('dis.xlsx', index=False)

        # Print statistics
        print("Inter-chip Hamming distance is:", inter_hd)
        # print("Distances:", distances)
        print("Standard deviation:", np.std(distances))
        print("Total pairs:", len(distances))
        print("Minimum distance:", min(distances))
        print("Maximum distance:", max(distances))

        # Plotting the histogram
        # plt.figure(figsize=(8, 6))  # Specify figure size
        # plt.xlim(0, 30)  # Set limits for the x-axis
        plt.yticks(weight='bold', fontsize=12)  # Customize y-axis ticks



        # Customize the title and labels
        plt.title('Hamming Distance Time Multiplexing', fontweight='bold', fontsize=12)
        plt.xlabel('Hamming Distance', fontweight='bold', fontsize=14)
        plt.ylabel('Frequency', fontweight='bold', fontsize=14)

        # Plot histogram for Hamming distances
        plt.hist(distances, bins=64, edgecolor='k', alpha=0.7, label='LRS')

        # Add legend
        plt.legend(fontsize=14)

        # Uncomment the following line if you want to save the plot
        # plt.savefig('./results/HD/HD_diff(LRS).png', format='PNG', dpi=300)
        # plt.savefig('./results/HD/HD_diff(HRS).png', format='PNG', dpi=300)
        plt.savefig('./results/HD/HD_same(LRS).png', format='PNG', dpi=300)
        # plt.savefig('./results/HD/HD_same(HRS).png', format='PNG', dpi=300)
        plt.tight_layout()
        # Show the plot
        plt.show()

        # return distances
            
    def inter_hd(self):
        pass
        
if __name__ == "__main__":
    # Assuming the second column in the CSV (index 1)
    # hd_calculator = HammingDistanceCalculator(r'./results/same(HRS)_ch16_rsp_32.csv', usecols=[1])
    hd_calculator = HammingDistanceCalculator(r'./results/same(LRS)_ch16_rsp_32.csv', usecols=[1])
    # hd_calculator = HammingDistanceCalculator(r'./results/diff(LRS)_ch16_rsp_32.csv', usecols=[1])
    # hd_calculator = HammingDistanceCalculator(r'./results/diff(HRS)_ch16_rsp_32.csv', usecols=[1])
    # hd_calculator = HammingDistanceCalculator(r'./unused/output.csv', usecols=[1])
    
    hd_calculator.inter_chip()
    # print(hd)
    

    


    