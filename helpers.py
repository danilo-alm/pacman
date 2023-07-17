import math


def get_linear_distance(a, b):
    # Get linear distance between two points
    return math.hypot(b[0] - a[0], b[1] - a[1])


def rotate(origin, point, angle):
    """ Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in radians. """
    # https://stackoverflow.com/questions/34372480/rotate-point-about-another-point-in-degrees-python
    
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy
