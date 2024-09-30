from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD
import numpy as np
import cv2
import pandas as pd
from findcentroid import FindCentroid
from cone_distance import ConeCalculator
from coordinate_analyzer import CoordinateAnalyzer
import time

cv2.VideoWriter_fourcc(*'MJPG')

# ---------------------------------------------------------------- #
mc = MyCobot(PI_PORT, 115200)

mc.power_on()
mc.set_color(0, 0, 50) # qChange the color here
# ---------------------------------------------------------------- #



class TrackMove:
    def __init__(self, video_source=0, max_corners=8, quality_level=0.4, min_distance=100):
        self.cap = cv2.VideoCapture(video_source)
        self.centroid_coord_list = []
        self.movement_commands = []
        self.max_corners = max_corners
        self.quality_level = quality_level
        self.min_distance = min_distance
        self.width = 640
        self.height = 480
        self.start = None  # Initialize start time to None
        self.universal_time = 0
        self.DPI = 96      # Dots per inch
        self.z_distance = []
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        self.out = cv2.VideoWriter('track_and_move.avi', self.fourcc, 20.0, (640, 480))

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
            self.z_distance.append(calculator.calculate())
            

            return frame, centroid

        except (ValueError, OverflowError, TypeError) as e:
            print(f"Irregularity: {e}")
            return frame, None

    def capture_video(self):
        itteration = 0
        self.start = time.time()  # Start the timer when video capture begins
        while True:

            self.universal_time = self.counter()
            #print(self.universal_time)

            frame, centroid = self.process_frame()
            if frame is not None:
                self.out.write(frame)
                cv2.imshow('frame', frame)
                if centroid:
                    self.centroid_coord_list.append(centroid)

            #self.check_contraints()
            #arm_move = self.get_moving_median()

            if round(self.universal_time, 1) % 4 == 0:   # THis is were we control how long between each movement
                print(f"\nTime Progressed: {self.universal_time}")
                itteration += 1
                try:
                    arm_move = self.get_moving_median()
                    print(f"Move the robot arms X: {arm_move[0]}, and Y:  {arm_move[1]}")
                    position_data = mc.get_coords()
                    print(f"Original Position: {position_data}")

                    position_data[0] += 2 * round(arm_move[0])
                    position_data[1] += round(arm_move[1])
                    
                    print(f"New Position: {position_data}")

# ------------------------------------------------------------------------------------------------------------------------------ #
# --------------------------------------------  Expiremental Correction Feature ------------------------------------------------ #                    
# ------------------------------------------------------------------------------------------------------------------------------ #
                    mc.send_coords(position_data, 10, 0)
                    if itteration % 4 == 0:
                        #time.sleep(2)
                        angle_data = mc.get_angles()
                        angle_data[2] = -angle_data[1]
                        angle_data[3] = 80
                        #angle_data[5] = -90
                        mc.send_angles(angle_data, 10)
                        #time.sleep(2)
