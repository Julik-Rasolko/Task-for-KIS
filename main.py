from PIL import Image
import numpy as np

class Solver:
    def __init__(self, file_name: str):
        self.image = Image.open(file_name).convert('1')
        self.pixels = np.asarray(self.image)
        self.prepare()
        self.draw_winner()
        self.image = Image.fromarray(self.pixels)
        
    def print(self):
        self.image.show()
        
    def cut_empty(self, array):
        for row in array:
            counter = 0
            for pixel in row:
                if (pixel == 1):
                    counter = counter + 1
                    break
            if (counter == 0):
                print('hi')
                np.delete(array, row)
    
    def prepare(self):
        self.cut_empty(self.pixels)
        rotated_pixels = np.asarray(Image.fromarray(self.pixels).rotate(90))
        self.cut_empty(rotated_pixels)
        self.image = Image.fromarray(rotated_pixels).rotate(270)
        self.pixels = np.asarray(self.image)
    
    
    def get_boundaries(self):
        sq_bounds = np.full((9, 4, 2), [0, 0])
        i = 0
        while(self.pixels[i][0] == 0):
            i = i + 1
        sq_bounds[0][3] = [0, i - 1]
        while(self.pixels[i][0] == 1):
            i = i + 1
        sq_bounds[3][0] = [0, i]
        while(self.pixels[i][0] == 0):
            i = i + 1
        sq_bounds[3][3] = [0, i - 1]
        while(self.pixels[i][0] == 1):
            i = i + 1
        sq_bounds[6][0] = [0, i]
        sq_bounds[6][3] = [0, self.pixels.shape[0]]
        
        i = 0
        while(self.pixels[0][i] == 0):
            i = i + 1
        sq_bounds[0][1] = [0, i - 1]
        sq_bounds[0][2] = [sq_bounds[0][3][0], i - 1]
        sq_bounds[3][1] = [sq_bounds[3][0][0], i - 1]
        sq_bounds[3][2] = [sq_bounds[3][3][0], i - 1]
        sq_bounds[6][1] = [sq_bounds[6][0][0], i - 1]
        sq_bounds[6][2] = [sq_bounds[6][3][0], i - 1]
        while(self.pixels[0][i] == 1):
            i = i + 1
        sq_bounds[1][0] = [0, i]
        sq_bounds[1][3] = [sq_bounds[0][3][0], i]
        sq_bounds[4][0] = [sq_bounds[3][0][0], i]
        sq_bounds[4][3] = [sq_bounds[3][3][0], i]
        sq_bounds[7][0] = [sq_bounds[6][0][0], i]
        sq_bounds[7][3] = [sq_bounds[6][3][0], i]
        while(self.pixels[0][i] == 0):
            i = i + 1
        sq_bound[1][1] = [0, i - 1]
        sq_bound[1][2] = [sq_bound[0][3][0], i - 1]
        sq_bound[4][1] = [sq_bound[3][0][0], i - 1]
        sq_bound[4][2] = [sq_bound[3][3][0], i - 1]
        sq_bound[7][1] = [sq_bound[6][0][0], i - 1]
        sq_bound[7][2] = [sq_bound[6][3][0], i - 1]
        while(self.pixels[0][i] == 1):
            i = i + 1
        sq_bounds[2][0] = [0, i]
        sq_bounds[2][3] = [sq_bounds[0][3][0], i]
        sq_bounds[5][0] = [sq_bounds[3][0][0], i]
        sq_bounds[5][3] = [sq_bounds[3][3][0], i]
        sq_bounds[8][0] = [sq_bounds[6][0][0], i]
        sq_bounds[8][3] = [sq_bounds[6][3][0], i]
        while(self.pixels[0][i] == 0):
            i = i + 1
        sq_bounds[2][1] = i - 1
        sq_bounds[2][2] = [sq_bounds[0][3][0], i - 1]
        sq_bounds[5][1] = [sq_bounds[3][0][0], i - 1]
        sq_bounds[5][2] = [sq_bounds[3][3][0], i - 1]
        sq_bounds[8][1] = [sq_bounds[6][0][0], i - 1]
        sq_bounds[8][2] = [sq_bounds[6][3][0], i - 1]
        return sq_bounds
    
    def get_shape(self, bounds):
        for i in range(bounds[0][0], bounds[3][0]):
            for j in range(bounds[0][1], bounds[1][1]):
                if (self.pixels[i][j]):
                    if (j - bounds[0][1] > (bounds[1][1] - bounds[0][1])*0.4 and
                        j - bounds[0][1] < (bounds[1][1] - bounds[0][1])*0.8):
                        return 1
                    else:
                        return 2
        return 0
    
    def draw_line(from_point, to_point):
        draw = ImageDraw.Draw(self.image)
        draw.line((from_point[0], from_point[1]), (to_point[0], to_point[1]), fill = 1, width = 3)
    
    def draw_winner(self):
        sq_bounds = self.get_boundaries()
        type = np.full(9, 0)
        for i in range(9):
            type = get_shape(sq_bounds[i])
        if (type[0] == type[1] and type[1] == type[2]):
            self.draw_line([(sq_bounds[0][0][0] - sq_bounds[0][3][0])/2, 0], 
                      [(sq_bounds[0][0][0] - sq_bounds[0][3][0])/2, self.pixels.shape[1]])
        elif (type[3] == type[4] and type[4] == type[5]):
            self.draw_line([sq_bounds[3][0][0] + (sq_bounds[3][0][0] - sq_bounds[3][3][0])/2, 0], 
                      [sq_bounds[3][0][0] + (sq_bounds[3][0][0] - sq_bounds[3][3][0])/2, self.pixels.shape[1]])
        elif (type[6] == type[7] and type[7] == type[8]):
            self.draw_line([sq_bounds[6][0][0] + (sq_bounds[6][0][0] - sq_bounds[6][3][0])/2, 0], 
                      [sq_bounds[6][0][0] + (sq_bounds[6][0][0] - sq_bounds[6][3][0])/2, self.pixels.shape[1]])
        elif (type[0] == type[3] and type[3] == type[6]):
            self.draw_line([0, sq_bounds[0][1][1] - sq_bounds[0][0][1]/2], 
                      [self.pixels.shape[0], sq_bounds[6][1][1] - sq_bounds[6][0][1]/2])
        elif (type[1] == type[4] and type[4] == type[7]):
            self.draw_line([0, sq_bounds[1][0][1] + (sq_bounds[1][1][1] - sq_bounds[1][0][1])/2], 
                      [self.pixels.shape[0], sq_bounds[1][0][1] + (sq_bounds[1][1][1] - sq_bounds[1][0][1])/2])
        elif (type[2] == type[5] and type[5] == type[8]):
            self.draw_line([0, sq_bounds[2][0][1] + (sq_bounds[2][1][1] - sq_bounds[2][0][1])/2], 
                      [self.pixels.shape[0], sq_bounds[2][0][1] + (sq_bounds[2][1][1] - sq_bounds[2][0][1])/2])
        elif (type[0] == type[4] and type[4] == type[8]):
            self.draw_line([0, 0], self.pixels.shape[0], self.pixels.shape[1])
        elif (type[2] == type[4] and type[4] == type[6]):
            self.draw_line([0, self.pixels.shape[1]], self.pixels.shape[0], 0)


if __name__ == "__main__":
    file_name = input()
    solver = Solver(file_name)
    solver.print()

