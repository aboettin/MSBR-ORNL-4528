# IMPORTANT NOTE
# File "Economic_Data.py" must be downloaded to same directory as this file.
import numpy as np
import scipy
from Economic_Data import float_check
from Economic_Data import int_check
from Economic_Data import yes_no
from Economic_Data import overnight_cost
from Economic_Data import can_cost
from Economic_Data import fuel_cost
from Economic_Data import nuc_salt_cost
from Economic_Data import storage_salt_cost
from Economic_Data import turbine_cost
from Economic_Data import generator_cost
from Economic_Data import replace

def bypass(thermal_storage_size):
    bypass = yes_no('Would you like to use default ThorCon values (YES/NO)?: ')
    if bypass.upper() == 'NO':
        nuc_info = nuc_salt_cost(bypass, 0, 0, 0, 'YES')
        storage_info = storage_salt_cost(thermal_storage_size, bypass, 0, 0, 'MAYBE', 'YES')
        can_info = can_cost(bypass, 0, 'YES')
        turbine_info = turbine_cost(bypass, 0, 'YES')
        generator_info = generator_cost(bypass, 0, 'YES')
        license_info = float_check('Licensing cost: $')
        labor_info = int_check('Number of people working at plant(s): ')
        salary_info = float_check('Average annual salary of workforce: $')
        length_info = float_check('Working life of the plant (years): ')
    else:
        nuc_info = nuc_salt_cost(bypass, 0, 0, 0, 'NO')
        storage_info = storage_salt_cost(thermal_storage_size, bypass, 0, 0, 'MAYBE', 'YES')
        can_info = can_cost(bypass, 0, 'NO')
        turbine_info = turbine_cost(bypass, 0, 'NO')
        generator_info = generator_cost(bypass, 0, 'NO')
        license_info = 100e6
        labor_info = 209
        salary_info = 150e3
        length_info = 60
    loan_opt = yes_no('Will a loan be used (YES/NO)?: ')
    if loan_opt.upper() == 'YES':        
        loan_amount = float_check('Loan amount: $')     
        r_hundred = float_check('Enter the annual interest rate (%): ')     
        n = float_check('Enter number of yearly payments: ')
        t = float_check('Length of loan (years): ')
    else:
        loan_amount = 0
        r_hundred = 1
        n = 1
        t = 1
    return nuc_info, storage_info, can_info, turbine_info, generator_info, license_info, labor_info, salary_info, length_info, loan_opt, loan_amount, r_hundred, n, t
            
