import numpy as np
import matplotlib.pyplot as plt

# IMPORTANT NOTE
# File "Economic_Data.py" must be downloaded to same directory as this file.

def plant_costs(
        grid_size = 1000e6,
        reactor_power = 1000e6, 
        thermal_storage_size = 1000e6, 
        turbine_size = 500e6, 
        generator_size = 500e4, 
        max_ramp_up_rate = 30e6,
        solar_excess = 0):
    
    # Sample grid information.
    out_text ="*** GRID INFORMATION TABLE ***\n"
    out_text+=" Reactor Power Needed:   {:10.3e} MW_e\n"  .format(reactor_power/1e6)
    out_text+=" Thermal Storage Needed: {:10.3e} MW_th*h\n".format(thermal_storage_size/1e6)
    out_text+=" Turbine Size Needed:    {:10.3e} MW_th\n"  .format(turbine_size/1e6)
    out_text+=" Generator Size Needed:  {:10.3e} MW_e\n"   .format(generator_size/1e6)
    out_text+=" Max Ramp Up Rate:  {:10.3e} MW_e/min\n"   .format(max_ramp_up_rate/(60 * 1e6))
    print(out_text)
    print('')
    
    # Import functions.
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
    
    # Testing bypass
    bypass = yes_no('Would you like to bypass user inputs in order to test code (YES/NO)?: ')
    print('')
    
    # Scaling factor
    SF = grid_size/1000e6
    
    # Chooses which type of fuel salt to use.
    nuc_salt = nuc_salt_cost(bypass, 0, 0, 0, 'YES')
    prim_salt = SF * nuc_salt[0]
    sec_salt = SF * nuc_salt[1]
    
    # Chooses what type of coolant salt to use.
    storage_costs = storage_salt_cost(thermal_storage_size, bypass, 0, 0, 'MAYBE', 'YES')
    storage_costs = SF * storage_costs[0]
    
    # Overnight costs
    overnight = SF * overnight_cost('YES')
    
    # Fuel costs
    fuel_costs = SF * fuel_cost('YES')
    
    # Can costs
    can_cost = can_cost(bypass, 0, 'YES')
    can_cost = SF * can_cost[0]
    
    # Chooses what turbine model to use.
    turbine_price = turbine_cost(bypass, turbine_size, 0, 'YES')
    turbine_price = turbine_price[0]
    
    # Chooses what generator model to use.
    generator_price = generator_cost(bypass, generator_size, 0, 'YES')
    generator_price = generator_price[0]
        
    # Determine licensing cost
    if bypass.upper() == 'NO':
        license = SF * float_check('Licensing cost: $')
    else:
        license = SF * 100e6

    # Determines plant labor costs.
    if bypass.upper() == 'NO':
        labor_force = int_check('Number of people working at plant(s): ')
    else:
        labor_force = np.sqrt(SF) * 209 # Estimate from ThorCon website
    if bypass.upper() == 'NO':
        avg_salary = float_check('Average annual salary of workforce: $')
    else:
        avg_salary = 150e3
    labor_cost = labor_force * avg_salary
    print('Yearly labor costs: $', labor_cost)
    
    # Determines the startup cost of the facility based on choices.
    # TODO: make sure all costs modeled are covered
    facility_cost = turbine_price + generator_price + overnight + can_cost + license
    salt_cost = prim_salt + sec_salt + storage_costs
    initial_cost = facility_cost + salt_cost + fuel_costs[0]
    
    # Input expected yearly revenue.
    if bypass.upper() == 'NO':
        sell_opt = yes_no('Do you have a price that power will be sold at (YES/NO)?: ')
    else:
        sell_opt = 'YES'
    if sell_opt.upper() == 'YES':
        if bypass.upper() == 'NO':
            pwr_cost = float_check('Selling power at [cents/kWh]: ')
        else:
            pwr_cost = 10
        yearly_rev = (pwr_cost / 100) * ((reactor_power * 24 * 365) / 1000)
    else:
        yearly_rev = float_check('Expected yearly revenue: $')
    print('Yearly revenue is: $', yearly_rev)
    
    # Determine plant life in years.
    if bypass.upper() == 'NO':
        work_length = float_check('Working life of the plant (years): ')
    else:
        work_length = 60
    
    # Initial facility cost
    print('Overnight capital cost:', initial_cost / (reactor_power / 1000), '$/kW.')
    print('Initial facility cost: $', initial_cost)
    
    # Determines if a loan is used.
    loan_opt = yes_no('Will a loan be used (YES/NO)?: ')
    
    # If a loan is taken.
    if loan_opt.upper() == 'YES':
        
        loan_amount = float_check('Loan amount: $') # Loan principal
        print('Loan is: $', loan_amount)
        
        r_hundred = float_check('Enter the annual interest rate (%): ')
        r = r_hundred/100.0
        print('Annual interest rate: ', r_hundred, '%')
        
        n = float_check('Enter number of yearly payments: ')
        print('Interest compounded ', n, 'times per year.')
        
        t = float_check('Length of loan (years): ')
        print('Length of loan: ', t, ' years.')
        term_num = n*t               # Number of loan terms
        term_rate = r/n              # Interest rate for each term
        
        loan_mcost = (loan_amount*term_rate)/(1-(1+(term_rate))**(-term_num)) # Monthly loan cost
        loan_tot = loan_mcost * term_num
        loan_ycost = loan_tot / t
        loan_interest = loan_tot - loan_amount
        initial_cost = initial_cost - loan_amount
        print('Initial facility cost with loan: $', initial_cost)
        print('Interest on loayen: $', loan_interest)
        
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
            can_replace = replace(can_cost, can_check, 4)
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
            debt = replacements + labor_cost + loan_ycost # Plant costs [$]
            life_cost.append(debt)
        life_cost[-1] = (initial_cost + loan_amount) * 0.1 + loan_remainder  #10% to decommision cost
        life_cost = np.array(life_cost) / (reactor_power * 24 * 365.25 / 1000)

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
            can_replace = replace(can_cost, can_check, 4)
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
            debt = replacements + labor_cost # Plant costs [$]
            life_cost.append(debt)
        life_cost[-1] = initial_cost * 0.1  #10% to decommision cost
        life_cost = np.array(life_cost) / (reactor_power * 24 * 365.25 / 1000)
    
    # Graphing
    # TODO: add monthly revenue plot, make plots look better, find break even point
    year = np.linspace(0, int(work_length),len(life_cost))
    plt.semilogy(year,life_cost,ls='-', marker='.', c='r', markersize=6)
    plt.xlabel('Time (years)', fontsize=14)                
    plt.ylabel('Costs ($/kWh)', fontsize=14)
    plt.tight_layout()
    print('Total lifetime costs: $', sum(life_cost))
    plt.savefig('Lifetime Costs')
    return