# ------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------------ #
# ------------------------------------------------------------------------------------------------------------------------------ #

                    self.movement_commands.append(
                        f"XY Movement Itteration Index: {itteration}\n"
                        f"Current Coordinates: {mc.get_coords()}\n"
                        f"Current Angles: {mc.get_angles()}\n"
                        f"Reference Centroid at: {arm_move[2]}\n"
                        f"X-Direction Command Movement: {int(arm_move[0])}\n"
                        f"Y-Direction Command Movement: {int(arm_move[1])}\n"
                        f"Z-Direction Command Movement: 0 \n"
                    )

                except (ValueError, OverflowError, TypeError, IndexError) as e:
                    print(f"Irregularity: {e}")
                    
            try:
                print(arm_move[2][0], arm_move[2][1])
                if (self.width/2 - 20) <= arm_move[2][0] <= (self.width/2 + 20) and (self.height/2 - 10) <= arm_move[2][1] <= (self.height/2 + 30):
                    #if cv2.waitKey(1) == ord('d'):
                    steps = 3
                    position_data = mc.get_coords()
                    angle_data = mc.get_angles()
                    print(f"Current Position: {position_data}")
                    print("Moving to True Center...")
                    #time.sleep(3)
                    #y_compensation = -110
                    #mc.send_coords(position_data, 5, 0)
                    #time.sleep(1)
                    y_static = position_data[1]
                
                    for n in range(1, steps + 1):
                        remaining_distance = None
                        if  n == 1:
                            y_compensation = -20
                            y_static += y_compensation
                            #angle_data[2] = -angle_data[1]
                            #angle_data[3] = 90
                            #mc.send_angles(angle_data, 3)
                            
                        elif n == 2:
                            y_compensation = -85
                            y_static += y_compensation
                            #angle_data[2] = -angle_data[1]
                            #angle_data[3] = 90
                            #mc.send_angles(angle_data, 3)
                            
                        elif n == 3:
                            y_compensation = -30
                            y_static += y_compensation
                            #angle_data[2] = -angle_data[1]
                            #angle_data[3] = 90
                            #mc.send_angles(angle_data, 3)
                        
                        print(f"Undergoing Docking - Step {n}")

                        time.sleep(4)
                        z_move = np.median(self.z_distance) / (steps * 4) #### Remove the 2 factor, this is for safety
                        print(f"Step {n}, moving: {z_move} mm")
                        position_data[1] = y_static
                        position_data[2] += int(z_move)

                        self.movement_commands.append(
                            f"Current Z Movement Iteration: {n}\n"
                            f"Reference Centroid at: {arm_move[2]}\n"
                            f"X-Direction Command Movement: 0\n"
                            f"Y-Direction Command Movement: 0\n"
                            f"Z-Direction Command Movement: {z_move}\n"
                            f"Current Coordinates: {mc.get_coords()}\n"
                            f"Current Angles: {mc.get_angles()}\n"
                        )

                        mc.send_coords(position_data, 8, 1)
                        remaining_distance = np.median(self.z_distance) - z_move * n
                        print(f"{remaining_distance} mm remaining \n")   ### This wont be correct if you have the 2 factor
                        # IF USER PRESSES D, ATTEMPT DOCKING
                        time.sleep(7)

                    user_input = input(f"Fufill docking of {remaining_distance} mm? 'Yes' or 'No': ").lower()
                    if user_input == "yes":
                        position_data = mc.get_coords()
                        position_data[2] += remaining_distance / 6
                        mc.send_coords(position_data, 5, 1)
                        time.sleep(4)
                        break
                    else:
                        break


                
            except (ValueError, OverflowError, TypeError, IndexError) as e:
                    print(f"Irregularity: {e}")
                    pass
                    
            if cv2.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()
    
    def get_moving_median(self):
        bin_width = 6
        try:
            #gets last [binwidth] elements from the list of coordinates
            last_elements = self.centroid_coord_list[-bin_width:]

            #converts to numpy array to make it easier to take the median
            last_element_numpy = np.array(last_elements)

            #takes median of each column
            median_x_y = np.median(last_element_numpy, 0)

            #rounds to get rid of decimals
            np.round(median_x_y)

            x_offset = median_x_y[0] - self.width/2 
            y_offset = -(self.height/2 - median_x_y[1])

            mm_displacement_x = (x_offset * 25.4) / self.DPI
            mm_displacement_y = (y_offset * 25.4) / self.DPI


            print(f"x offset = {x_offset}")
            print(f"y offset = {y_offset}")

            print(f"Milimeter Displacement X = {mm_displacement_x}")
            print(f"Milimeter Displacement Y = {mm_displacement_y}")

            return mm_displacement_x, mm_displacement_y, median_x_y

        except (ValueError, OverflowError, TypeError, IndexError) as e:
            #print(f"Irregularity: {e}")
            return None

    def counter(self):
        end = time.time()
        return (end - self.start)  # Use self.start to reference the start time
    
    def save_movement_commands(self, output_filepath='commands/movement_commands.txt'):
        df = pd.DataFrame(self.movement_commands, columns=["Commands"])
        df.to_csv(output_filepath, index=False, header=False)

# --------------------------------------------  Used to limit arm to arm distances ------------------------------------------------ # 
    def check_contraints(self):
        running_angles = mc.get_angles()
        if abs(running_angles[1] - running_angles[3]) < 20:
            mc.pause()
        
        if abs(running_angles[2] - running_angles[4]) < 20:
            mc.pause()
# --------------------------------------------------------------------------------------------------------------------------------- # 

    def run(self):
        try:
            self.capture_video()
            move_commands = self.save_movement_commands()
            elapsed_time = self.counter()
            return elapsed_time  # Return elapsed time after the run
        
        except Exception as e:
            print(f"An error occurred: {e}")
            return None  # Ensure something is returned even if an error occurs
        
#if __name__ == "__main__":
    #detector = TrackMove()
    #detector.capture_video()
    #x_displace, y_displace = detector.capture_video()
    #detector.get_moving_median()
    #moving_median = detector.get_moving_median()

    #elapsed_time = detector.counter()  
    #print(f"Elapsed Time: {elapsed_time} seconds")
