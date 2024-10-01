# Autonomous Docking with MyCobot Arm Control

Overview
This project uses a MyCobot robotic arm controlled through Python and a connected camera to track the movement of objects in real-time. 
The program captures video input, detects key corners in each frame using OpenCV, calculates the centroid of the polygon formed by those corners, and commands the MyCobot arm to move based on the calculated centroid. 
Centroid coordinates are tracked over time, and the MyCobot arm adjusts its position to align with the moving object.

Dependencies
The project requires the following libraries and hardware:

Libraries:
pymycobot
numpy
opencv-python (cv2)
pandas

Custom Modules:
FindCentroid
ConeCalculator
CoordinateAnalyzer

Hardware:
MyCobot robotic arm
A camera compatible with OpenCV
Raspberry Pi or any device that supports serial communication with MyCobot

Usage
Robotic Arm Initialization
The MyCobot robotic arm is initialized using the PI_PORT for communication and the baud rate of 115200. 
Before beginning the movement, the arm is powered on, and a default color (blue) is set.

_______________________________________________________________________________________________________

mc = MyCobot(PI_PORT, 115200)
mc.power_on()
mc.set_color(0, 0, 50)
_______________________________________________________________________________________________________

Video Capture and Corner Detection
The program captures video frames from the camera in real-time and processes them to detect corners using the Shi-Tomasi algorithm with OpenCV's goodFeaturesToTrack function. Two modes for corner detection are provided, based on object movement:

Stationary Objects:
MaxCorners: 8
QualityLevel: 0.4
MinDistance: 100

Moving Objects:
These parameters can be tuned as needed.

Centroid calculation uses the shoelace method to compute the centroid of the polygon formed by the corners. 
A filter ensures that centroids falling outside the defined frame are skipped.

Real-Time Display
Detected corners are displayed as blue circles, and the calculated centroid is shown as a red circle in each frame. The program runs continuously until 'q' is pressed to exit.

Movement Commands
Centroid positions are used to control the MyCobot arm, aligning its movements with the detected object’s centroid.
A median of the recent centroid coordinates is computed to generate movement commands for smoother operation.


_______________________________________________________________________________________________________

mc.send_coords(position_data, 10, 0)  # Commands the arm to move
_______________________________________________________________________________________________________

If the centroids align with the center of the frame, the program will attempt a docking procedure, adjusting the z-axis movement in small steps to achieve precise alignment.


# How it Works

Step-by-Step Breakdown

Capture Frames: The program continuously captures video frames from the camera feed.
Corner Detection: The frame is converted to grayscale, and corners are detected using goodFeaturesToTrack.
Centroid Calculation: The shoelace method is used to calculate the centroid of the polygon formed by the detected corners.
Arm Movement: Based on the centroid position, movement commands are generated for the MyCobot arm to align it with the centroid.
Z-Distance Calculation: The distance between extreme corners is calculated using the ConeCalculator for further refinement of arm movements.
Docking Procedure: If the object is within a certain threshold, a docking maneuver is attempted, moving the arm in precise steps.
Command Logging: All movement commands are logged and saved to a file for post-process analysis.

Output Files
track_and_move.avi: A video file showing the frames processed during the session.
commands/movement_commands.txt: A log of all movement commands issued to the MyCobot arm.

References
Shi-Tomasi algorithm: Good Features to Track - OpenCV Documentation
Shoelace theorem and centroid formula: Proof for Centroid Formula

Run the Program
Initialize the MyCobot arm and ensure the camera is connected.
Run the TrackMove class to begin video capture and movement control.
Press 'q' to stop the video feed and finalize movement commands.

_______________________________________________________________________________________________________

# Example to run
tracker = TrackMove()
tracker.run()
_______________________________________________________________________________________________________

