import numpy as np
import pylab as plt
import pandas as pd

class RunningMedianCalculator:
    def __init__(self, csv_file, total_bins=6):
        # Initialize with CSV file and number of bins
        self.df_filtered = pd.read_csv(csv_file)
        self.X = self.df_filtered["x-coordinate"]
        self.Y = -self.df_filtered["y-coordinate"]
        self.total_bins = total_bins
        self.bins = None
        self.delta = None
        self.idx = None
        self.running_median = None

    def calculate_bins(self):
        # Calculate bins based on X coordinate range
        self.bins = np.linspace(self.X.min(), self.X.max(), self.total_bins)
        self.delta = self.bins[1] - self.bins[0]

    def calculate_running_median(self):
        # Digitize X into bins and calculate running median for Y
        self.idx = np.digitize(self.X, self.bins)
        self.running_median = [np.median(self.Y[self.idx == k]) for k in range(self.total_bins)]

    def plot(self):
        # Plot the results
        plt.scatter(self.X, self.Y, color='k', alpha=0.5, s=2)
        plt.plot(self.bins - self.delta / 2, self.running_median, 'r--', lw=4, alpha=0.8)
        plt.axis('tight')
        plt.xlabel("x-coordinate")
        plt.ylabel("y-coordinate")
        plt.title("Receiver Center Positions")
        plt.show()

    def get_final_median_point(self):
        # Get the final median point
        final_median_x = self.bins[-1] - self.delta / 2
        final_median_y = self.running_median[-1]
        return -final_median_x, -final_median_y

    def run(self):
        # Full execution pipeline
        self.calculate_bins()
        self.calculate_running_median()
        self.plot()
        final_x, final_y = self.get_final_median_point()
        print(f"Final Median Point: ({final_x}, {final_y})")

# Usage
if __name__ == "__main__":
    calculator = RunningMedianCalculator(csv_file='centroid_coordinates')
    calculator.run()
