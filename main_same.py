
from RRAMArrayArchitecture import RRAMArrayArchitecture
from RRAMArrayArchitecture import RRAMArrayElementAssign
from puf_design import puf_design
from plotting import Plot

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

def row_col_bit(a):
    b = math.log2(a)
    x = (b + a) / 2   
    y = a - x         
    print("Rounded x:", round(x))
    print("Rounded y:", round(y))
    return  round(x),round(y) 


def main_LRS(challenge_size):
    ref_res=4.43
    
    # #input the row and columns
    # row = int(input("Enter the row: "))
    # columns = int(input("Enter the columns: "))
    
    x,y=row_col_bit(challenge_size)
    row = 2**x
    columns = row
    print("row:", row,"\ncolumns:" , row)
    
    # # Create an instance of RRAMArrayArchitecture
    rram = RRAMArrayArchitecture(row, columns)
    
    
    # usecols='E' == LRS
    populator = RRAMArrayElementAssign(r'C:\Users\Piyush\Desktop\sem3\PUF\Code\fig5(b).xlsx', usecols='E', skiprows=[1, 2])

    # Load the data from the Excel sheet
    populator.load_data()

    # Populate the RRAM array with the data
    populator.populate(rram)
    
    # rram.display_architecture()
    array = rram.get_array()
    
    
    #             # 2 array store 
    # column_names = [f'BL_{i+1}' for i in range(len(array[0]))]
    # index_names = [f'WL_{i+1}' for i in range(len(array[0]))]
    # df = pd.DataFrame(array,columns=column_names,index=index_names)
    # df.to_excel('./Memory_1024(LRS).xlsx')
    

    Puf = puf_design()
    
    challenge= [1,0,1,0,0,0,1,1,1,0,1,0,0,0,1,1]
    # challenge_row, challenge_col = challenge[:5],challenge[5:]

    # # challenge_row, challenge_col = [1,0,1,0,0],[0,1,1]
    # response1 = Puf.get_response(challenge_row, challenge_col, array, ref_res,  4)
    # print("challenge:",challenge,"response1: ",list(response1))
    
    
    # challenge.reverse()
    # challenge_row, challenge_col = challenge[:10],challenge[10:]

    # # challenge_row, challenge_col = [1,0,1,0,0],[0,1,1]
    # # def get_response(self,challenge_row, challenge_col, rram_cell, ref_res, col_page):
    # response2 = Puf.get_response(challenge_row, challenge_col, array, ref_res,  64)
    # print("challenge:",challenge,"response2: ",list(response2))
    
    # response  = list(response1) +  list(response2)
    # print("respose_16bit:",response)

    # file_name = "diff_output_16bit(LRS)rsp"
    file_name = "./results/same(LRS)_ch16_rsp"
    #           def challenge_response         (self, array, ref_res,col_page,challenge,select_line,challenge_size, block,file_name):
    challenges1, responses1 = Puf.challenge_response_same( array, ref_res,   64,    challenge,    10,      16,              2 ,file_name)

    
    
                # ploting wihtout the matric
    # plt.hist(responses1,bins=16,edgecolor='k', alpha=0.7,label='LRS')
    # plt.axhline(y=4096, color='r', linestyle='--', label='Ideal')
    # plt.title('Uniqueness of responses',fontweight='bold',fontsize=16 )
    # plt.xlabel('Responses',fontweight='bold',fontsize=14)
    # plt.ylabel('Frequency',fontweight='bold',fontsize=14)
    # plt.legend(fontsize=20)
    # plt.tight_layout()
    # plt.savefig('./results/sam16_c16r32_hrs(LRS).png',format = 'PNG' , dpi = 300)
    # plt.show()

    ideal = 2048
    bin = 32
                
                # ploting with the matric
    counts, bins, bars = plt.hist(responses1, bins=bin, alpha=0.6, edgecolor='black',label='LRS')
    plt.axhline(y=ideal, color='r', linestyle='--', label='Ideal({ideal})')
    plt.title('Uniqueness of responses',fontweight='bold',fontsize=16 )
    plt.xlabel('Responses',fontweight='bold',fontsize=14)
    plt.ylabel('Frequency',fontweight='bold',fontsize=14)
    plt.bar_label(bars,fontsize=6)
    
    msq_error  = np.sqrt(np.sum((ideal - counts)**2)/len(counts))
    
    plt.text(0.4, 0.4, f'metric  = {msq_error :.2f}', 
         horizontalalignment='left', verticalalignment='top', 
         transform=plt.gca().transAxes, fontsize=8, color='k', weight='bold', 
         bbox=dict(facecolor='white', edgecolor='none', pad=3))
     
    # Display the legend
    plt.legend(loc='lower left', facecolor='white', edgecolor='black', fontsize=10)
    # plt.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'./results/sam{bin}_c16r32_hrs_metric(LRS).png',format = 'PNG' , dpi = 300)
    plt.show()

