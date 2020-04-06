import numpy as np
import scipy
import matplotlib.pyplot as plt

def power_costs(
        max_grid_size = 1000e6,
        solar_cost = 0.2,
        land_cost = 500,
        solar_grid_fraction = 0.15,
        heat_eff = 0.4,
        storage_eff = 0.4):
    # Import Functions
    from Cost_Functions import solar_fraction
    from Cost_Functions import solar_costs
    from Cost_Functions import nuc_costs
    from Cost_Functions import bypass
    # Input Repeatable Parameters
    parameters = bypass(1)
    grid_size = np.linspace(0, max_grid_size, 1000)
    # Determine Peak Solar Fraction
    peak_solar = solar_fraction(solar_grid_fraction)
    # Generate Supply Curve
    solar_price = np.zeros(len(grid_size))
    nuclear_price = np.zeros(len(grid_size))
    power_price = np.zeros(len(grid_size))
    for i in range(0, len(grid_size)):     
        # Determine Solar Costs, Thermal Storage Needs, and Average Power Load
        grid = grid_size[i]
        solar_info = solar_costs(grid, peak_solar, solar_cost, land_cost, storage_eff, heat_eff, parameters)
        solar_price[i] = solar_info[0]
        nuclear_load = solar_info[1]
        thermal_storage_size = solar_info[2]
        turbine_size = solar_info[3]
        generator_size = solar_info[4]
        # Determine Nuclear and Thermal Storage Costs
        nuclear_price[i] = nuc_costs(nuclear_load, thermal_storage_size, heat_eff, turbine_size, generator_size, parameters)
        # Total Power Costs (per kWh)
        power_price[i] = (solar_price[i] * solar_grid_fraction) + (nuclear_price[i] * (1 - solar_grid_fraction))
    #plt.semilogy(nuclear_price, grid_size, ls='-', marker='.', c='r', markersize=6)
    #plt.xlabel('$/kWh', fontsize=14)                
    #plt.ylabel('Q (W)', fontsize=14)
    #plt.tight_layout()
    #plt.savefig('Supply Curve')
    return grid_size, power_price
