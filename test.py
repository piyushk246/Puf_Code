# import csv
# from itertools import combinations
# import matplotlib.pyplot as plt
# import ast  # For safely converting strings to lists

# # Function to calculate the Hamming distance between two binary strings (now lists)
# def hamming_distance(resp1, resp2):
#     return sum(el1 != el2 for el1, el2 in zip(resp1, resp2))

# # Function to read CRP data from CSV
# def read_crp(file_path):
#     crp = {}
#     with open(file_path, mode='r') as file:
#         csv_reader = csv.DictReader(file)
#         for row in csv_reader:
#             challenge = ast.literal_eval(row['Challenges'])  # Convert challenge string to list
#             response_binary = ast.literal_eval(row['ResponsesBinary'])  # Convert response string to list
            
#             challenge = tuple(challenge)  # Convert challenge to a tuple so it can be used as a dict key
            
#             if challenge not in crp:
#                 crp[challenge] = []
#             crp[challenge].append(response_binary)
#     return crp

# # Calculate Inter-Hamming Distance
# def calculate_inter_hamming(crp):
#     inter_distances = []
#     challenges = list(crp.keys())
#     # Compare responses from different challenges
#     for i in range(len(challenges)):
#         for j in range(i + 1, len(challenges)):
#             responses1 = crp[challenges[i]]
#             responses2 = crp[challenges[j]]
#             for resp1 in responses1:
#                 for resp2 in responses2:
#                     distance = hamming_distance(resp1, resp2)
#                     inter_distances.append(distance)
#     return inter_distances

# # Plot histogram of Inter-Hamming Distances
# def plot_histogram(distances, num_bits):
#     plt.hist(distances, bins=num_bits, edgecolor='black', alpha=0.7)
#     plt.title('Histogram of Inter-Hamming Distances')
#     plt.xlabel('Hamming Distance')
#     plt.ylabel('Frequency')
#     plt.grid(True)
#     plt.show()

# # Example Usage
# # file_path = 'path_to_your_csv_file.csv'
# file_path = './output_16bit(LRS).csv'
# crp_data = read_crp(file_path)

# # Print CRP data for verification
# # print(crp_data)

# # Calculate inter-Hamming distances
# inter_hd_distances = calculate_inter_hamming(crp_data)

# # Plot histogram (assuming 32-bit responses)
# plot_histogram(inter_hd_distances, num_bits=32)


####################by multiprocessing #########


import csv
from itertools import combinations
import matplotlib.pyplot as plt
import ast
from concurrent.futures import ThreadPoolExecutor, as_completed
import os  # Import os module to get the number of CPU cores

# Function to calculate the Hamming distance between two binary strings (now lists)
def hamming_distance(resp1, resp2):
    return sum(el1 != el2 for el1, el2 in zip(resp1, resp2))

# Function to read CRP data from CSV
def read_crp(file_path):
    crp = {}
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            challenge = ast.literal_eval(row['Challenges'])  # Convert challenge string to list
            response_binary = ast.literal_eval(row['ResponsesBinary'])  # Convert response string to list
            
            challenge = tuple(challenge)  # Convert challenge to a tuple so it can be used as a dict key
            
            if challenge not in crp:
                crp[challenge] = []
            crp[challenge].append(response_binary)
    return crp

# Function to compute Hamming distances between responses of different challenges
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

# Calculate Inter-Hamming Distance using threading
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

# Plot histogram of Inter-Hamming Distances
def plot_histogram(distances, num_bits):
    plt.hist(distances, bins=num_bits, edgecolor='black', alpha=0.7)
    plt.title('Histogram of Inter-Hamming Distances')
    plt.xlabel('Hamming Distance')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

# Example Usage
file_path = './output_16bit(LRS).csv'
crp = read_crp(file_path)

# Calculate inter-Hamming distances using threading
inter_hd_distances = calculate_inter_hamming_threading(crp)

# Plot histogram (assuming 16-bit responses)
plot_histogram(inter_hd_distances, num_bits=16)
