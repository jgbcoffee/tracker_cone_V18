# Theory from here: https://stackoverflow.com/questions/14038002/opencv-how-to-calculate-distance-between-camera-and-object-using-image

class ConeCalculator:
    def __init__(self, x1, y1, x2, y2):
        # Initialize attributes
        self.EFL = 3.04 # Focal length in mm (specs say 3.04, cal say 4.35)
        self.fx = 2612.90 # from MATLAb calibrations
        self.fy = 2637.94 # from MATLAb calibrations
        self.true_reciever_dimension = 99  # width/height of cone (mm)
        self.native_resolution = [96, 96]
        self.width = 640  
        self.height = 480  
        # x y coordinates from draw bounding box on frame
        self.x1 = x1  
        self.y1 = y1 
        self.x2 = x2
        self.y2 = y2

    def calculate(self):
        # Calculate the cone dimensions in pixels and cm
        avg_f = (self.fx + self.fy) / 2
        pix_per_mm = avg_f / self.EFL
        cone_dim_pixel = abs(self.x1 - self.x2) # Size of one side in pixels
        native_resolution_mm = self.native_resolution[0] * 25.4 # conversion into mm
        conversion_to_lower_resolution = (self.width * pix_per_mm) / native_resolution_mm
        object_size_in_CMOS = (cone_dim_pixel) / conversion_to_lower_resolution
        dist_to_cone = (self.true_reciever_dimension * self.EFL) / object_size_in_CMOS

        # Output intermediate results
        print(f"\nCorner 1: ({self.x1}, {self.y1})")
        print(f"Corner 2: ({self.x2}, {self.y2})")
        print("Pixels Length Between Corners: " + str(cone_dim_pixel))
        print("Distance to cone: " + str(dist_to_cone) + " mm")
        print("")

        return dist_to_cone





