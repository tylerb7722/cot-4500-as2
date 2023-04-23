# Tyler Boudreau
# Assignment 2
# COT 4500
import numpy as np
np.set_printoptions(precision=7,suppress=True,linewidth=100)


def nevilles_method(x_points, y_points, x):
    # must specify the matrix size (this is based on how many columns/rows you want)
    matrix = np.zeros((3, 3))
    
    # fill in value (just the y values because we already have x set)
    for counter, row in enumerate(matrix):
        row[0] = y_points[counter]

    # the end of the first loop are how many columns you have...
    num_of_points = len(x_points)

    # populate final matrix (this is the iterative version of the recursion explained in class)
    # the end of the second loop is based on the first loop...
    for i in range(1, num_of_points):
        for j in range(1, i + 1):
            first_multiplication = (x - x_points[i-j]) * matrix[i][j-1]
            second_multiplication = (x - x_points[i]) * matrix[i-1][j-1]

            denominator = x_points[i] - x_points[i-j]

            # this is the value that we will find in the matrix
            coefficient = (first_multiplication - second_multiplication) / denominator
            matrix[i][j] = coefficient
    print(matrix[i][j], "\n")

def divided_difference_table(x_points, y_points):
    # set up the matrix
    size: int = len(x_points)
    matrix: np.array = np.zeros((size, size))

    # fill the matrix
    for index, row in enumerate(matrix):
        row[0] = y_points[index]

    # populate the matrix (end points are based on matrix size and max operations we're using)
    for i in range(1, size):
        for j in range(1, i+1):
            # the numerator are the immediate left and diagonal left indices...
            numerator =  matrix[i][j-1] - matrix[i-1][j-1]

            # the denominator is the X-SPAN...
            denominator = x_points[i] - x_points[i-j]

            operation = numerator / denominator

            # cut it off to view it more simpler
            matrix[i][j] = operation
    return matrix

def get_approximate_result(matrix, x_points, value):
    # p0 is always y0 and we use a reoccuring x to avoid having to recalculate x 
    reoccuring_x_span = 1
    reoccuring_px_result = matrix[0][0]
    
    # we only need the diagonals...and that starts at the first row...
    for index in range(1, len(x_points)):
        polynomial_coefficient = matrix[index][index]

        # we use the previous index for x_points....
        reoccuring_x_span *= (value - x_points[index-1])
        
        # get a_of_x * the x_span
        mult_operation = polynomial_coefficient * reoccuring_x_span

        # add the reoccuring px result
        reoccuring_px_result += mult_operation

    
    # final result
    return reoccuring_px_result

def apply_div_dif(matrix: np.array):
    size = len(matrix)
    for i in range(2, size):
        for j in range(2, i+2):
            if (j >= len(matrix[i]) or matrix[i][j] != 0): # Check if value is already filled
                continue
            # Get left cell entry
            left: float = matrix[i][j-1]
            # Get diagonal left entry
            diagonal_left: float = matrix[i-1][j-1]
            numerator: float = left - diagonal_left # Calculate numerator
            # denominator is current i's x_val minus the starting i's x_val
            denominator = matrix[i][0] - matrix[i-2][0]
            operation = numerator / denominator # Perform division operation
            matrix[i][j] = operation
    return matrix

def hermite_interpolation(x_points, y_points, slopes):
    num_of_points = len(x_points)
    # Matrix size changes because of "doubling" up info for hermite
    matrix = np.zeros((num_of_points*2,num_of_points*2))
    # Fill with x values 
    for i in range(num_of_points):
        matrix[i*2][0] = x_points[i]
        matrix[i*2+1][0] = x_points[i]
    # Fill with y values 
    for i in range(num_of_points):
        matrix[i*2][1] = y_points[i]
        matrix[i*2+1][1] = y_points[i]
    # Fill with derivative values
    for i in range(num_of_points):
        matrix[i*2+1][2] = slopes[i]
    filled_matrix = apply_div_dif(matrix) # Apply divided difference method 
    print(filled_matrix,"\n")


def main():
    # Problem 1
    x_points = [3.6, 3.8, 3.9]
    y_points = [1.675, 1.436, 1.318]
    x = 3.7

    nevilles_method(x_points, y_points, x)

    # Problem 2
    x_points = [7.2, 7.4, 7.5, 7.6]
    y_points = [23.5492, 25.3913, 26.8224, 27.4589]
    divided_table = divided_difference_table(x_points, y_points)

    num_points = len(x_points)
    result = np.zeros((num_points - 1, 1))
    for i in range(1, num_points):
        result[i - 1] = divided_table[i][i]
    print(result.T[0], "\n")

    # Problem 3
    # find approximation
    approximating_x = 7.3
    final_approximation = get_approximate_result(divided_table, x_points, approximating_x)
    print(final_approximation, "\n")

    # Problem 4
    x_points = [3.6, 3.8, 3.9]
    y_points = [1.675, 1.436, 1.318]
    slopes = [-1.195, -1.188, -1.182]
    hermite_interpolation(x_points, y_points, slopes)


if __name__ == "__main__":
    main()

