import matplotlib.pyplot as plt
import numpy as np

class Plot:
    def __init__(self, challenges, responses, challenge_size, col_page):
        self.challenges = challenges
        self.responses = responses
        self.col_page = col_page
        self.challenges_size = challenge_size
        self.y_ref = (2**challenge_size) / (2*col_page)
        # print(self.y_ref)

    def CRP(self):
        plt.figure(figsize=(10, 6))  # Adjust the size of the figure if needed

        # Setting the x-axis limit
        plt.xlim(0, 65536)

        # Creating ticks and labels
        ticks = np.arange(0, 65536, 13107)
        labels = [f'{tick}' for tick in ticks]

        # Setting the x-ticks and y-ticks with customized font properties
        plt.xticks(ticks, labels, weight='bold', fontsize=12)
        plt.yticks(weight='bold', fontsize=12)

        # Plotting the histogram of responses
        plt.hist(self.responses, bins=32, edgecolor='k', alpha=0.7, label='LRS')

        # Adding a horizontal line at the calculated y_ref
        plt.axhline(y=self.y_ref, color='r', linestyle='--', label='Ideal')

        # Adding titles and labels with bold fonts
        plt.title('Uniqueness of Responses', fontweight='bold', fontsize=16)
        plt.xlabel('Responses', fontweight='bold', fontsize=14)
        plt.ylabel('Frequency', fontweight='bold', fontsize=14)

        # Displaying the legend with a specific font size
        plt.legend(fontsize=12)
        plt.tight_layout()

        # Display the plot
        plt.show()

# Example usage:
challenges = np.random.randint(0, 2, size=(10, 8))  # Example challenge data
responses = np.random.randint(0, 65536, size=10000)  # Example response data
plotter = Plot(challenges, responses, 8, 8)  # Example values for challenges_size and col_page
# plotter.CRP()
