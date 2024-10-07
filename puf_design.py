
import numpy as np
import pandas as pd

from RRAMArrayArchitecture import RRAMArrayArchitecture
from RRAMArrayArchitecture import RRAMArrayElementAssign

class puf_design:
    def __init__(self) -> None:
        pass
    
    def pages(self,challenge):
        return (int)(len(challenge))
    
    #will return the selected row based on challenge
    def row_decoder(self,challenge_row):
        c=len(challenge_row)-1
        d=0
        for i in range((len(challenge_row))):
            r=challenge_row[i]%10
            d=d+r*(2**c)
            c-=1
        return d

    #will return the selected columns from each page based on the challenge
    def col_mux(self,challenge_col):
        c=len(challenge_col)-1
        d=0
        for i in range((len(challenge_col))):
            r=challenge_col[i]%10
            d=d+r*(2**c)
            c-=1
        return d

    def get_response(self,challenge_row, challenge_col, rram_cell, ref_res, col_page):
        response = []
        sel_row = self.row_decoder(challenge_row)
        sel_col = self.col_mux(challenge_col)
        
        # print("sel_row:",sel_row)
        # print("sel_col:",sel_col)
        # print("len:",len(rram_cell))
        
        count = 0
        for _ in range((len(challenge_row) + len(challenge_col))):
            response.append(1 if rram_cell[sel_row][sel_col + count] > ref_res else 0)
            count += col_page
        return np.array(response)

    def get_response_Deco(self,challenge_row, challenge_col, rram_cell, ref_res, col_page):
        response = []
        sel_row = self.row_decoder(challenge_row)
        sel_col = self.col_mux(challenge_col)
        
        count = 0
        for _ in range(2*(len(challenge_row) + len(challenge_col))):
            response.append(1 if rram_cell[sel_row][sel_col + count] > ref_res else 0)
            count += col_page
        return np.array(response)

    # # puf_instance will give the responses of various pufs
    # def puf_instances(self,challenge_row, challenge_col, res_f, row, col, ref_res, col_page):
    #     num_cells = row * col
    #     rram_cell = res_f[:num_cells].reshape((row, col))
    #     response = self.get_response(challenge_row, challenge_col, rram_cell, ref_res, col_page)
    #     return response, res_f[num_cells:]

    #function to convert binary to digital
    def converts_decimal(self,count,arr,master):
        d=0
        for i in range(len(arr)):
            r=arr[i]%10
            d=d+r*(2**count)
            count-=1
        master.append(d)
        return(master)
    
    responce_bit= 0
    
    #calculating the challenge response pair //count = length of the challenge , block = number of the same block
    def challenge_response_same(self, array,  ref_res, col_page, challenge, select_line, count, block,file_name):
        challenges = []
        responses = []
        responses_binary = []
        challenges_binary = []
        responce_bit = block
        # Generating all possible challenge-response pairs
        for i in range(2**(len(challenge))):
            challenge_new = []
            while i != 0:
                r = i % 2
                challenge_new.append(r)
                i = i // 2
            while len(challenge_new) < len(challenge):
                challenge_new.append(0)
            challenge_new.reverse()
            challenges_binary.append(challenge_new)
            challenge_row1 = challenge_new[:select_line]
            challenge_col1 = challenge_new[select_line:]
            
            # Converting challenges to its decimal equivalent
            challenges = self.converts_decimal((count-1), challenge_new, challenges)
            
            # Getting the response using get_response
            # get_response(challenge_row, challenge_col, array, ref_res,  4)
            response1 = self.get_response(challenge_row1, challenge_col1, array, ref_res, col_page)
            
            if block == 2:
                # Reverse challenge_row1 and challenge_col1 for response2
                challenge_row1_reversed = list(reversed(challenge_row1))
                challenge_col1_reversed = list(reversed(challenge_col1))
                
                response2 = self.get_response(challenge_row1_reversed, challenge_col1_reversed, array, ref_res, col_page)
                response = np.append(response1, response2)
                # print(responses)
                responses = self.converts_decimal((2*count-1), response, responses)
                responses_binary.append(response)

                
            else:
                response = response1
                responses = self.converts_decimal((count-1), response, responses)
                # print(responses)
                responses_binary.append(response)


        responses_binary = np.array(responses_binary)  # List of all possible responses in binary format
        # print(responses_binary)
        
        responses = np.array(responses)  # List of all possible responses in decimal format
        # print(responses)
        crp = pd.DataFrame({f'Challenges_{len(challenge)}': challenges_binary, f'ResponsesBinary_{responce_bit*len(challenge)}': responses_binary.tolist(), 'ChallengeDecimal': challenges, 'ResponseDecimal': responses})
        # crp.to_csv(f'output_16bit(LRS)rsp{responce_bit*len(challenge)}.csv', index=False)
        crp.to_csv(f'{file_name}_{responce_bit*len(challenge)}.csv', index=False)
        
        challenges = np.array(challenges)  # List of all possible challenges
        return challenges, responses

    #calculating the challenge response pair for two differnt puf //count = length of the challenge , block = number of the same block
    def challenge_response_diff(self, array1, array2, ref_res, col_page, challenge, select_line, count,file_name):
        challenges = []
        responses = []
        responses_binary = []
        challenges_binary = []
        responce_bit = 2
        # Generating all possible challenge-response pairs
        for i in range(2**(len(challenge))):
            challenge_new = []
            while i != 0:
                r = i % 2
                challenge_new.append(r)
                i = i // 2
            while len(challenge_new) < len(challenge):
                challenge_new.append(0)
            challenge_new.reverse()
            challenges_binary.append(challenge_new)
            challenge_row1 = challenge_new[:select_line]
            challenge_col1 = challenge_new[select_line:]
            
            # Converting challenges to its decimal equivalent
            challenges = self.converts_decimal((count-1), challenge_new, challenges)
            
            # Getting the response using get_response
            # get_response(challenge_row, challenge_col, array, ref_res,  4)
            response1 = self.get_response(challenge_row1, challenge_col1, array1, ref_res, col_page)
            response2 = self.get_response(challenge_row1, challenge_col1, array2, ref_res, col_page)
            response = np.append(response1, response2)
            responses = self.converts_decimal((2*count-1), response, responses)
            responses_binary.append(response)
            

        responses_binary = np.array(responses_binary)  # List of all possible responses in binary format
        # print(responses_binary)
        
        responses = np.array(responses)  # List of all possible responses in decimal format
        # print(responses)
        crp = pd.DataFrame({f'Challenges_{len(challenge)}': challenges_binary, f'ResponsesBinary_{responce_bit*len(challenge)}': responses_binary.tolist(), 'ChallengeDecimal': challenges, 'ResponseDecimal': responses})
        # crp.to_csv(f'diff_output_16bit(LRS)rsp{responce_bit*len(challenge)}.csv', index=False)
        crp.to_csv(f'{file_name}_{responce_bit*len(challenge)}.csv', index=False)
        
        challenges = np.array(challenges)  # List of all possible challenges
        return challenges, responses

    def Decoder_challenge_2response(self, array,  ref_res, col_page, challenge_len, select_line, count, file_name):
        challenges = []
        responses = []
        responses_binary = []
        challenges_binary = []
        block = 2
        responce_bit = block
        # Generating all possible challenge-response pairs
        for i in range(2**(challenge_len)):
            challenge_new = []
            while i != 0:
                r = i % 2
                challenge_new.append(r)
                i = i // 2
            while len(challenge_new) < challenge_len:
                challenge_new.append(0)
            challenge_new.reverse()
            challenges_binary.append(challenge_new)
            challenge_row1 = challenge_new[:select_line]
            challenge_col1 = challenge_new[select_line:]

            # print(len(challenge_col1))
            # Converting challenges to its decimal equivalent
            challenges = self.converts_decimal((2*count-1), challenge_new, challenges)
            # print(challenges)

            # Getting the response using get_response
            # get_response(challenge_row, challenge_col, array, ref_res,  4)
            response1 = self.get_response(challenge_row1, challenge_col1, array, ref_res, col_page)
            
            # if block == 2:
            #     # Reverse challenge_row1 and challenge_col1 for response2
            #     challenge_row1_reversed = list(reversed(challenge_row1))
            #     challenge_col1_reversed = list(reversed(challenge_col1))
                
            #     response2 = self.get_response(challenge_row1_reversed, challenge_col1_reversed, array, ref_res, col_page)
            #     response = np.append(response1, response2)
            #     # print(responses)
            #     responses = self.converts_decimal((2*count-1), response, responses)
            #     responses_binary.append(response)

                
            # else:
            #     response = response1
            #     responses = self.converts_decimal((count-1), response, responses)
            #     # print(responses)
            #     responses_binary.append(response)

            response = response1
            responses = self.converts_decimal((count-1), response, responses)
            # print(responses)
            responses_binary.append(response)


        responses_binary = np.array(responses_binary)  # List of all possible responses in binary format
        # print(responses_binary)
        
        responses = np.array(responses)  # List of all possible responses in decimal format
        # print(responses)
        crp = pd.DataFrame({f'Challenges_{challenge_len}': challenges_binary, f'ResponsesBinary_{responce_bit*challenge_len}': responses_binary.tolist(), 'ChallengeDecimal': challenges, 'ResponseDecimal': responses})
        # crp.to_csv(f'output_16bit(LRS)rsp{responce_bit*len(challenge)}.csv', index=False)
        crp.to_csv(f'{file_name}_{2*challenge_len}.csv', index=False)
        
        challenges = np.array(challenges)  # List of all possible challenges
        return challenges, responses
    

if __name__ == '__main__':


    # # Create an instance of RRAMArrayArchitecture2048

            
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
    
    file_name = "./decode_ch16_rsp"
    PUF = puf_design()
    # def Decoder_challenge_2response(self, array,  ref_res, col_page, challenge_len, select_line, count,file_name):
    PUF.Decoder_challenge_2response(array = array,  ref_res = 8.15, col_page =32, challenge_len =16, select_line = 11, count= 16, file_name = file_name)