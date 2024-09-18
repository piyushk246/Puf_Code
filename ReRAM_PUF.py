# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 15:07:12 2024

@author: LENOVO
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


#collecting the hrs values
#col E has LRS values and col B has HRS values
# df = pd.read_excel(r'fig5(b).xlsx', usecols='B', skiprows=[1,2])
df = pd.read_excel(r'C:\Users\Piyush\Desktop\sem3\PUF\Code\fig5(b).xlsx', usecols='B', skiprows=[1,2])

res_f = df.to_numpy().flatten()




# print(res_f)

#ref_res = np.median(res_f) #finding the reference resistance
ref_res=8.1814  #HRS
# ref_res=4.43 #LRs
#appending the hrs values to have a larger set of data
for i in range(10):
    res_f=np.append(res_f,res_f)
# print(len(res_f))
'''
manually entering the row and col number based on challenge size

for 4 bit challenge ,row=8
for 8 bit challenge ,row=32
for 16bit challenge ,row=1024
'''
#row = 2**19
row = 1024
col = row
#randomly generating a challenge, where size is challenge size
challenge = np.random.choice([0, 1], size=16, p=[0.5, 0.5])
#challenge = np.random.choice([0, 1], size=2**13, p=[0.5, 0.5])

#manually entering challenge to ensure same challenge is given to HRS and LRS data during inter chip variation calculation
#challenge=[1,0,1,0,0,1,0,1,1,0,0,1,0,0,1,1]
#challenge=np.array(challenge)

select_line=(int)(np.log2(row))
count=len(challenge)
# checking the number of blocks based on the size of the challenge
if (np.log2(len(challenge))%2 !=0):
    block=2
    pages=len(challenge)//2
    
else:
    block=1
    pages=(int)(len(challenge))
col_page = col//pages #number of columns in each page

#dividing the input challenge bit into inputs for row decoder and column selector
challenge_row = challenge[:select_line]
challenge_col = challenge[select_line:]

#will return the selected row based on challenge
def row_decoder(challenge_row):
    c=len(challenge_row)-1
    d=0
    for i in range((len(challenge_row))):
        r=challenge_row[i]%10
        d=d+r*(2**c)
        c-=1
        # print(d)
    return d

#will return the selected columns from each page based on the challenge
def col_mux(challenge_col):
    c=len(challenge_col)-1
    d=0
    for i in range((len(challenge_col))):
        r=challenge_col[i]%10
        d=d+r*(2**c)
        c-=1
    return d

#function to convert binary to digital
def converts_decimal(count,arr,master):
    d=0
    for i in range(len(arr)):
        r=arr[i]%10
        d=d+r*(2**count)
        count-=1
    master.append(d)
    return(master)

# print(challenge_row, challenge_col, ref_res, col_page)

def get_response(challenge_row, challenge_col, rram_cell, ref_res, col_page):
    response = []
    sel_row = row_decoder(challenge_row)
    sel_col = col_mux(challenge_col)
    count = 0
    for _ in range(pages):
        response.append(1 if rram_cell[sel_row][sel_col + count] > ref_res else 0)
        count += col_page
    return np.array(response)

# puf_instance will give the responses of various pufs
def puf_instances(challenge_row, challenge_col, res_f, row, col, ref_res, col_page):
    num_cells = row * col
    rram_cell = res_f[:num_cells].reshape((row, col))
    # print("rram_cell:",rram_cell)
    response = get_response(challenge_row, challenge_col, rram_cell, ref_res, col_page)
    # print(res_f[num_cells:])
    return response, res_f[num_cells:]

#function to count the occurance of each response
# def counter():
#     counts=[]
#     for i in range(len(responses)):
#          c=0
#          for j in range(len(responses)):
#              if np.array_equal(responses[i],responses[j]):
#                  c+=1
#          counts.append(c)
#     print(counts)

#calculates the variation in 2 responses
def hamming_distance(response1, response2):
    return sum(r1 != r2 for r1, r2 in zip(response1, response2))

#same challenge fed to different puf instances
# def inter_chip(pufs, challenge_row, challenge_col, res_f, row, col, ref_res, col_page):
#     distances = []
#     responses = []
#     s = 0
#     for _ in range(pufs):
#         if block==2:
#             response1, res_f = puf_instances(challenge_row, challenge_col, res_f, row, col, ref_res, col_page)
#             response2, res_f = puf_instances(challenge_row, challenge_col, res_f, row, col, ref_res, col_page)
#             response=np.append(response1,response2)
#         else:
#             response, res_f = puf_instances(challenge_row, challenge_col, res_f, row, col, ref_res, col_page)
#         responses.append(response)

