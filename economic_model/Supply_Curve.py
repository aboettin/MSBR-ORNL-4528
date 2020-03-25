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
    # Determine Peak Solar Fraction
    peak_solar = solar_fraction(solar_grid_fraction)
    # Input Repeatable Parameters
    parameters = bypass(1)
    # Generate Supply Curve
    grid_size = np.linspace(0, max_grid_size, 1000)
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
        # Determine Nuclear and Thermal Storage Costs
        nuclear_price[i] = nuc_costs(nuclear_load, thermal_storage_size, heat_eff, parameters)
        # Total Power Costs (per kWh)
        power_price[i] = (solar_price[i] * solar_grid_fraction) + (nuclear_price[i] * (1 - solar_grid_fraction))
    plt.semilogy(power_price, grid_size, ls='-', marker='.', c='r', markersize=6)
    plt.xlabel('$', fontsize=14)                
    plt.ylabel('Q', fontsize=14)
    plt.tight_layout()
    return power_price
