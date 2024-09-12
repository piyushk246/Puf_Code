import pandas as pd
import ast
from itertools import combinations
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import Pool
import os

def hamming_distance(resp1, resp2):
    return sum(el1 != el2 for el1, el2 in zip(resp1, resp2))

def read_crp(file_path):
    crp = {}
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        challenge = ast.literal_eval(row['Challenges'])  # Convert challenge string to list
        response_binary = ast.literal_eval(row['ResponsesBinary'])  # Convert response string to list
        
        challenge = tuple(challenge)  # Convert challenge to a tuple so it can be used as a dict key
        
        if challenge not in crp:
            crp[challenge] = []
        crp[challenge].append(response_binary)
    return crp

def compute_distances(challenges_pair):
    challenge1, challenge2 = challenges_pair
    distances = []
    responses1 = crp[challenge1]
    responses2 = crp[challenge2]
    for resp1 in responses1:
        for resp2 in responses2:
            distance = hamming_distance(resp1, resp2)
            distances.append(distance)
    return distances

def calculate_inter_hamming_threading(crp):
    inter_distances = []
    challenges = list(crp.keys())
    challenge_pairs = combinations(challenges, 2)
    
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        future_to_pair = {executor.submit(compute_distances, pair): pair for pair in challenge_pairs}
        
        for future in as_completed(future_to_pair):
            result = future.result()
            inter_distances.extend(result)
        
    return inter_distances

def calculate_inter_hamming_multiprocessing(crp):
    inter_distances = []
    challenges = list(crp.keys())
    challenge_pairs = list(combinations(challenges, 2))
    
    with Pool(processes=os.cpu_count()) as pool:
        results = pool.map(compute_distances, challenge_pairs)
        
    for result in results:
        inter_distances.extend(result)
    
    return inter_distances

def plot_histogram(distances, num_bits):
    plt.hist(distances, bins=num_bits, edgecolor='black', alpha=0.7)
    plt.title('Histogram of Inter-Hamming Distances')
    plt.xlabel('Hamming Distance')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig("inter.png")
    plt.show()

# Example Usage
file_path = './output_16bit(LRS).xlsx'  # Change extension if needed
crp = read_crp(file_path)

# Calculate inter-Hamming distances using multiprocessing
inter_hd_distances = calculate_inter_hamming_multiprocessing(crp)

# Plot histogram (assuming 16-bit responses)
plot_histogram(inter_hd_distances, num_bits=16)
