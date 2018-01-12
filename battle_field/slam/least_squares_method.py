import logging

LOG = logging.getLogger("least_squares_method")


# input: list of tuples - [(x1,y1), (x2,y2), ... ]
# output: (k, b) if line is y=kx+b or (x value) if line is x=3
# None if count of dots == 0
def approximate_line(dots):
    x_sum = 0
    y_sum = 0
    x_square_sum = 0
    xy_sum = 0
    count_of_dots = len(dots)
    if count_of_dots == 0:
        return None
    k = 0
    b = 0
    for dot in dots:
        x_sum += dot[0]
        y_sum += dot[1]
        x_square_sum += dot[0] * dot[0]
        xy_sum += dot[0] * dot[1]
    x_sum_square = x_sum * x_sum
    # we have vertical line x = ...
    if count_of_dots * x_square_sum == x_sum_square:
        return dots[0]
    # we have y = kx + b line
    else:
        k = (
            count_of_dots * (xy_sum) - x_sum * y_sum) / (
            count_of_dots * x_square_sum - x_sum_square)
        b = (y_sum - k * x_sum) / count_of_dots
        return (k, b)
