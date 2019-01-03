import itertools
from src.config import *


def dim_x_to_diff_arr(input_points, song_changing_chunks):
    y_axis_list = [point[0] for point in input_points]
    return dimension_arr_to_diff_arr(y_axis_list, song_changing_chunks)


def dim_y_to_diff_arr(input_points, song_changing_chunks):
    y_axis_list = [point[1] for point in input_points]
    return dimension_arr_to_diff_arr(y_axis_list, song_changing_chunks)


def dimension_arr_to_diff_arr(dim_arr, song_changing_chunks):
    scaled_list = scale_list(dim_arr)
    num_samples = min(song_changing_chunks, len(scaled_list))
    diff_list = pick_idxs(scaled_list, num_samples)
    return [1 + PARAM_CHANGE_FACTOR * x for x in diff_list]


def split_num(num, parts):
    """divide number to parts with thought of the remainder"""
    diff = num % parts
    base = int(num/parts)
    if diff == 0:
        return [base] * parts
    else:
        return [base+1] * diff + [base] * (parts-diff)


def scale_list(unscaled_points):
    """returns scaled points to start point and scale"""
    z_p, min_p, max_p = unscaled_points[0], min(unscaled_points), max(unscaled_points),
    scale = max_p - min_p if max_p!=min_p else 1
    return [(z_p - pnt) / scale for pnt in unscaled_points]


def pick_idxs(large_array, num_samples):
    nums_split = split_num(len(large_array), num_samples)
    idxs = list(itertools.accumulate(nums_split))
    return [large_array[i - 1] for i in idxs]
