# import datascience as ds
import numpy as np
#
# def standard_units(arr):
#     return (arr - np.mean(arr))/np.std(arr)
#
# def correlation(t, x, y):
#     x_standard = standard_units(t.column(x))
#     y_standard = standard_units(t.column(y))
#     return np.mean(x_standard * y_standard)
#
# def slope(t, x, y):
#     r = correlation(t, x, y)
#     y_sd = np.std(t.column(y))
#     x_sd = np.std(t.column(x))
#     return r * y_sd  / x_sd
#
# def intercept(t, x, y):
#     x_mean = np.mean(t.column(x))
#     y_mean = np.mean(t.column(y))
#     return y_mean - slope(t, x, y)*x_mean
#
# def fit_line(tbl):
#     x = tbl.column(0)
#     y = tbl.column(1)
#     r = correlation(tbl, 0, 1)
#     slope = r*(np.std(y)) / np.std(x)
#     intercept = np.mean(y) - slope * np.mean(x)
#     return ds.make_array(slope, intercept)

