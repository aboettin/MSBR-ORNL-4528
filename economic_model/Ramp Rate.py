# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 14:27:09 2020

@author: alexb
"""

import numpy as np
import scipy
import matplotlib.pyplot as plt

def ramp_rate(
    grid_size   = 1e9) :
    '''Calculates size of the plants components and related parameters
    Input: 
        grid_size   = 1e9   # grid max load [W_e]
    Outputs:
        Graph of maximum ramp rate as a function of total solar contribution.'''
# Constants
    solar_hour_start =  7.50 # Sun shines from 
    solar_hour_end   = 18.50 # Sun shines until
# Hardcoded to remove dependency on another file
    grid_load = np.array([ 16091., 15248., 14836., 14629., 14825., 15944.,
  17230., 17736., 18892., 20392., 21913., 23394., 24676., 25493.,  25946., 
  26024., 25920., 25235., 24245., 24099., 23131., 21516., 19551., 17928.]) 
# Normalize to power load
    grid_load /= scipy.amax(grid_load) # Normalized max grid_load to 1
    grid_load *= grid_size             # Normalized max grid_load to grid_size
# Add solar; plant load is difference between grid load and solar generation
    solar_gen          = np.copy(grid_load)    # Create array for solar generation
    plant_load         = np.copy(grid_load)    # Create array for plant load
    solar_fract        = np.linspace(0,1,101)
    max_ramp_up_rate   = np.zeros(len(solar_fract))
    solar_contribution = np.zeros(len(solar_fract))
    for i in range(len(solar_fract)):
        for hour in range(0,24):
            if hour <= solar_hour_start or hour >= solar_hour_end: 
                solar_gen[hour] = 0.0
            else:
                sun_phase =  np.pi * \
                (hour - solar_hour_start)/(solar_hour_end -solar_hour_start)
                solar_gen[hour] = solar_fract[i] * grid_size * np.sin(sun_phase)
            my_reduced_load = grid_load[hour] - solar_gen[hour]   # Solar load reduces plant load
            if my_reduced_load >= 0:
                plant_load[hour]   = my_reduced_load
            else: 
                plant_load[hour]   = 0.0
        load_max = scipy.amax(plant_load)
        for hour in range(0,23):            # Forward differentiation
            my_ramp_rate = (plant_load[hour+1] - plant_load[hour]) / load_max
            if my_ramp_rate > max_ramp_up_rate[i]:
                max_ramp_up_rate[i] = my_ramp_rate
        solar_contribution[i] = sum(solar_gen)/sum(grid_load)
    plt.plot(100*solar_contribution,max_ramp_up_rate*100)
    plt.xlabel('Solar Contribution to Grid (%)', fontsize=14)                
    plt.ylabel('Maximum Ramp Rate (%/hr)', fontsize=14)
    #plt.title('The Effect of Solar on Ramp Rate', fontsize=15)
    plt.tight_layout()
    return 100*solar_contribution, 100*max_ramp_up_rate
a=ramp_rate()