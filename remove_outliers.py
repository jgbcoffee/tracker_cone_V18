import pandas as pd
import numpy as np

# This code aims to filter out any outliers in the centroid csv created after the main loop of center data is collected

class OutlierRemover:
    # Initialize class atributes
    def __init__(self, filepath):
        self.df = pd.read_csv(filepath)

    # Main z-score filtering using theory from: https://medium.com/@bhatshrinath41/quick-guide-to-outlier-treatment-ada01f8cfc5
    def remove_outliers_z_score(self, column, threshold=1):
        mean = self.df[column].mean()
        std = self.df[column].std()
        z_scores = (self.df[column] - mean) / std
        self.df = self.df[np.abs(z_scores) < threshold]
        return self.df

    def save_to_csv(self, output_filepath):
        self.df.to_csv(output_filepath, index=False)

# This section uses pandas to save the filtered set into a new csv file named (df_no_outliers)
if __name__ == "__main__":
    input_filepath = 'centroid_coordinates'
    output_filepath = 'df_no_outliers'
    
    outlier_remover = OutlierRemover(input_filepath)
    
    outlier_remover.remove_outliers_z_score('x-coordinate')
    outlier_remover.remove_outliers_z_score('y-coordinate')

    outlier_remover.save_to_csv(output_filepath)
