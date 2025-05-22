import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np
from scipy.optimize import curve_fit

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

pprint(data)

print(yearAfter1987)



# Normalize the data
# skien = skien / sum(skien)
# balsfjord = balsfjord / sum(balsfjord)



# Generate high-resolution x values for the sine function
high_res_years = np.linspace(yearAfter1987.min(), yearAfter1987.max(), 1000)




#%% Behandle Balsfjord data

def sineBalsfjord(x, a, p, x0, b, c, d, e):
    return a * np.sin(2*np.pi/p * (x - x0)) + b*x**3 + c*x**2 + d*x + e

balsfjordParams, _ = curve_fit(sineBalsfjord, yearAfter1987, balsfjord, p0=[2, 14, 3, 0.00045, -0.0062, 0.13, 4.0])


# Plot the original data and the sine function
plt.plot(yearAfter1987, balsfjord, label="Balsfjord Data")
plt.plot(high_res_years, sineBalsfjord(high_res_years, *balsfjordParams), label="Fitted Sine Function")
plt.legend()
plt.show()




#%% Skien data

# Define a linear function for the trend line
def linear_trend(x, a, b):
    return a * x + b

def poly4(x, a, b, c, d, e):
    return a*x**4 + b*x**3 + c*x**2 + d*x + e

def skienPolySine(x, a, p, x0, b, c, d, e, f):
    return a * np.sin(2*np.pi/p * (x - x0)) + b*x**4 + c*x**3 + d*x**2 + e*x + f


# Manually remove some values before fitting.

indexes_to_remove = [10, 19, 20]

filtered_skien = np.delete(skien.copy(), indexes_to_remove)
filtered_years = np.delete(yearAfter1987.copy(), indexes_to_remove)


# Fit the trend line to the Skien data
skienTrendParams, _ = curve_fit(linear_trend, filtered_years, filtered_skien)
skienFitParams, _ = curve_fit(skienPolySine, filtered_years, filtered_skien, [2, 8, 1, -0.00043, 0.036, -0.995, 8.79, 25.2])

# Generate the line values
trend_line_skien = linear_trend(yearAfter1987, *skienTrendParams)
fitted_skien = skienPolySine(high_res_years, *skienFitParams)

# Calculate the deviation (residuals) from the trend line
deviation = skien - trend_line_skien

# Plot the trend line over Skien data with deviation
plt.plot(yearAfter1987, skien, label="Skien Data")
plt.plot(yearAfter1987, trend_line_skien, label="Trend Line", linestyle="--")
# plt.fill_between(yearAfter1987, trend_line_skien - deviation, trend_line_skien + deviation, color='gray', alpha=0.3, label="Trend Deviation")
plt.plot(high_res_years, fitted_skien, label="Fitted Line", linestyle="--")
plt.legend()
plt.show()




# Define the integrate function
def integrate(array, time, start=0):
    integrated = np.zeros(len(time))
    integrated[0] = start
    for i in range(1, len(time)):
        integrated[i] = integrated[i-1] + array[i] * (time[i] - time[i-1])
    return integrated

skienIntegrated = integrate(fitted_skien, high_res_years)


plt.plot(high_res_years, skienIntegrated, label="Skien Integrated")
plt.legend()
plt.show()


skienDerived = np.gradient(fitted_skien)

plt.plot(high_res_years, skienDerived, label="Skien Derived")
plt.legend()
plt.show()






# %%