def main_HRS(challenge_size):
    ref_res=8.17
    
    x,y=row_col_bit(challenge_size)
    row = 2**x
    columns = row
    print("row:", row,"\ncolumns:" , row)
    
    # # Create an instance of RRAMArrayArchitecture
    rram = RRAMArrayArchitecture(row, columns)
    
    # usecols='E' == LRS
    populator = RRAMArrayElementAssign(r'C:\Users\Piyush\Desktop\sem3\PUF\Code\fig5(b).xlsx', usecols='B', skiprows=[1, 2])

    # Load the data from the Excel sheet
    populator.load_data()

    # Populate the RRAM array with the data
    populator.populate(rram)
    
    # rram.display_architecture()
    array = rram.get_array()
    
    
                # 2 array store 
    # column_names = [f'BL_{i+1}' for i in range(len(array[0]))]
    # index_names = [f'WL_{i+1}' for i in range(len(array[0]))]
    # df = pd.DataFrame(array,columns=column_names,index=index_names)
    # df.to_excel('./Memory_1024(HRS).xlsx')
    

    Puf = puf_design()
    
    challenge= [1,0,1,0,0,0,1,1,1,0,1,0,0,0,1,1]


    # file_name = "diff_output_16bit(LRS)rsp"
    file_name = "./results/same(HRS)_ch16_rsp"
    #           def challenge_response         (self, array, ref_res,col_page,challenge,select_line,challenge_size, block,file_name):
    challenges1, responses1 = Puf.challenge_response_same( array, ref_res,   64,    challenge,    10,      16,              2 ,file_name)

    #         #PLOTING WITHOUT THE MATRIC
    # plt.hist(responses1,bins=16,edgecolor='k', alpha=0.7,label='HRS')
    # plt.axhline(y=4096, color='r', linestyle='--', label='Ideal')
    # plt.title('Uniqueness of responses',fontweight='bold',fontsize=16 )
    # plt.xlabel('Responses',fontweight='bold',fontsize=14)
    # plt.ylabel('Frequency',fontweight='bold',fontsize=14)
    # plt.legend(fontsize=20)
    # plt.tight_layout()
    # plt.savefig('./results/sam16_c16r32_hrs(HRS).png',format = 'PNG' , dpi = 300)
    # plt.show()

    cr= Plot()
    cr.C_vs_R(challenges1, responses1)

    ideal = 2048
    bin = 32
            #PLOTING WITH THE MATRIC
    plt.figure(1)
    counts, bins, bars = plt.hist(responses1, bins=bin, alpha=0.6, edgecolor='black',label='HRS')
    plt.axhline(y=ideal, color='r', linestyle='--', label=f'Ideal({ideal})')
    plt.title('Uniqueness of responses',fontweight='bold',fontsize=16 )
    plt.xlabel('Responses',fontweight='bold',fontsize=14)
    plt.ylabel('Frequency',fontweight='bold',fontsize=14)
    plt.bar_label(bars,fontsize=6)
    
    msq_error  = np.sqrt(np.sum((ideal - counts)**2)/len(counts))
    
    plt.text(0.4, 0.4, f'metric  = {msq_error :.2f}', 
         horizontalalignment='left', verticalalignment='top', 
         transform=plt.gca().transAxes, fontsize=8, color='k', weight='bold', 
         bbox=dict(facecolor='white', edgecolor='none', pad=3))
     
    # Display the legend
    plt.legend(loc='lower left', facecolor='white', edgecolor='black', fontsize=10)
    # plt.legend(fontsize=10)
    
    plt.tight_layout()
    # plt.savefig(f'./results/sam{bin}_c16r32_hrs_metric(HRS).png',format = 'PNG' , dpi = 300)
    # plt.show() 
    
    
if __name__ == "__main__":
    challenge_size= 16
    
    # main_LRS(challenge_size)
    main_HRS(challenge_size)
    
    
