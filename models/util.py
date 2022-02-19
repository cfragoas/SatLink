import numpy as np
import math


# def curve_interpolation(x, interp, name_c1, c1, name_c2, c2):
#     c1_interp = np.interp(x, c1.index, c1)
#     c2_interp = np.interp(x, c2.index, c2)
#     delta_curve = abs(name_c1 - name_c2)
#     delta_y = abs(c1_interp - c2_interp)
#
#     if c1_interp < c2_interp:
#         delta_val = interp - name_c1
#         interpolated_point = c1_interp + delta_y * (delta_val / delta_curve)
#     elif c1_interp > c2_interp:
#         delta_val = interp - name_c2
#         interpolated_point = c2_interp + delta_y * (delta_val / delta_curve)
#     else:
#         return c2_interp
#
#     return interpolated_point

def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor



def curve_interpolation(x, interp, data):
    to_be_fitedx = []
    to_be_fitedy = []
    for i in data.columns:
        curve_interpol = np.interp(x, data.index.array, data[i].values)
        to_be_fitedx.append(float(i))
        to_be_fitedy.append(curve_interpol)

    intepolated_point = np.interp(interp, to_be_fitedx, to_be_fitedy)


    return intepolated_point

def convert_path_os(path: str) -> str: # this function convert paths to work in differents OSs
    import platform
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        path = path.replace('\\', '/')
        return path