def nuc_costs(
        grid_size = 1000e6,
        thermal_storage_size = 1000e6,
        efficency = 1,
        parameters = np.zeros(13)):
    
    # Testing bypass
    bypass_parameters = parameters
    
    # Scaling factor
    SF = grid_size/1000e6
    reactor_power = grid_size/efficency
    
    # Chooses which type of fuel salt to use.
    nuc_salt = bypass_parameters[0]
    prim_salt = SF * nuc_salt[0]
    sec_salt = SF * nuc_salt[1]
        
    # Chooses what type of coolant salt to use.
    storage = bypass_parameters[1]
    storage_index = storage[1]
    storage_amount = storage[2]
    storage_check = storage[3]
    storage_costs = storage_salt_cost(thermal_storage_size, 'NO', storage_index, storage_amount, storage_check, 'NO')
    storage_costs = SF * storage_costs[0]
    
    # Overnight costs
    overnight = SF * overnight_cost('NO')
    
    # Fuel costs
    fuel_costs = SF * fuel_cost('NO')
    
    # Can costs
    can_price = bypass_parameters[2]
    can_price = SF * can_price[0]
    
    # Chooses what turbine model to use.
    turbine_price = bypass_parameters[3]
    turbine_price = SF * turbine_price[0]
    
    # Chooses what generator model to use.
    generator_price = bypass_parameters[4]
    generator_price = SF * generator_price[0]
        
    # Determine licensing cost
    license = SF * bypass_parameters[5]

    # Determines plant labor costs.
    labor_force = bypass_parameters[6]
    avg_salary = bypass_parameters[7]
    labor_cost = labor_force * avg_salary
    
    # Determines the startup cost of the facility based on choices.
    # TODO: make sure all costs modeled are covered
    facility_cost = turbine_price + generator_price + overnight + can_price + license
    salt_cost = prim_salt + sec_salt + storage_costs
    initial_cost = facility_cost + salt_cost + fuel_costs[0]
        
    # Determine plant life in years.
    work_length = bypass_parameters[8]
    
    # Determines if a loan is used.
    loan_opt = bypass_parameters[9]
    
    # If a loan is taken.
    if loan_opt.upper() == 'YES':
        
        loan_amount = bypass_parameters[10]
        
        r_hundred = bypass_parameters[11]
        r = r_hundred/100.0
        
        n = bypass_parameters[12]
        
        t = bypass_parameters[13]
        term_num = n*t               # Number of loan terms
        term_rate = r/n              # Interest rate for each term
        
        loan_mcost = (loan_amount*term_rate)/(1-(1+(term_rate))**(-term_num)) # Monthly loan cost
        loan_tot = loan_mcost * term_num
        loan_ycost = loan_tot / t
        initial_cost = initial_cost - loan_amount
        
        # Calculate plant revenue throughout lifetime.
        # TODO: refine periodic costs (can replacement, salt replacement, etc.)
        time = 0
        fuel_check = 0
        can_check = 0
        prim_salt_check = 0
        sec_salt_check = 0
        tert_salt_check = 0
        life_cost = [initial_cost]
        while time <= work_length:
            
            # Increments time checks.
            time = time + 1
            fuel_check = fuel_check + 1
            
            # Fuel must be replaced every year.
            if fuel_check <= 7:
                fuel_replacement = fuel_costs[fuel_check]
            else:
                fuel_replacement = fuel_costs[0]
                fuel_check = 0
            
            # Can must be replaced every 4 years.
            can_replace = replace(can_price, can_check, 4)
            can_replacement = can_replace[0]
            can_check = can_replace[1]
            
            # Primary salt must be replaced every 8 years.
            prim_salt_replace = replace(prim_salt, prim_salt_check, 8)
            prim_salt_replacement = prim_salt_replace[0]
            prim_salt_check = prim_salt_replace[1]
                
            # Secondary salt must be replaced every 32 years.
            sec_salt_replace = replace(sec_salt, sec_salt_check, 32)
            sec_salt_replacement = sec_salt_replace[0]
            sec_salt_check = sec_salt_replace[1]
                
            # Tertiary salt must be replaced every 32 years.
            tert_salt_replace = replace(storage_costs, tert_salt_check, 32)
            tert_salt_replacement = tert_salt_replace[0]
            tert_salt_check = tert_salt_replace[1]
                 
            # Calculates loan remainder
            if time <= t:
                loan_remainder = loan_tot - loan_ycost * time
            else:
                loan_remainder = 0
                loan_ycost = 0
                
            # Calculates costs throughout plant life.
            replacements = fuel_replacement + prim_salt_replacement + sec_salt_replacement + tert_salt_replacement + can_replacement
            debt = replacements + labor_cost + loan_ycost
            life_cost.append(debt)
        life_cost[-1] = (initial_cost + loan_amount) * 0.1 + loan_remainder  #10% to decommision cost
        life_cost = np.array(life_cost) / (3600 * reactor_power * 24 / 1000)
    # If loan is not taken.
    # TODO: refine periodic costs (core replacement, salt replacement, etc.)
    else:
        time = 0
        fuel_check = 0
        can_check = 0
        prim_salt_check = 0
        sec_salt_check = 0
        tert_salt_check = 0
        life_cost = [initial_cost]
        while time <= work_length:
            
            # Increments time checks.
            time = time + 1
            fuel_check = fuel_check + 1
            
            # Fuel must be replaced every year.
            if fuel_check <= 7:
                fuel_replacement = fuel_costs[fuel_check]
            else:
                fuel_replacement = fuel_costs[0]
                fuel_check = 0
            
            # Can must be replaced every 4 years.
            can_replace = replace(can_price, can_check, 4)
            can_replacement = can_replace[0]
            can_check = can_replace[1]
            
            # Primary salt must be replaced every 8 years.
            prim_salt_replace = replace(prim_salt, prim_salt_check, 8)
            prim_salt_replacement = prim_salt_replace[0]
            prim_salt_check = prim_salt_replace[1]
                
            # Secondary salt must be replaced every 32 years.
            sec_salt_replace = replace(sec_salt, sec_salt_check, 32)
            sec_salt_replacement = sec_salt_replace[0]
            sec_salt_check = sec_salt_replace[1]
                
            # Tertiary salt must be replaced every 32 years.
            tert_salt_replace = replace(storage_costs, tert_salt_check, 32)
            tert_salt_replacement = tert_salt_replace[0]
            tert_salt_check = tert_salt_replace[1]
                
            # Calculates costs throughout plant life.
            replacements = fuel_replacement + prim_salt_replacement + sec_salt_replacement + tert_salt_replacement + can_replacement
            debt = replacements + labor_cost
            life_cost.append(debt)
        life_cost[-1] = initial_cost * 0.1  #10% to decommision cost
        life_cost = np.array(life_cost) / (3600 * reactor_power * 24 / 1000)
    
    # Graphing
    # TODO: add monthly revenue plot, make plots look better, find break even point
    nuc_cost = np.sum(life_cost)
    return nuc_cost

