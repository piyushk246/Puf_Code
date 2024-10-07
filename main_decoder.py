
from RRAMArrayArchitecture import RRAMArrayArchitecture
from RRAMArrayArchitecture import RRAMArrayElementAssign
from puf_design import puf_design
# from plotting import Plot

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

def row_col_bit(a):
    b = math.log2(a)
    x = (b + a) / 2   
    y = a - x         
    # print("Rounded x:", round(x))
    # print("Rounded y:", round(y))
    return  round(x),round(y) 

def main_LRS(challenge_size):

    ref_res=4.43

    x,y=row_col_bit(challenge_size)
    row = 2**(x+1)
    columns = row
    col_page = 2**(y-1)

    select_line = x+1
    print("row:", row,"\ncolumns:" , row)
    
    # # Create an instance of RRAMArrayArchitecture
    rram = RRAMArrayArchitecture(row, columns)
    
    # usecols='E' == LRS
    populator = RRAMArrayElementAssign(r'fig5(b).xlsx', usecols='E', skiprows=[1, 2])

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
    file_name = "./results/deco(LRS)_ch16_rsp"
    #         def Dec0_challenge_2response(self, array,  ref_res, col_page, challenge_len, select_line, count, block,file_name):
    # challenges1, responses1 = Puf.Decoder_challenge_2response( array, ref_res,  col_page,    challenge_len= 16,    select_line=11,      count = 16, file_name = file_name )
    challenges1, responses1 = Puf.Decoder_challenge_2response(array = array,  ref_res = ref_res, col_page =32, challenge_len =16, select_line = 11, count= 16, file_name = file_name)
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

    # cr= Plot()
    # cr.C_vs_R(challenges1, responses1)


    ideal = 2048
    bin = 32
            #PLOTING WITH THE MATRIC
    plt.figure(0)
    counts, bins, bars = plt.hist(responses1, bins=bin, alpha=0.6, edgecolor='black',label='LRS')
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
    plt.savefig(f'./results/UniqueResp/deco{bin}_c16r32_lrs_metric(LRS).png',format = 'PNG' , dpi = 300)
    
    plt.figure(1)
    # ticks = np.arange(0, 16, 1)
    # labels = [f'{tick} ' for tick in ticks]
    # plt.xticks(ticks, labels,weight='bold')
    # plt.ylim(0, 16)
    # labels1 = [f'{tick} ' for tick in ticks]
    # plt.yticks(ticks, labels1,weight='bold')
    plt.plot(challenges1,responses1,'o',markersize=0.4,color='blue',label='LRS')
    plt.title('Relation between challenge and response',fontweight='bold',fontsize=16)
    plt.xlabel('Challenge',fontweight='bold',fontsize=14)
    plt.ylabel('Response',fontweight='bold',fontsize=14)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig('./results/ChaRes/deco_LRS_ch_rsp.png',format = 'PNG' , dpi = 300)
    
    plt.show() 
    

def main_HRS(challenge_size):

    ref_res=8.17
    x,y=row_col_bit(challenge_size)
    row = 2**(x+1)
    columns = row
    col_page = 2**(y-1)

    select_line = x+1
    print("row:", row,"\ncolumns:" , row)
    
    # # Create an instance of RRAMArrayArchitecture
    rram = RRAMArrayArchitecture(row, columns)
    
    # usecols='E' == LRS
    populator = RRAMArrayElementAssign(r'fig5(b).xlsx', usecols='B', skiprows=[1, 2])

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
    file_name = "./results/deco(HRS)_ch16_rsp"
    #         def Dec0_challenge_2response(self, array,  ref_res, col_page, challenge_len, select_line, count, block,file_name):
    # challenges1, responses1 = Puf.Dec0_challenge_2response( array, ref_res,  col_page,    challenge_len= 16,    select_line=11,      count = 16, file_name = file_name )
    challenges1, responses1 = Puf.Decoder_challenge_2response(array = array,  ref_res = ref_res, col_page =32, challenge_len =16, select_line = 11, count= 16, file_name = file_name)

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

    # cr= Plot()
    # cr.C_vs_R(challenges1, responses1)


    ideal = 2048
    bin = 32
            #PLOTING WITH THE MATRIC
    plt.figure(0)
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
    plt.savefig(f'./results/UniqueResp/deco{bin}_c16r32_hrs_metric(HRS).png',format = 'PNG' , dpi = 300)
    
    plt.figure(1)
    # ticks = np.arange(0, 16, 1)
    # labels = [f'{tick} ' for tick in ticks]
    # plt.xticks(ticks, labels,weight='bold')
    # plt.ylim(0, 16)
    # labels1 = [f'{tick} ' for tick in ticks]
    # plt.yticks(ticks, labels1,weight='bold')
    plt.plot(challenges1,responses1,'o',markersize=0.4,color='#F81506',label='HRS')
    plt.title('Relation between challenge and response',fontweight='bold',fontsize=16)
    plt.xlabel('Challenge',fontweight='bold',fontsize=14)
    plt.ylabel('Response',fontweight='bold',fontsize=14)
    plt.legend(fontsize=12)
    plt.tight_layout()
    plt.savefig('./results/ChaRes/deco_HRS_ch_rsp.png',format = 'PNG' , dpi = 300)
    
    plt.show() 
    
    
if __name__ == "__main__":
    challenge_size= 16
    
    main_LRS(challenge_size)
    # main_HRS(challenge_size)

