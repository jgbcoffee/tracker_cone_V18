# This code aims to find the center (centroid) of a polygon given any number of verticie (corner) cordinates

class FindCentroid:
    # Initialize class atributes
    def __init__(self, vertices):
        self.vertices = vertices

    # This section utlizes the shoelace method to find the area of the polygon using its verticies.
    # The theory along with the function used can be found here: https://math.stackexchange.com/questions/1702595/proof-for-centroid-formula-for-a-polygon
    def shoelace(self, vertices):
        vertices = self.vertices + [self.vertices[0]]
        n = len(vertices) - 1
        x_sum = 0
        y_sum = 0
        area = 0
        
        # Main shoelace method implemantation: https://www.theoremoftheday.org/GeometryAndTrigonometry/Shoelace/TotDShoelace.pdf
        for i in range(n):
            x0, y0 = vertices[i]
            x1, y1 = vertices[i + 1]
            cross_product = x0 * y1 - x1 * y0
            area += cross_product
            x_sum += (x0 + x1) * cross_product
            y_sum += (y0 + y1) * cross_product

        area /= 2

        # from it area and verticies sum, it then finds the center x, y coorinates.
        Cx = x_sum / (6 * area)
        Cy = y_sum / (6 * area)

        return Cx, Cy