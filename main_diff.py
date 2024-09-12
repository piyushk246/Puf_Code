
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


def main_HRS(challenge_size):
    ref_res=8.1814
    x,y=row_col_bit(challenge_size)
    row = 2**x
    columns = row
    print("row:", row,"\ncolumns:" , row)

    rram = RRAMArrayArchitecture(row, columns)
    assigner = RRAMArrayElementAssign(r'C:\Users\Piyush\Desktop\sem3\PUF\Code\fig5(b).xlsx', usecols='B', skiprows=[1, 2])
    # Load the data from the Excel sheet
    assigner.load_data()

    # Populate the RRAM array with the data
    array= assigner.populate_with_blocks(rram, num_blocks=2)
    
    Puf = puf_design()
    challenge= [1,0,1,0,0,0,1,1,1,0,1,0,0,0,1,1]

    # def challenge_response(self, array,  ref_res, col_page, challenge, select_line, challenge_size, block):
    # def challenge_response_diff(self, array1, array2, ref_res, col_page, challenge, select_line, count):
    # challenges1, responses1 = Puf.challenge_response( array[0], ref_res,   64,    challenge,    10,      16,              1 )
    file_name = "./results/diff(HRS)_ch16_rsp"
    challenges2, responses1 = Puf.challenge_response_diff( array[0], array[1], ref_res,   64,    challenge,    10,      16,file_name)


                    # ploting without the matric  
    # plt.hist(responses1,bins=16,edgecolor='k', alpha=0.7,label='HRS')
    # plt.axhline(y=4096, color='r', linestyle='--', label='Ideal')
    # plt.title('Uniqueness of responses',fontweight='bold',fontsize=16 )
    # plt.xlabel('Responses',fontweight='bold',fontsize=14)
    # plt.ylabel('Frequency',fontweight='bold',fontsize=14)
    # plt.legend(fontsize=10)
    # plt.tight_layout()
    # plt.savefig('./results/diff16_c16r32_hrs(HRS).png',format = 'PNG' , dpi = 300)
    # plt.show()

                    #ploting with the matric
    ideal = 2048
    bin = 32
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
    plt.savefig(f'./results/diff{bin}_c16r32_hrs_metric(HRS).png',format = 'PNG' , dpi = 300)
    plt.show()  
    
def main_LRS(challenge_size):
    ref_res=4.43
    x,y=row_col_bit(challenge_size)
    row = 2**x
    columns = row
    print("row:", row,"\ncolumns:" , row)

    rram = RRAMArrayArchitecture(row, columns)

    
    assigner = RRAMArrayElementAssign(r'C:\Users\Piyush\Desktop\sem3\PUF\Code\fig5(b).xlsx', usecols='E', skiprows=[1, 2])

    # Load the data from the Excel sheet
    assigner.load_data()

    # Populate the RRAM array with the data
    array= assigner.populate_with_blocks(rram, num_blocks=2)
    
    
    Puf = puf_design()
    challenge= [1,0,1,0,0,0,1,1,1,0,1,0,0,0,1,1]
    # challenge_row, challenge_col = challenge[:10],challenge[10:]

    # challenge_row, challenge_col = [1,0,1,0,0],[0,1,1]
    # response1 = Puf.get_response(challenge_row, challenge_col, array[0], ref_res,  4)
    # print("challenge:",challenge,"response1: ",list(response1))
    
    
    # challenge.reverse()
    # challenge_row, challenge_col = challenge[:10],challenge[10:]

    # challenge_row, challenge_col = [1,0,1,0,0],[0,1,1]
    
    # response2 = Puf.get_response(challenge_row, challenge_col, array[1], ref_res,  4)
    # print("challenge:",challenge,"response2: ",list(response2))
    
    # response  = list(response1) +  list(response2)
    # print("respose_16bit:",response)

    # def challenge_response(self, array,  ref_res, col_page, challenge, select_line, challenge_size, block):
    # def challenge_response_diff(self, array1, array2, ref_res, col_page, challenge, select_line, count):
    # challenges1, responses1 = Puf.challenge_response( array[0], ref_res,   64,    challenge,    10,      16,              1 )
    file_name = "./results/diff(LRS)_ch16_rsp"
    challenges2, responses1 = Puf.challenge_response_diff( array[0], array[1], ref_res,   64,    challenge,    10,      16,file_name)
    
    
    # plt.hist(responses1,bins=16,edgecolor='k', alpha=0.7,label='LRS')
    
    ideal = 2048
    bin= 32
    counts, bins, bars = plt.hist(responses1, bins=bin, alpha=0.6, edgecolor='black',label='LRS')
    plt.axhline(y=ideal, color='r', linestyle='--', label=f'Ideal({ideal})')
    plt.title('Uniqueness of responses',fontweight='bold',fontsize=16 )
    plt.xlabel('Responses',fontweight='bold',fontsize=14)
    plt.ylabel('Frequency',fontweight='bold',fontsize=14)
    plt.bar_label(bars,fontsize=6)
    print(len(counts))
    msq_error  = np.sqrt(np.sum((ideal - counts)**2)/len(counts))        #root mean square error (RMSE)
    std_dev = np.std(responses1)        # Standard Deviation

    

    plt.text(0.4, 0.4, f'metric  = {msq_error :.2f}', 
         horizontalalignment='left', verticalalignment='top', 
         transform=plt.gca().transAxes, fontsize=8, color='k', weight='bold', 
         bbox=dict(facecolor='white', edgecolor='none', pad=3))

     
    # Display the legend
    plt.legend(loc='lower left', facecolor='white', edgecolor='black', fontsize=10)
    # plt.legend(fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'./results/diff{bin}_c16r32_hrs_metric(LRS).png',format = 'PNG' , dpi = 300)
    plt.show()
    

    # sum_deviation = sqrt(np.sum((1024 - counts)**2))
    


    
    # print("counts: ",counts)
    # print("bins: ",bins)
    # counts = np.array(counts)
    # print("counts: ",counts)
    
    # print((4096-counts))
    
    ####call the ploting function for the plot
     
    
    # print(responses1)
    # plotter = Plot(challenges1, responses1,challenge,8)
    # plotter.CRP()

    # print()
if __name__ == "__main__":
    challenge_size= 16
    
    main_LRS(challenge_size)
    main_HRS(challenge_size)
