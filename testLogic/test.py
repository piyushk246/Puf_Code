import numpy as np


from RRAMArrayArchitecture import RRAMArrayArchitecture
from RRAMArrayArchitecture import RRAMArrayElementAssign

    
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



def get_response_Deco(challenge_row, challenge_col, rram_cell, ref_res, col_page):
    response = []
    sel_row = row_decoder(challenge_row)
    sel_col = col_mux(challenge_col)
    
    count = 0
    for _ in range(2*(len(challenge_row) + len(challenge_col))):
        response.append(1 if rram_cell[sel_row][sel_col + count] > ref_res else 0)
        count += col_page
    return np.array(response)


rram = RRAMArrayArchitecture(2048, 2048)

# usecols='E' == LRS
populator = RRAMArrayElementAssign(r'fig5(b).xlsx', usecols='B', skiprows=[1, 2])
# Load the data from the Excel sheet
populator.load_data()
# Populate the RRAM array with the data
populator.populate(rram)
# rram.display_architecture()
array = rram.get_array()
# print("Returned Array:",array)

challenge= [1,0,1,0,0,0,1,1,1,0,1,0,0,0,1,1]
print(len(challenge))
challenge_row, challenge_col = challenge[:10],challenge[10:]

res = get_response_Deco(challenge_row= challenge_row, challenge_col= challenge_col, rram_cell = array, ref_res = 8.16, col_page = 32)

print(res)
print(len(res))