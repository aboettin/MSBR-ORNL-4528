import numpy as np
import scipy
import matplotlib.pyplot as plt

def ramp_rate(
    grid_size = 1e9):
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
    solar_fract         = np.linspace(0,2.71,272)
    solar_gen           = np.copy(grid_load)    # Create array for solar generation
    plant_load          = np.copy(grid_load)    # Create array for plant load
    solar_excess        = np.copy(grid_load)    # Create array for excessive solar
    max_ramp_up_rate    = np.zeros(len(solar_fract))
    solar_contribution  = np.zeros(len(solar_fract))
    solar_excess_energy = np.zeros(len(solar_fract))
    excess_start_index = 0
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
                solar_excess[hour] = 0
            else: 
                plant_load[hour]   = 0.0
                solar_excess[hour] =-1.0*my_reduced_load
        for hour in range(0,23):            # Forward differentiation
            my_ramp_rate = (plant_load[hour+1] - plant_load[hour])/1
            if my_ramp_rate > max_ramp_up_rate[i]:
                max_ramp_up_rate[i] = my_ramp_rate
        solar_excess_energy[i] = 0
        for j in range(len(solar_excess)-1): # Trapezoidal rule integration
            solar_excess_energy[i] = solar_excess_energy[i] + ((solar_excess[j] + solar_excess[j+1])/2)
        solar_contribution[i] = sum(solar_gen)/sum(grid_load)
        if solar_excess_energy[i] > 0 and excess_start_index == 0:
            excess_start_index = i
        if solar_contribution[i] > 1:
            max_ramp_up_rate[i]   = -1
            solar_excess_energy[i]   = -1
            solar_contribution[i] = -1
            tot_solar             = (solar_fract[i])*100
    solar_contribution = solar_contribution[solar_contribution>=0]
    max_ramp_up_rate   = max_ramp_up_rate[max_ramp_up_rate>=0]
    solar_excess_energy   = solar_excess_energy[solar_excess_energy>=0]
    plt.plot(100*solar_contribution,max_ramp_up_rate/1e6)
    plt.xlabel('Total Solar Contribution to Grid (%)', fontsize=14)                
    plt.ylabel('Maximum Ramp Rate (MW/hr)', fontsize=14)
    plt.show()
    plt.semilogy(100*solar_contribution,solar_excess_energy/1e6)
    plt.xlabel('Total Solar Contribution to Grid (%)', fontsize=14)                
    plt.ylabel('Solar Excess (MW-hr)', fontsize=14)
    plt.tight_layout()
    plt.show()
    min_ramp = np.min(max_ramp_up_rate)
    min_ramp_index = np.where(max_ramp_up_rate == min_ramp)
    solar_min_ramp = 100*solar_contribution[min_ramp_index]
    excess_start = 100*solar_contribution[excess_start_index]
    print('Complete solar contribution occurs when solar is', tot_solar, '% of peak power demand.')
    print('')
    print('Minimum ramp rate occurs when solar is',solar_min_ramp[-1],'% of peak power demand.')
    print('')
    print('Excess power is produced when solar is at least',excess_start,'% of peak power demand.')
    print('')
    print('At complete solar contribution, there is',solar_excess_energy[-1]/1e6,'MW-hr of excess energy or',100*solar_excess_energy[-1]/(grid_size*24),'% of the grid size.')
    return 100*solar_contribution, max_ramp_up_rate/1e6, solar_excess_energy/1e6
a=ramp_rate()