#     responses = np.asarray(responses)
    
#     df = pd.DataFrame(responses)
#     df.to_excel('hamming_distance_responses.xlsx', index=False)
    
#     for i in range(pufs - 1):
#         for j in range(i + 1, pufs):
#             dist = hamming_distance(responses[i], responses[j])
#             s += dist
#             distances.append(dist)
#     #calculates the inter chip hamming distance
#     inter_hd = 2 / (pufs * (pufs - 1) * len(response)) * s * 100
    

    
#     #considering it in percentage form
#     distances = [(dist * 100 / len(response)) for dist in distances]
    
#     df_dis = pd.DataFrame(distances)
#     df_dis.to_excel('dis.xlsx', index=False)
    
#     print("Inter-chip Hamming distance is:", inter_hd)
#     print(distances)
#     print(np.std(distances))
#     print(len(distances))
#     print(min(distances))
#     print(max(distances))
#     return distances


#calculating the challenge response pair
def challenge_response():
    challenges=[]
    responses=[]
    responses_binary=[]
    challenges_binary=[]
    #generating all possible challenge response pairs
    for i in range(2**(len(challenge))):
        j = i
        challenge_new=[]
        while (i!=0):
            r=i%2
            challenge_new.append(r)
            i=i//2
        while len(challenge_new)<len(challenge):
            challenge_new.append(0)
        challenge_new.reverse()
        challenges_binary.append(challenge_new)
        challenge_row1 = challenge_new[:select_line]
        challenge_col1=challenge_new[select_line:]
        #converting challenges to its decimal equivalent
        challenges=converts_decimal((count-1),challenge_new,challenges)
        #challenges.append(challenge_new)
        if block==2:
            # sdjkdf = 0
            # print(j)
            response1, temp_res = puf_instances(challenge_row1, challenge_col1, res_f, row, col, ref_res, col_page)
            response2, _ = puf_instances(challenge_row1, challenge_col1, temp_res, row, col, ref_res, col_page)
            response=np.append(response1,response2)
        else:
            # print("##########################")
            response,_ = puf_instances(challenge_row1, challenge_col1, res_f, row, col, ref_res, col_page)
        responses_binary.append(response)
        #converting each response to its decimal equivalent
        responses=converts_decimal((count-1),response,responses)
        
        avg_response = np.mean(responses)
        # print("avger_response:",avg_response)

    responses_binary=np.array(responses_binary)#list of all possible responses in binary format
    responses=np.array(responses)#list of all possible responses in decimal format
    crp = pd.DataFrame({'Challenges': challenges_binary, 'ResponsesBinary': responses_binary.tolist(),'ChallengeDecimal':challenges,'ResponseDecimal': responses})
    # print(crp)
    # crp.to_csv('output_16bit(LRS).csv', index=False)
    crp.to_excel('output_16bit(LRS).xlsx', index=False)
    challenges=np.array(challenges)#list of all possible challenge
    return(challenges,responses)

'''
def check_randomness(cycles):
    challenges,responses,res_f=challenge_response(res_f)
    correlation_matrix = np.corrcoef(challenges, responses)
    correlation_numpy = correlation_matrix[0, 1]
    print("Randomness Factor:", correlation_numpy)
 '''

#getting the list of challenges and responses
challenges,responses=challenge_response()


'''
#checking correlation between challenge and response for one puf instance
correlation_matrix = np.corrcoef(challenges, responses)
correlation_numpy = correlation_matrix[0, 1]
print("Randomness Factor:", correlation_numpy)


#plotting
plt.figure(figsize=(10, 10))

#plotting inter chip hamming distance
#plt.subplot(2, 2, 2) '''

# plt.xlim(0, 100)
# ticks = np.arange(0, 100, 10)
# labels = [f'{tick} ' for tick in ticks]
# plt.xticks(ticks, labels,weight='bold',fontsize=12)
# plt.yticks(weight='bold',fontsize=12)
# plt.hist(inter_chip(100, challenge_row, challenge_col, res_f, row, col, ref_res, col_page), bins=40, edgecolor='k', alpha=0.7,label='HRS')
# plt.title('Inter-chip Hamming Distance',fontweight='bold',fontsize=16)
# plt.xlabel('Hamming Distance',fontweight='bold',fontsize=14)
# plt.ylabel('Frequency',fontweight='bold',fontsize=14)
# plt.legend(fontsize=20)

