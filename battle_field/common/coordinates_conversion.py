import logging
import math

LOG = logging.getLogger("coordinates_conversion")


# input value:
# (range, heading in degrees)
# offset (x, y) -> pos of lidar for example
# output values:
# (x, y)
def convert_polar_to_cartesian_with_offset(coord, offset):
    cartesian = convert_polar_to_cartesian(coord)
    cartesian_with_offset = (
        offset[0] + cartesian[0], offset[1] + cartesian[1])
    return cartesian_with_offset


# input value - (range, heading in degrees)
# output value - (x, y)
def convert_polar_to_cartesian(coord):
    cartesian = (coord[0] * math.cos(
        math.radians(- coord[1])),
        coord[0] * (math.sin(
            math.radians(- coord[1]))))
    return cartesian


# input value - (x, y)
# output value - (range, heading in degrees)
def convert_cartesian_to_polar(coord):
    dist = math.sqrt(math.pow(coord[0], 2) + math.pow(coord[1], 2))
    heading = math.degrees(math.atan2(-coord[1], coord[0]))
    cartesian = (dist, heading)
    return cartesian
