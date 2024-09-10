
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


######################################
#         Define the funtion         #
######################################

#will return the selected row based on challenge
def row_decoder(challenge_row):
    c=len(challenge_row)-1
    d=0
    for i in range((len(challenge_row))):
        r=challenge_row[i]%10
        d=d+r*(2**c)
        c-=1
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

# puf_instance will give the responses of various pufs
def puf_instances(challenge_row, challenge_col, res_f, row, col, ref_res, col_page):
    num_cells = row * col
    rram_cell = res_f[:num_cells].reshape((row, col))
    response = get_response(challenge_row, challenge_col, rram_cell, ref_res, col_page)
    return response, res_f[num_cells:]

def hamming_distance(response1, response2):
    return sum(r1 != r2 for r1, r2 in zip(response1, response2))

def inter_chip(pufs, challenge_row, challenge_col, res_f, row, col, ref_res, col_page):
    distances = []
    responses = []
    s = 0
    for _ in range(pufs):
        if block==2:
            response1, res_f = puf_instances(challenge_row, challenge_col, res_f, row, col, ref_res, col_page)
            response2, res_f = puf_instances(challenge_row, challenge_col, res_f, row, col, ref_res, col_page)
            response=np.append(response1,response2)
        else:
            response, res_f = puf_instances(challenge_row, challenge_col, res_f, row, col, ref_res, col_page)
        responses.append(response)

    responses = np.asarray(responses)
    for i in range(pufs - 1):
        for j in range(i + 1, pufs):
            dist = hamming_distance(responses[i], responses[j])
            s += dist
            distances.append(dist)
    #calculates the inter chip hamming distance
    inter_hd = 2 / (pufs * (pufs - 1) * len(response)) * s * 100
    #considering it in percentage form
    distances = [(dist * 100 / len(response)) for dist in distances]
    print("Inter-chip Hamming distance is:", inter_hd)
    print(distances)
    print(np.std(distances))
    print(len(distances))
    print(min(distances))
    print(max(distances))
    return distances


#function to count the occurance of each response
def counter(responses):
    counts=[]
    for i in range(len(responses)):
         c=0
         for j in range(len(responses)):
             if np.array_equal(responses[i],responses[j]):
                 c+=1
         counts.append(c)
    print(counts)
    
    
def get_response(challenge_row, challenge_col, rram_cell, ref_res, col_page):
    response = []
    sel_row = row_decoder(challenge_row)
    sel_col = col_mux(challenge_col)
    count = 0
    for _ in range(pages):
        response.append(1 if rram_cell[sel_row][sel_col + count] > ref_res else 0)
        count += col_page
    return np.array(response)


def row_decoder(challenge_row):
    c=len(challenge_row)-1
    d=0
    for i in range((len(challenge_row))):
        r=challenge_row[i]%10
        d=d+r*(2**c)
        c-=1
    return d


def challenge_response(res_f,ref_res,count):
    challenges=[]
    responses=[]
    responses_binary=[]
    challenges_binary=[]
    #generating all possible challenge response pairs
    for i in range(2**(len(challenge))):
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
            response1, temp_res = puf_instances(challenge_row1, challenge_col1, res_f, row, col, ref_res, col_page)
            response2, _ = puf_instances(challenge_row1, challenge_col1, temp_res, row, col, ref_res, col_page)
            response=np.append(response1,response2)
        else:
            response,_ = puf_instances(challenge_row1, challenge_col1, res_f, row, col, ref_res, col_page)
        responses_binary.append(response)
        #converting each response to its decimal equivalent
        responses=converts_decimal((count-1),response,responses)

    responses_binary=np.array(responses_binary)#list of all possible responses in binary format
    responses=np.array(responses)#list of all possible responses in decimal format
    crp = pd.DataFrame({'Challenges': challenges_binary, 'ResponsesBinary': responses_binary.tolist(),'ChallengeDecimal':challenges,'ResponseDecimal': responses})
    print(crp)
    #crp.to_excel('output_16bit(LRS).xlsx', index=False)
    challenges=np.array(challenges)#list of all possible challenge
    return(challenges,responses)


if __name__ == "__main__":

    '''
    manually entering the row and col number based on challenge size

    for 4 bit challenge row=8       and size = 2 
    for 8 bit challenge row=32      and size = 8
    for 16bit challenge row=1024    and size =  16
    for 32 bit challenge row =      and size = 32  
    '''
    ref_res=8.1814

    ##############################################################
    #   read the ReRAM Resistacne vaule form the execl sheet     #
    ##############################################################

    #C:\Users\Piyush\Desktop\sem3\PUF\fig5(b).xlsx
    df = pd.read_excel(r'C:\Users\Piyush\Desktop\sem3\PUF\Code\unused\fig5(b).xlsx', usecols='B', skiprows=[1,2])

    res_f = df.to_numpy().flatten() #read the document
    # print(len(res_f))
    # print(res_f[len(res_f)-1])
    ref_res = np.mean(res_f)


    # for i in range(2):
    #     res_f=np.append(res_f,res_f)
    # # print("length = " ,len(res_f))
    # # print(res_f)


    #################################
    #   Give the input row and      #
    #################################

    row = 1024
    # row = 2**27

    col = row
    #randomly generating a challenge
    challenge = np.random.choice([0, 1], size=16, p=[0.5, 0.5])
    # challenge = np.random.choice([0, 1], size=2**5, p=[0.5, 0.5])

    # challenge = [1 ,0  ,1 , 1 ,1 ,1 ,1 ,0 ]
    print("Challenge: ",challenge)
    print("Challenge Length:",len(challenge))

    # challenge.reverse()
    select_line=(int)(np.log2(row))
    count=len(challenge) 

    print("Select Line:",select_line)

    # print(challenge)

    ###############################################
    #   take challenge form txt file in future    #
    ###############################################

    # checking the number of blocks based on the size of the challenge
    if (np.log2(len(challenge))%2 !=0):
        block=2 
        pages=len(challenge)//2
        print("pages if :",pages)
    else:
        block=1
        pages=(int)(len(challenge))
        print("pages else :",pages)

    col_page = col//pages #number of number of bitlines or columns in each page

    col_per_page = col_page

    print('Bit line:',col)
    print("Bit line per page:",col_per_page)
    print('pages:',pages)

    challenge_row = challenge[:select_line]
    challenge_col = challenge[select_line:]

    # print('challenge_row:',challenge_row)
    # print('challenge_col:',challenge_col)
    
    challenges,responses=challenge_response(res_f,ref_res,count)
    print("Row Decoder output:",row_decoder(challenge_row))
    
    # print("challenges:",challenges)