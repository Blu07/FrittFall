import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np
from scipy.optimize import curve_fit

from utils import integrate

url = "https://data.ssb.no/api/v0/no/table/03501/"
jsonQuery = {
  "query": [
    {
      "code": "Region",
      "selection": {
        "filter": "agg:KommSummer",
        "values": [
          "K-4003",
          "K-5532"
        ]
      }
    },
    {
      "code": "Aarsak",
      "selection": {
        "filter": "item",
        "values": [
          "0"
        ]
      }
    },
    {
      "code": "Dyr3",
      "selection": {
        "filter": "item",
        "values": [
          "1"
        ]
      }
    }
  ],
  "response": {
    "format": "json-stat2"
  }
}


response = requests.post(url, json=jsonQuery)
data = response.json()


#%% Behandle data

yearAfter1987 = np.array([x.split("-")[0] for x in data['dimension']['Tid']['category']['label'].values()], dtype=float) - 1987

skien = np.array(data['value'][:len(data['value'])//2], dtype=float)
balsfjord = np.array(data['value'][len(data['value'])//2:], dtype=float)


# Generate high-resolution x values for the fitted function to be plotted smoothly
high_res_years = np.linspace(yearAfter1987.min(), yearAfter1987.max(), 1000)




# #%% Behandle Balsfjord data

# def sineBalsfjord(x, a, p, x0, b, c, d, e):
#     return a * np.sin(2*np.pi/p * (x - x0)) + b*x**3 + c*x**2 + d*x + e

# balsfjordParams, _ = curve_fit(sineBalsfjord, yearAfter1987, balsfjord, p0=[2, 14, 3, 0.00045, -0.0062, 0.13, 4.0])
# fitted_balsfjord = sineBalsfjord(high_res_years, *balsfjordParams)

# fig1 = plt.figure("Balsfjord Elk Data with Sine Fit")
# fig1.gca().plot(yearAfter1987, balsfjord, label="Balsfjord Data")
# fig1.gca().plot(high_res_years, sineBalsfjord(high_res_years, *balsfjordParams), label="Fitted Sine Function")
# fig1.gca().set_xlabel("Years after 1987")
# fig1.gca().set_ylabel("Number of Elk deceased")
# fig1.gca().set_title("Balsfjord Elk Data with Fitted Sine Function")
# fig1.gca().legend()


# # Integrate the fitted Balsfjord data
# balsfjordIntegrated = integrate(fitted_balsfjord, high_res_years)

# # Calculate the total number of elk deceased since 1987 from the actual data
# balsfjordSum = [sum(balsfjord[:i+1]) for i in range(len(balsfjord))]

# fig2 = plt.figure("Balsfjord Integrated and Summed Data")
# fig2.gca().plot(high_res_years, balsfjordIntegrated, label="Balsfjord Integrated")
# fig2.gca().plot(yearAfter1987, balsfjordSum, label="Balsfjord Summed", linestyle="--")
# fig2.gca().set_xlabel("Years after 1987")
# fig2.gca().set_ylabel("Total number of Elk deceased since 1987")
# fig2.gca().set_title("Integrated Balsfjord Elk Data")
# fig2.gca().legend()


# # Derive the Balsfjord data
# skienDerived = np.gradient(fitted_balsfjord)
# fig3 = plt.figure("Balsfjord Derived Data")
# fig3.gca().plot(high_res_years, skienDerived, label="Skien Derived")
# # add points and text for x-value where the derived value is zero
# fig3.gca().hlines(0, high_res_years.min(), high_res_years.max(), colors='red', linestyles='--', label="y=0 Line")
# zero_crossings = np.where(np.diff(np.sign(skienDerived)))[0]
# for zero in zero_crossings:
#     fig3.gca().plot(high_res_years[zero], 0, 'ro')  # red points at zero crossings
#     fig3.gca().annotate(f"x = {round(high_res_years[zero], 1)}", (high_res_years[zero], 0), textcoords="offset points", xytext=(22,5), ha='center', fontsize=8)

# fig3.gca().set_xlabel("Years after 1987")
# fig3.gca().set_ylabel("Rate of change of Elk deceased")
# fig3.gca().set_title("Derived Balsfjord Elk Data")
# fig3.gca().legend()

# #%% Skien data


# def poly4(x, a, b, c, d, e):
#     return a*x**4 + b*x**3 + c*x**2 + d*x + e

# def skienPolySine(x, a, p, x0, b, c, d, e, f):
#     return a * np.sin(2*np.pi/p * (x - x0)) + b*x**4 + c*x**3 + d*x**2 + e*x + f


# # Manually remove some values before fitting. (These values are outliers and affect the fit significantly)
# # The indexes to remove are based on visual inspection of the data
# # The values will still be plotted, but not used in the fitting process
# indexes_to_remove = [10, 19, 20]
# filtered_skien = np.delete(skien.copy(), indexes_to_remove)
# filtered_years = np.delete(yearAfter1987.copy(), indexes_to_remove)


# # Fit the trend line to the Skien data
# skienFitSineParams, _ = curve_fit(skienPolySine, filtered_years, filtered_skien, [2, 8, 1, -0.00043, 0.036, -0.995, 8.79, 25.2])
# skienFitPolyParams, _ = curve_fit(poly4, filtered_years, filtered_skien, [-0.00043, 0.036, -0.995, 8.79, 25.2])

# # Generate the line values
# fitted_sine_skien = skienPolySine(high_res_years, *skienFitSineParams)
# fitted_poly_skien = poly4(high_res_years, *skienFitPolyParams)


# # fig1 = plt.figure("Skien Elk Data with Trend Line and Fitted Line")
# fig1.gca().plot(yearAfter1987, skien, label="Raw Data")
# fig1.gca().plot(high_res_years, fitted_sine_skien, label="Sine Fit", linestyle="--", color="orange")
# fig1.gca().plot(high_res_years, fitted_poly_skien, label="Poly Fit", linestyle="--", color="green")
# fig1.gca().set_xlabel("Years after 1987")
# fig1.gca().set_ylabel("Number of Elk deceased per year")
# fig1.gca().set_title("Skien Elk Data with Fitted Lines")
# fig1.gca().legend()


# # Integrate the fitted Skien data
# skienSineIntegrated = integrate(fitted_sine_skien, high_res_years)
# skienPolyIntegrated = integrate(fitted_poly_skien, high_res_years)

# # Calculate the total number of elk deceased since 1987 from the actual data
# skienSum = [sum(skien[:i+1]) for i in range(len(skien))]
# # fig2 = plt.figure("Skien Integrated and Summed Data")
# fig2.gca().plot(yearAfter1987, skienSum, label="Summed")
# fig2.gca().plot(high_res_years, skienSineIntegrated, label="Sine Fit Integrated", linestyle='--', color='orange')
# fig2.gca().plot(high_res_years, skienPolyIntegrated, label="Poly Fit Integrated", linestyle='--', color='green')
# fig2.gca().set_xlabel("Years after 1987")
# fig2.gca().set_ylabel("Total number of Elk deceased since 1987")
# fig2.gca().set_title("Integrated Skien Elk Data")
# fig2.gca().legend()



# # Derive the Skien data
# skienSineDerived = np.gradient(fitted_sine_skien)
# skienPolyDerived = np.gradient(fitted_poly_skien)

# # fig3 = plt.figure("Skien Derived Data")

# fig3.gca().plot(high_res_years, skienSineDerived, label="Sine Fit Derived", color='orange')
# fig3.gca().plot(high_res_years, skienPolyDerived, label="Poly Fit Derived", color='green')

# # # add points and text for x-value where the derived value is zero
# # fig6.gca().hlines(0, high_res_years.min(), high_res_years.max(), colors='red', label="y=0 Line")

# # # Find zero crossings in both sine and poly
# # zero_crossings_sine = np.where(np.diff(np.sign(skienSineDerived)))[0]
# # zero_crossings_poly = np.where(np.diff(np.sign(skienPolyDerived)))[0]



# # for zero in zero_crossings_sine:
# #     fig6.gca().plot(high_res_years[zero], 0, 'ro')  # red points at zero crossings
# #     fig6.gca().annotate(f"{round(high_res_years[zero], 1)}", (high_res_years[zero], 0), textcoords="offset points", xytext=(10, 5), ha='center', fontsize=8)

# # for zero in zero_crossings_poly:
# #     fig6.gca().plot(high_res_years[zero], 0, 'ro')  # red points at zero crossings
# #     fig6.gca().annotate(f"{round(high_res_years[zero], 1)}", (high_res_years[zero], 0), textcoords="offset points", xytext=(10, -10), ha='center', fontsize=8)



# fig3.gca().set_xlabel("Years after 1987")
# fig3.gca().set_ylabel("Rate of change of Elk deceased")
# fig3.gca().set_title("Derived Skien Elk Data")
# fig3.gca().legend()


# # Savefig calls at the end
# # Uncomment to save the figures
# if True:
# 	DPI = 1200
# 	fig1.savefig("matteFigures/balsfjord_fit.png", dpi=DPI, bbox_inches='tight')
# 	fig2.savefig("matteFigures/balsfjord_integrated.png", dpi=DPI, bbox_inches='tight')
# 	fig3.savefig("matteFigures/balsfjord_derived.png", dpi=DPI, bbox_inches='tight')
# 	fig1.savefig("matteFigures/skien_fit.png", dpi=DPI, bbox_inches='tight')
# 	fig2.savefig("matteFigures/skien_integrated.png", dpi=DPI, bbox_inches='tight')
# 	fig3.savefig("matteFigures/skien_derived.png", dpi=DPI, bbox_inches='tight')





#%% Define all fitting functions

def poly3(x, a, b, c, d):
    return a*x**3 + b*x**2 + c*x + d

def poly4(x, a, b, c, d, e):
    return a*x**4 + b*x**3 + c*x**2 + d*x + e

def balsfjordSine(x, a, p, x0, b, c, d, e):
    return a * np.sin(2*np.pi/p * (x - x0)) + poly3(x, b, c, d, e)

def skienSine(x, a, p, x0, b, c, d, e, f):
    return a * np.sin(2*np.pi/p * (x - x0)) + poly4(x, b, c, d, e, f)


#%% Balsfjord data

# Poly
balsfjordPolyParams, _ = curve_fit(poly3, yearAfter1987, balsfjord, p0=[0.00045, -0.0062, 0.13, 4.0])
balsfjordPolyFitted = poly3(high_res_years, *balsfjordPolyParams)

balsfjordPolyIntegrated = integrate(balsfjordPolyFitted, high_res_years)
balsfjordPolyDerived = np.gradient(balsfjordPolyFitted, high_res_years)


# Sine
balsfjordSineParams, _ = curve_fit(balsfjordSine, yearAfter1987, balsfjord, p0=[2, 14, 3, 0.00045, -0.0062, 0.13, 4.0])
balsfjordSineFitted = balsfjordSine(high_res_years, *balsfjordSineParams)

balsfjordSineIntegrated = integrate(balsfjordSineFitted, high_res_years)
balsfjordSineDerived = np.gradient(balsfjordSineFitted, high_res_years)



#%% Skien data

# Manually remove some values before fitting. (These values are outliers and affect the fit significantly)
# The indexes to remove are based on visual inspection of the data
# The values will still be plotted, but not used in the fitting process
indexes_to_remove = [10, 19, 20]
filtered_skien = np.delete(skien.copy(), indexes_to_remove)
filtered_years = np.delete(yearAfter1987.copy(), indexes_to_remove)


# Poly
skienFitPolyParams, _ = curve_fit(poly4, filtered_years, filtered_skien, p0=[-0.00043, 0.036, -0.995, 8.79, 25.2])
fitted_poly_skien = poly4(high_res_years, *skienFitPolyParams)

balsfjordSum = [sum(balsfjord[:i+1]) for i, _ in enumerate(balsfjord)]
skienPolyIntegrated = integrate(fitted_poly_skien, high_res_years)
skienPolyDerived = np.gradient(fitted_poly_skien, high_res_years)


# Sine
skienFitSineParams, _ = curve_fit(skienSine, filtered_years, filtered_skien, p0=[2, 8, 1, -0.00043, 0.036, -0.995, 8.79, 25.2])
skienSineFitted = skienSine(high_res_years, *skienFitSineParams)

skienSum = [sum(skien[:i+1]) for i, _ in enumerate(skien)]
skienSineIntegrated = integrate(skienSineFitted, high_res_years)
skienSineDerived = np.gradient(skienSineFitted, high_res_years)





figsize = (12, 9)


# Plot Skien data with fitted functions
fig1 = plt.figure("Balsfjord Elk deceased since 1987", figsize=figsize)

fig1.gca().plot(yearAfter1987, balsfjord, label="Balsfjord Data", color="#1f77b4")
fig1.gca().plot(high_res_years, balsfjordPolyFitted, label="Fitted Poly Function", linestyle="--", color="green")
fig1.gca().plot(high_res_years, balsfjordSineFitted, label="Fitted Sine Function", linestyle="--", color="orange")


fig1.gca().set_title("Elk Data with Fitted Lines")
fig1.gca().set_xlabel("Years after 1987")
fig1.gca().set_ylabel("Number of Elk deceased in Balsfjord per year")
fig1.gca().legend()


# Plot Balsfjord data with fitted functions
fig2 = plt.figure("Skien Elk deceased since 1987", figsize=figsize)

fig2.gca().plot(yearAfter1987, skien, label="Skien Data", color="#1f77b4", marker='o', markersize=3)
fig2.gca().plot(high_res_years, fitted_poly_skien, label="Fitted Poly Function", linestyle="--", color="green")
fig2.gca().plot(high_res_years, skienSineFitted, label="Fitted Sine Function", linestyle="--", color="orange")

fig2.gca().set_ylabel("Number of Elk deceased in Skien per year")
fig2.gca().set_title("Elk Data with Fitted Lines")
fig2.gca().set_xlabel("Years after 1987")
fig2.gca().legend()




#%% Integrated and Summed Data

# Balsfjord
fig3 = plt.figure("Balsfjord Integrated and Summed Data", figsize=figsize)
fig3.gca().plot(yearAfter1987, balsfjordSum, label="Data Summed", linestyle="-")
fig3.gca().plot(high_res_years, balsfjordPolyIntegrated, label="Poly Fit Integrated", linestyle='--', color='green')
fig3.gca().plot(high_res_years, balsfjordSineIntegrated, label="Sine Fit Integrated", linestyle='--', color='orange')

fig3.gca().set_title("Integrated Balsfjord Elk Data")
fig3.gca().set_xlabel("Years after 1987")
fig3.gca().set_ylabel("Total number of Elk deceased since 1987")
fig3.gca().legend()



# Skien
fig4 = plt.figure("Skien Integrated and Summed Data", figsize=figsize)
fig4.gca().plot(yearAfter1987, skienSum, label="Data Summed", linestyle="-")
fig4.gca().plot(high_res_years, skienPolyIntegrated, label="Poly Fit Integrated", linestyle='--', color='green')
fig4.gca().plot(high_res_years, skienSineIntegrated, label="Sine Fit Integrated", linestyle='--', color='orange')

fig4.gca().set_title("Integrated Skien Elk Data")
fig4.gca().set_xlabel("Years after 1987")
fig4.gca().set_ylabel("Total number of Elk deceased since 1987")
fig4.gca().legend()





#%% Derived Data

fig5 = plt.figure("Skien Derived Data", figsize=figsize)

fig5.gca().plot(high_res_years, skienSineDerived, label="Sine Fit Derived", color="orange")
fig5.gca().plot(high_res_years, skienPolyDerived, label="Poly Fit Derived", color="green")

fig5.gca().set_title("Derived Skien Elk Data")
fig5.gca().set_xlabel("Years after 1987")
fig5.gca().set_ylabel("Rate of change of Elk deceased")
fig5.gca().legend()


fig6 = plt.figure("Balsfjord Derived Data", figsize=figsize)

fig6.gca().plot(high_res_years, balsfjordSineDerived, label="Sine Fit Derived", color='orange')
fig6.gca().plot(high_res_years, balsfjordPolyDerived, label="Poly Fit Derived", color='green')

fig6.gca().set_title("Derived Balsfjord Elk Data")
fig6.gca().set_xlabel("Years after 1987")
fig6.gca().set_ylabel("Rate of change of Elk deceased")
fig6.gca().legend()




#%% Save all figures
# Savefig calls at the end
# Toggle True/False to save figures
if True:
  DPI = 1200
  fig1.savefig("matteFigures/balsfjord-data.png", dpi=DPI, bbox_inches='tight')
  fig2.savefig("matteFigures/skien-data.png", dpi=DPI, bbox_inches='tight')

  fig3.savefig("matteFigures/balsfjord-integrated.png", dpi=DPI, bbox_inches='tight')
  fig4.savefig("matteFigures/skien-integrated.png", dpi=DPI, bbox_inches='tight')

  fig5.savefig("matteFigures/skien-derived.png", dpi=DPI, bbox_inches='tight')
  fig6.savefig("matteFigures/balsfjord-derived.png", dpi=DPI, bbox_inches='tight')

