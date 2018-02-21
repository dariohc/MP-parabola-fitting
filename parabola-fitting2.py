__author__ = 'Dario Hermida'
import numpy as np
from scipy.optimize import leastsq
from scipy.optimize import curve_fit
import pylab as plt
import math
import random

# basic, plots, final_plots
debug = 'final_plots'
N = 20  # number of data points
angle = 25
measurements_erase = 15
rad_angle = angle * np.pi / 180
# generate base positions vector
t = np.linspace(200, 800, 100)
cog_compilation = []
R2_compilation = []
params_compilation = []

X_mm = [634.028, 610.93, 587.741, 564.626, 541.506,
        518.378, 495.192, 472.091, 448.88, 425.596,
        402.45, 379.32, 356.129, 332.993, 309.825,
        286.633, 263.495, 240.299, 217.181, 194.035]
# generate data measurements to be fitted
MP_inertia = [1375.3, 1364.1, 1350.3, 1339.8, 1328.1,
              1321.5, 1311.1, 1305.7, 1298.6, 1296.4,
              1292.7, 1293.9, 1293.5, 1291.3, 1300.6,
              1301.1, 1308.1, 1313.6, 1324.1, 1333.5]

def optimize_func(t, a, b, c):
    return a * t ** 2 + b * t + c

def fitting_error(params, X_mm_mod, MP_inertia_mod):
    data_fit = [params[0] * X_mm_mod[k] ** 2 + params[1] * X_mm_mod[k] + params[2] for k in range(0, len(X_mm_mod))]
    # find the minimum of the parabola using derivatives
    derivative = -params[1] / (2 * params[0])
    cog_height = derivative / math.sin(rad_angle)
    data_fit_average = sum(data_fit) / len(data_fit)
    SSR = [(data_fit[k] - data_fit_average) ** 2 for k in range(0, len(MP_inertia_mod))]
    SST = [(MP_inertia_mod[k] - data_fit_average) ** 2 for k in range(0, len(MP_inertia_mod))]
    R2_fit = sum(SSR) / sum(SST)
    if debug == 'plots':
        plt.plot(data_fit, 'r*')
        plt.plot(MP_inertia_mod, '+')
        plt.show()
    return data_fit, cog_height, SSR, SST, R2_fit

def update_values(data_fit, X_mm_mod, MP_inertia_mod):
    simple_error = [(MP_inertia_mod[k] - data_fit[k]) ** 2 for k in range(0, len(MP_inertia_mod))]
    print(simple_error)
    delete = simple_error.index(max(simple_error))
    X_mm_mod.pop(delete)
    MP_inertia_mod.pop(delete)
    simple_error.pop(delete)

    # print('to delete index:', delete)

MP_inertia_mod = MP_inertia
X_mm_mod = X_mm
for k in range(0, measurements_erase):
    params, params_covariance = curve_fit(optimize_func, X_mm_mod, MP_inertia_mod)
    # recreate the fitted curve using the optimized parameters
    data_fit, cog_height, SSR, SST, R2_fit = fitting_error(params, X_mm_mod, MP_inertia_mod)
    # compile CoGs and R2s
    print('ssts', sum(SST))
    cog_compilation.append(cog_height)
    R2_compilation.append(R2_fit)
    params_compilation.extend(params)
    if debug == 'basic' :
        print('cog_height:', cog_height)
        print('R2_fit:', R2_fit)
        print('cog_compilation:', cog_compilation)
        print('R2_compilation:', R2_compilation)
    # now we have data_fit and the MP_inertias
    update_values(data_fit, X_mm_mod, MP_inertia_mod)

if debug == 'final_plots' or 'plots':
    plt.subplot(2, 1, 1)
    plt.title('Cog_compilation')
    plt.ylabel('Cog height [mm]')
    plt.plot(cog_compilation)
    plt.subplot(2, 1, 2)
    plt.title('R2_compilation')
    plt.ylabel('Fitting ratio')
    plt.plot(R2_compilation)
    plt.show()
    print(params_compilation)