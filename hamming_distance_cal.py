import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast

class HammingDistanceCalculator:        
    # def __init__(self, csv_path, usecols=None, skiprows=1):
    #     self.csv_path = csv_path
    #     self.usecols = usecols if usecols is not None else [1]  
    #     self.skiprows = skiprows if skiprows is not None else []
    #     self.data = None
    #     # Read the CSV file and extract data from the second column (index 1)
    #     df = pd.read_csv(self.csv_path, usecols=self.usecols, skiprows=self.skiprows)
    #     # self.data = df.to_numpy().flatten()
    #     # self.data = df.to_numpy()
    #     self.data = df.applymap(lambda x: ast.literal_eval(x) if isinstance(x, str) else x).to_numpy()
    #     # print(len(self.data[0][0]))
    #     # print(self.data[0][0])
    #     print(self.data)

    def __init__(self, csv_path, usecols=None, skiprows=1):
        self.csv_path = csv_path
        self.usecols = usecols if usecols is not None else [1]  
        self.skiprows = skiprows if skiprows is not None else []
        self.data = None
        # Read the CSV file and extract data from the specified column
        df = pd.read_csv(self.csv_path, usecols=self.usecols, skiprows=self.skiprows)
        self.data = df.iloc[:, 0].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x).tolist()
        # print(self.data)


    def hamming_distance(self, response1, response2):
        return sum(r1 != r2 for r1, r2 in zip(response1, response2))
    
    def hd_calculator(self):
        ham_dis = []
        for i in range(1,len(self.data)):
            hamming_dist =self.hamming_distance(self.data[i-1],self.data[i])
            # print(i,"Hamming Distance:", hamming_dist)
            ham_dis.append(hamming_dist)
        return ham_dis
            
            
    def inter_hd(self):
        pass
        
if __name__ == "__main__":
    
    # Assuming the second column in the CSV (index 1)
    # hd_calculator = HammingDistanceCalculator(r'./results/diff(HRS)_ch16_rsp_32.csv', usecols=[1])
    # hd_calculator = HammingDistanceCalculator(r'./results/same(HRS)_ch16_rsp_32.csv', usecols=[1])
    hd_calculator = HammingDistanceCalculator(r'./unused/output.csv', usecols=[2])
    # response1 = [1, 0, 1, 1]
    # response2 = [0, 1, 1, 0]
    # hamming_dist = hd_calculator.hamming_distance(response1, response2)
    # print("Hamming Distance:", hamming_dist)
    
    hd = hd_calculator.hd_calculator()
    # print(hd)
    
    plt.figure()
    #plotting inter chip hamming distance
    #plt.subplot(2, 2, 2)
    plt.xlim(0, 30)
    # ticks = np.arange(0, 100, 10)
    # labels = [f'{tick} ' for tick in ticks]
    # plt.xticks(ticks, labels,weight='bold',fontsize=12)
    
    plt.yticks(weight='bold',fontsize=12)
    plt.hist(hd, bins=16, edgecolor='k', alpha=0.7,label='HRS')
    # plt.title('Hamming Distance hardware multiplexing ',fontweight='bold',fontsize=12)
    plt.title('Hamming Distance Time multiplexing ',fontweight='bold',fontsize=12)
    plt.xlabel('Hamming Distance',fontweight='bold',fontsize=14)
    plt.ylabel('Frequency',fontweight='bold',fontsize=14)
    plt.legend(fontsize=14)
    # plt.savefig('./results/Hamming_Distance_diff(LRS).png',format = 'PNG' , dpi = 300)
    # plt.savefig('./Hamming_Distance_diff(HRS).png',format = 'PNG' , dpi = 300)
    # plt.savefig('./Hamming_Distance_same(HRS).png',format = 'PNG' , dpi = 300)
    plt.show()


    