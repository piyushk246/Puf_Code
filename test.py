import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def inter_chip(pufs, binary_responses):
    distances = []
    s = 0

    # Ensure the binary_responses are in a NumPy array format
    responses = np.asarray(binary_responses)

    # Calculate Hamming distances between all pairs of responses
    for i in range(pufs - 1):
        for j in range(i + 1, pufs):
            dist = hamming_distance(responses[i], responses[j])
            s += dist
            distances.append(dist)

    # Calculate inter-chip Hamming distance (in percentage form)
    inter_hd = (2 * s * 100) / (pufs * (pufs - 1) * len(responses[0]))
    
    # Normalize distances to percentage form
    distances = [(dist * 100 / len(responses[0])) for dist in distances]

    # Save distances to an Excel file
    df_dis = pd.DataFrame(distances)
    df_dis.to_excel('dis.xlsx', index=False)
    
    # Print statistics
    print("Inter-chip Hamming distance is:", inter_hd)
    print("Distances:", distances)
    print("Standard deviation:", np.std(distances))
    print("Total pairs:", len(distances))
    print("Minimum distance:", min(distances))
    print("Maximum distance:", max(distances))
    
    # Plotting the histogram
    plt.figure(figsize=(8, 6))  # Specify figure size
    # plt.xlim(0, 30)  # Set limits for the x-axis
    plt.yticks(weight='bold', fontsize=12)  # Customize y-axis ticks

    # Plot histogram for Hamming distances
    plt.hist(distances, bins=16, edgecolor='k', alpha=0.7, label='HRS')

    # Customize the title and labels
    plt.title('Hamming Distance Time Multiplexing', fontweight='bold', fontsize=12)
    plt.xlabel('Hamming Distance', fontweight='bold', fontsize=14)
    plt.ylabel('Frequency', fontweight='bold', fontsize=14)

    # Add legend
    plt.legend(fontsize=14)

    # Uncomment the following line if you want to save the plot
    # plt.savefig('./Hamming_Distance_Plot.png', format='PNG', dpi=300)

    # Show the plot
    plt.show()
    
    return distances

def hamming_distance(response1, response2):
    # Compute the Hamming distance between two binary responses
    return sum(r1 != r2 for r1, r2 in zip(response1, response2))

# Example usage:
binary_responses = [
    [0, 1, 0, 1, 1, 0, 1, 0],
    [1, 0, 1, 0, 0, 1, 0, 1],
    [0, 1, 1, 0, 1, 1, 0, 0],
    [1, 1, 0, 0, 0, 1, 1, 1]
]

distances = inter_chip(pufs=len(binary_responses), binary_responses=binary_responses)
