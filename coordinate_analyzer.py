class CoordinateAnalyzer:
    def __init__(self, coordinates):
        self.coordinates = coordinates

    def find_extreme_coordinates(self):
        lowest_x_highest_y = 0
        highest_x_lowest_y = 0
        
        # Making sure any real x-coordinate value from the list will be smaller/larger during the first comparison
        min_x = float('inf')
        max_x = float('-inf')

        for x, y in self.coordinates:
            # This block checks if the current x-coordinate is smaller than the smallest x-coordinate found so far (min_x),
            # or if the current x-coordinate is equal to the minimum but its corresponding y-coordinate is larger than the current maximum y-coordinate in lowest_x_highest_y.
            if x < min_x or (x == min_x and (y > lowest_x_highest_y[1])):
                min_x = x
                lowest_x_highest_y = (x, y)
            
            # Conversly, this block checks if the current x-coordinate is larger than the largest x-coordinate found so far (max_x), 
            # or if the x-coordinate is equal to the maximum but its corresponding y-coordinate is smaller than the minimum y-coordinate in highest_x_lowest_y.
            if x > max_x or (x == max_x and (y < highest_x_lowest_y[1])):
                max_x = x
                highest_x_lowest_y = (x, y)

        return lowest_x_highest_y, highest_x_lowest_y


