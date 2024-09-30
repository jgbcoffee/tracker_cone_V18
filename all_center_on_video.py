import numpy as np
import cv2
import pandas as pd

class VideoProcessor:
    def __init__(self, video_source=0, csv_file='centroid_coordinates'):
        self.cap = cv2.VideoCapture(video_source)
        self.df_filtered = pd.read_csv(csv_file)
        self.width = int(self.cap.get(3))
        self.height = int(self.cap.get(4))
        self.x0, self.y0 = int(self.width / 2), int(self.height / 2)
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('center_tracking_0.6_.avi', self.fourcc, 20.0, (640, 480))

    def process_frame(self):
        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            frame = self.draw_circles(frame)
            #frame = self.draw_median_center(frame)
            self.out.write(frame)
            cv2.imshow('frame', frame)

            if cv2.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

    def draw_circles(self, frame):
        # Iterate over each row in df_filtered to get x and y coordinates
        for _, row in self.df_filtered.iterrows():
            x_coordinate = int(row['x-coordinate'])
            y_coordinate = int(row['y-coordinate'])

            # Draw a circle at each (x, y) position
            frame = cv2.circle(frame, (x_coordinate, y_coordinate), 1, (0, 0, 255), 5, -1)
        return frame

    def draw_median_center(self, frame):
        # Draw a circle at the median center
        median_x = int(self.df_filtered["x-coordinate"].median())
        median_y = int(self.df_filtered["y-coordinate"].median())
        #frame = cv2.circle(frame, (median_x, median_y), 1, (0, 255, 0), 5, -1)
        return frame



