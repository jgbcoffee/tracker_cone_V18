import numpy as np
import cv2
import pandas as pd
from findcentroid import FindCentroid
from remove_outliers import OutlierRemover
from cone_distance import ConeCalculator
from coordinate_analyzer import CoordinateAnalyzer
import time

cv2.VideoWriter_fourcc(*'MJPG')

class CentroidDetector:
    def __init__(self, video_source=0, max_corners=8, quality_level=0.6, min_distance=100):
        self.cap = cv2.VideoCapture(video_source)
        self.centroid_coord_list = []
        self.max_corners = max_corners
        self.quality_level = quality_level
        self.min_distance = min_distance
        self.start = None  # Initialize start time to None
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('realtime_tracking_0.6_.avi', self.fourcc, 20.0, (640, 480))

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        try:
            corners = cv2.goodFeaturesToTrack(gray, maxCorners=self.max_corners, qualityLevel=self.quality_level, minDistance=self.min_distance)
            corners = np.int0(corners)
            reshaped_array = corners.ravel().reshape(-1, 2)
            coordinates = [tuple(pair) for pair in reshaped_array]
            
            if len(coordinates) <= 2:
                return frame, None

            find_centroid = FindCentroid(vertices=coordinates)
            centroid = find_centroid.shoelace(vertices=coordinates)

            if abs(centroid[0]) > 640 or abs(centroid[1]) > 480:
                return frame, None

            for corner in corners:
                x, y = corner.ravel()
                cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)

            frame = cv2.circle(frame, (int(centroid[0]), int(centroid[1])), 2, (0, 0, 255), 5, -1)

            analyzer = CoordinateAnalyzer(coordinates)
            lowest_x_highest_y, highest_x_lowest_y = analyzer.find_extreme_coordinates()

            x1, y1 = lowest_x_highest_y
            x2, y2 = highest_x_lowest_y
            calculator = ConeCalculator(x1, y1, x2, y2)
            calculator.calculate()

            return frame, centroid

        except (ValueError, OverflowError, TypeError) as e:
            print(f"Irregularity: {e}")
            return frame, None

    def capture_video(self):
        self.start = time.time()  # Start the timer when video capture begins
        while True:
            frame, centroid = self.process_frame()
            if frame is not None:
                self.out.write(frame)
                cv2.imshow('frame', frame)
                if centroid:
                    self.centroid_coord_list.append(centroid)
            if cv2.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def save_centroid_data(self, output_filepath='centroid_coordinates'):
        df = pd.DataFrame(self.centroid_coord_list, columns=["x-coordinate", "y-coordinate"])
        df.to_csv(output_filepath, index=False)
        return output_filepath

    def remove_outliers(self, input_filepath, output_filepath='df_no_outliers'):
        outlier_remover = OutlierRemover(input_filepath)
        outlier_remover.remove_outliers_z_score('x-coordinate')
        outlier_remover.remove_outliers_z_score('y-coordinate')
        outlier_remover.save_to_csv(output_filepath)
        return output_filepath

    def get_median_coordinates(self, filtered_filepath='df_no_outliers'):
        df_filtered = pd.read_csv(filtered_filepath)
        median_x = df_filtered["x-coordinate"].median()
        median_y = df_filtered["y-coordinate"].median()
        print("Median Center Coordinates are:", median_x, median_y)
        return median_x, median_y
    
    def counter(self):
        end = time.time()
        return (end - self.start)  # Use self.start to reference the start time
    
    def run(self):
        try:
            self.capture_video()
            centroid_file = self.save_centroid_data()
            cleaned_file = self.remove_outliers(input_filepath=centroid_file)
            self.get_median_coordinates(filtered_filepath=cleaned_file)
            elapsed_time = self.counter()
            return elapsed_time  # Return elapsed time after the run
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # Ensure something is returned even if an error occurs
        
if __name__ == "__main__":
    detector = CentroidDetector()
    detector.capture_video()

    centroid_file = detector.save_centroid_data()
    cleaned_file = detector.remove_outliers(input_filepath=centroid_file)
    detector.get_median_coordinates(filtered_filepath=cleaned_file)
    elapsed_time = detector.counter()  
    print(f"Elapsed Time: {elapsed_time} seconds")