'''
#plotting the relation between challenge and response
#plt.subplot(2, 2, 3)
plt.xlim(0, 16)
ticks = np.arange(0, 16, 1)
labels = [f'{tick} ' for tick in ticks]
plt.xticks(ticks, labels,weight='bold')
plt.ylim(0, 16)
labels1 = [f'{tick} ' for tick in ticks]
plt.yticks(ticks, labels1,weight='bold')
plt.plot(challenges,responses,'o',markersize=4,color='#F81506',label='LRS')
plt.title('Relation between challenge and response',fontweight='bold',fontsize=16)
plt.xlabel('Challenge',fontweight='bold',fontsize=14)
plt.ylabel('Response',fontweight='bold',fontsize=14)
plt.legend(fontsize=20)
'''
# plotting occurance of each response in one puf instance
# plt.subplot(2, 2, 1)
# plt.xlim(0, 65536)
# ticks = np.arange(0, 65536,13107)
# labels = [f'{tick} ' for tick in ticks]
# plt.xticks(ticks, labels,weight='bold',fontsize=12)

bin = 16
ideal = 4096
# plt.yticks(weight='bold',fontsize=12)
counts, bins, bars = plt.hist(responses,bins=bin,edgecolor='k', alpha=0.7,label='HRS')
plt.axhline(y=ideal, color='r', linestyle='--', label='Ideal')
plt.title(f'Uniqueness of responses BIN = {bin}',fontweight='bold',fontsize=16 )
plt.xlabel('Responses',fontweight='bold',fontsize=14)
plt.ylabel('Frequency',fontweight='bold',fontsize=14)
plt.bar_label(bars,fontsize=6)
print(len(counts))
msq_error  = np.sqrt(np.sum((ideal - counts)**2)/len(counts))        #root mean square error (RMSE)
std_dev = np.std(responses)  

plt.text(0.4, 0.4, f'metric  = {msq_error :.2f}', 
     horizontalalignment='left', verticalalignment='top', 
     transform=plt.gca().transAxes, fontsize=8, color='k', weight='bold', 
     bbox=dict(facecolor='white', edgecolor='none', pad=3))
 
# Display the legend
plt.legend(loc='lower left', facecolor='white', edgecolor='black', fontsize=10)
# plt.legend(fontsize=10)

# plt.tight_layout()
plt.savefig(f'./results/UniqueResp/one16_c16r16_hrs_metric(HRS).png',format = 'PNG' , dpi = 300)
# plt.show()

'''

plt.subplot(2, 2, 2)
plt.xlim(0, 16)
ticks = np.arange(0, 16,1)
labels = [f'{tick} ' for tick in ticks]
plt.xticks(ticks, labels)
plt.hist(responses,bins=16, edgecolor='k', alpha=0.7)
plt.title('Uniqueness of responses with 16 bins',fontweight='bold',fontsize=16)
plt.xlabel('Responses',fontweight='bold',fontsize=14)
plt.ylabel('Frequency',fontweight='bold',fontsize=14)

plt.subplot(2, 2, 3)
plt.xlim(0, 16)
ticks = np.arange(0, 16,1)
labels = [f'{tick} ' for tick in ticks]
plt.xticks(ticks, labels)
plt.hist(responses,bins=16, edgecolor='k', alpha=0.7)
plt.title('Uniqueness of responses with 16 bins',fontweight='bold',fontsize=16)
plt.xlabel('Responses',fontweight='bold',fontsize=14)
plt.ylabel('Frequency',fontweight='bold',fontsize=14)


plt.subplot(2, 2, 4)
plt.xlim(0, 65536)
ticks = np.arange(0, 65536,3855)
labels = [f'{tick} ' for tick in ticks]
plt.xticks(ticks, labels)
plt.hist(responses,bins=1024, edgecolor='k', alpha=0.7)
plt.title('Uniqueness of responses with 1024 bins',fontweight='bold',fontsize=16)
plt.xlabel('Responses',fontweight='bold',fontsize=14)
plt.ylabel('Frequency',fontweight='bold',fontsize=14)

#plotting counts of each occurance
plt.grid()
#plt.subplot(2, 2, 4)
plt.xlim(0, 5)
ticks = np.arange(0, 5, 1)
labels = [f'{tick} ' for tick in ticks]
plt.xticks(ticks, labels)
plt.ylim(0, 100)
ticks1 = np.arange(0,100, 2)
labels1 = [f'{tick} ' for tick in ticks1]
plt.yticks(ticks1, labels1)
plt.hist(counts,bins=256, edgecolor='k', alpha=0.7)
plt.title('Frequency')
plt.xlabel('Responses')
plt.ylabel('counts')
'''

plt.tight_layout()
# plt.savefig('responses16_hrs.png',format = 'PNG' , dpi = 300)
plt.show()

