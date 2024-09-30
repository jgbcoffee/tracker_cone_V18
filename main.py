from pymycobot.mycobot import MyCobot
from pymycobot import PI_PORT, PI_BAUD
import tkinter
import time
import tkinter
from track_object_centers import CentroidDetector
from all_center_on_video import VideoProcessor
from center_displacements import CentroidAnalyzer
from display_camera import VideoCaptureApp
from track_and_move import TrackMove


display_camera = VideoCaptureApp()

elapsed_time = 0
 


#---------------------------------------------------------------------------------------------#
mc = MyCobot(PI_PORT, 115200)

# Define the neutral position coordinates for the robot arm
NEUTRAL_POSITION = [-90, 125, -132, 90, 2, -90]

# Power on the robot and set the LED color to green (0, 10, 0) indicating it's ready
mc.power_on()
mc.set_color(0, 10, 0)

# Move the robot arm to the neutral position at speed 5 (mm/s) using mode 1 for linear movement
mc.send_angles(NEUTRAL_POSITION, 5)

#---------------------------------------------------------------------------------------------#

# Create the main window for the robot control UI
window = tkinter.Tk()
window.title("Autonomous Docking UI")
window.config(padx=30, pady=30, bg="white")

# --------------------------- Loading Images ------------------------------ #

# Load and display the title image in the window
title_path = "./Images/title.PNG"
canvas_title = tkinter.Canvas(window, width=324, height=50, bg="white", highlightthickness=0)
title_img = tkinter.PhotoImage(file=title_path)
canvas_title.create_image(162, 25, image=title_img) 
canvas_title.grid(column=0, row=0, columnspan=3, pady=(0, 20))

# Load and display the camera_on image in the window
cam_on = "./Images/camera_on.png"
canvas_cam_on = tkinter.Canvas(window, width=150, height=100, bg="white", highlightthickness=0)
cam_on_img = tkinter.PhotoImage(file=cam_on)
canvas_cam_on.create_image(75, 50, image=cam_on_img) 
canvas_cam_on.grid(column=0, row=1)

# Load and display the track_center image in the window
track_center = "./Images/track_center.png"
canvas_track_center = tkinter.Canvas(window, width=150, height=100, bg="white", highlightthickness=0)
track_center_img = tkinter.PhotoImage(file=track_center)
canvas_track_center.create_image(75, 50, image=track_center_img)  
canvas_track_center.grid(column=1, row=1)

# Load and display the track_center image in the window
track_and_follow = "./Images/track_and_follow.png"
canvas_track_and_follow = tkinter.Canvas(window, width=130, height=90, bg="white", highlightthickness=0)
track_and_follow_img = tkinter.PhotoImage(file=track_and_follow)
canvas_track_and_follow.create_image(65, 45, image=track_and_follow_img)  
canvas_track_and_follow.grid(column=2, row=1)

# Load and display the all_centers image in the window
all_centers = "./Images/all_centers.PNG"
canvas_all_centers = tkinter.Canvas(window, width=150, height=100, bg="white", highlightthickness=0)
all_centers_img = tkinter.PhotoImage(file=all_centers)
canvas_all_centers.create_image(75, 50, image=all_centers_img) 
canvas_all_centers.grid(column=0, row=3, columnspan=2)

# Load and display the track_path image in the window
track_path = "./Images/track_path.PNG"
canvas_track_path = tkinter.Canvas(window, width=150, height=100, bg="white", highlightthickness=0)
track_path_img = tkinter.PhotoImage(file=track_path)
canvas_track_path.create_image(75, 50, image=track_path_img)  
canvas_track_path.grid(column=1, row=3, columnspan=2)

# --------------------------- Camera Functions ------------------------------ #

# Function for when the "Display Camera" button is clicked
def Display_Camera_button_clicked():
    display_camera.run()
    pass


# Function for when the "Track Object Centers" button is clicked
def track_object_centers_button_clicked():
    global elapsed_time
    elapsed_time = CentroidDetector().run()
    print(elapsed_time)
    pass

##################
def track_and_follow_button_clicked():
    global elapsed_time
    elapsed_time = TrackMove().run()
    print(elapsed_time)
    pass

# DFunction for when the "Display Centers" button is clicked
def display_centers_button_clicked():
    VideoProcessor().process_frame()
    pass

# Function for when the "Plot Path" button is clicked
def Plot_Path_button_clicked():
    plot_path = CentroidAnalyzer(csv_file='centroid_coordinates')
    plot_path.set_elapsed_time(elapsed_time)
    plot_path.plot_medians()

# ---------------------------- UI SETUP ------------------------------- #
# Create button for Display Camera
Display_Camera_button = tkinter.Button(text="Display Camera", command=Display_Camera_button_clicked)
Display_Camera_button.grid(column=0, row=2, pady=(10, 10))

# Create button for Track Object Centers
track_object_centers_button = tkinter.Button(text="Track Object Centers", command=track_object_centers_button_clicked)
track_object_centers_button.grid(column=1, row=2, pady=(10, 10))

# Create button for Track Object Centers
track_and_follow_button = tkinter.Button(text="Track and Follow", command=track_and_follow_button_clicked)
track_and_follow_button.grid(column=2, row=2, pady=(10, 10))

# Create button for Display All Centers
display_centers_button = tkinter.Button(text="Display All Centers", command=display_centers_button_clicked)
display_centers_button.grid(column=0, row=4, columnspan=2, pady=(10, 10)) 

# Create button for Plot Path
Plot_Path_button = tkinter.Button(text="Plot Path", command=Plot_Path_button_clicked)
Plot_Path_button.grid(column=1, row=4, columnspan=2, pady=(10, 10))  

# Keep the window open and wait for user interaction
window.mainloop()