def solar_fraction(
    sol_fraction = 0.15):
    
# Constants
    solar_hour_start =  7.50 # Sun shines from 
    solar_hour_end   = 18.50 # Sun shines until
# Hardcoded to remove dependency on another file
    grid_load = np.array([ 16091., 15248., 14836., 14629., 14825., 15944.,
  17230., 17736., 18892., 20392., 21913., 23394., 24676., 25493.,  25946., 
  26024., 25920., 25235., 24245., 24099., 23131., 21516., 19551., 17928.]) 
# Normalize to power load
    grid_load /= scipy.amax(grid_load) # Normalized max grid_load to 1
# Add solar; plant load is difference between grid load and solar generation
    solar_fract         = np.linspace(0,2.7065,1000)
    solar_gen           = np.copy(grid_load)    # Create array for solar generation
    plant_load          = np.copy(grid_load)    # Create array for plant load
    solar_excess        = np.copy(grid_load)    # Create array for excessive solar
    max_ramp_up_rate    = np.zeros(len(solar_fract))
    solar_contribution  = np.zeros(len(solar_fract))
    solar_excess_energy = np.zeros(len(solar_fract))
    solar_index         = np.zeros(len(solar_fract))
    excess_start_index = 0
    for i in range(0, len(solar_fract)):
        for hour in range(0,24):
            if hour <= solar_hour_start or hour >= solar_hour_end: 
                solar_gen[hour] = 0.0
            else:
                sun_phase =  np.pi * \
                (hour - solar_hour_start)/(solar_hour_end -solar_hour_start)
                solar_gen[hour] = solar_fract[i] * np.sin(sun_phase)
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
        solar_index[i] = np.abs((sum(solar_gen)/sum(grid_load)) - sol_fraction)
        if solar_excess_energy[i] > 0 and excess_start_index == 0:
            excess_start_index = i
        if solar_contribution[i] > 1:
            solar_contribution[i] = 1
            solar_index[i] = 1 - sol_fraction
    idx = np.argmin(solar_index)
    solar_fraction = solar_fract[idx]
    return solar_fraction

def solar_costs(
    grid_size = 1e9,
    solar_fract = 0.87,
    production_price = 0.2,
    land_price = 500,
    storage_eff = 0.4,
    heat_eff = 0.4,
    parameters = np.zeros(13)):
    
# constants
    solar_hour_start =  7.50 # Sun shines from 
    solar_hour_end   = 18.50 # Sun shines until
# hardcoded to remove dependency on another file
    grid_load = np.array([ 16091., 15248., 14836., 14629., 14825., 15944.,
  17230., 17736., 18892., 20392., 21913., 23394., 24676., 25493.,  25946., 
  26024., 25920., 25235., 24245., 24099., 23131., 21516., 19551., 17928.]) 
# normalize to power load
    grid_load /= scipy.amax(grid_load) # normalized max grid_load to 1
    grid_load *= grid_size             # normalized max grid_load to grid_size
# add solar; plant load is difference between grid load and solar generation
    solar_gen   = np.copy(grid_load)    # create array for solar generation
    plant_load  = np.copy(grid_load)    # create array for plant load
    thermal_storage = np.copy(grid_load)    # create array for excessive solar
    for hour in range(0,24):
        if hour <= solar_hour_start or hour >= solar_hour_end: 
            solar_gen[hour] = 0.0
        else:
            sun_phase =  np.pi * \
            (hour - solar_hour_start)/(solar_hour_end -solar_hour_start)
            solar_gen[hour] = solar_fract * grid_size * np.sin(sun_phase)
        my_reduced_load = grid_load[hour] - solar_gen[hour]   # solar load reduces plant load
        if my_reduced_load >= 0:
            plant_load[hour]   = my_reduced_load
            thermal_storage[hour] = 0.0
        else: 
            plant_load[hour]   = 0.0
            thermal_storage[hour] =-1.0*my_reduced_load # count solar excess separately)
    energy = 0
    for index in range(0,23):
        energy += (1800 * (solar_gen[index] + solar_gen[index+1]))/1000
    load_avg = scipy.average(plant_load)    
    load_var = 0
    for hourlyload in np.nditer(plant_load): 
        load_var += abs(hourlyload-load_avg)
    thermal_storage_size = load_var / (2.0*storage_eff*heat_eff)
    bypass_parameters = parameters
    work_length = bypass_parameters[8]
    solar_costs = ((production_price * np.max(solar_gen)) + ((land_price * 12 * work_length * np.max(solar_gen)) / (357e6 / (365.25 * 24)))) / energy
    if solar_fract == 0:
        solar_costs = 0
    return solar_costs, load_avg, thermal_storage_size
