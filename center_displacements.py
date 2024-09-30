import numpy as np
import cv2
import pandas as pd
import time
import pylab as plt

class CentroidAnalyzer:
    def __init__(self, csv_file, width=640, height=480):
        self.df_original = pd.read_csv(csv_file)
        self.width = width
        self.height = height
        self.elapsed_time = None
        self.grouped_medians = None

    def set_elapsed_time(self, elapsed_time):
        """Set the elapsed time from an external source."""
        self.elapsed_time = elapsed_time
        self.calculate_group_medians()

    def calculate_group_medians(self):
        """Divide data into bins and calculate medians."""
        total_bins = int(self.elapsed_time)
        print(total_bins)

        # Divide the data into bins and assign group labels
        self.df_original['group'] = pd.qcut(self.df_original.index, total_bins, labels=False) + 1
        self.grouped_medians = self.df_original.groupby('group').median()

    def plot_medians(self):
        """Plot the median X and Y coordinates."""
        if self.grouped_medians is not None:
            x_medians = self.grouped_medians['x-coordinate']
            y_medians = self.grouped_medians['y-coordinate']

            plt.figure(figsize=(8, 6))
            plt.plot(x_medians, y_medians, marker='o', linestyle='-', color='b')

            plt.xlim(0, self.width)
            plt.ylim(0, self.height)
            plt.gca().invert_yaxis()
            plt.title(f"Median x-y Pixel Positions Over {int(self.elapsed_time)} Seconds")
            plt.xlabel('x (pixels)')
            plt.ylabel('y (pixels)')

            plt.grid(True)
            plt.show()
        else:
            print("Medians have not been calculated. Please set elapsed time first.")

# Usage example:

# Assume 'elapsed_time' is obtained from another file or source
# elapsed_time = 5

# analyzer = CentroidAnalyzer('centroid_coordinates.csv')
# analyzer.set_elapsed_time(elapsed_time)
# analyzer.plot_medians()
