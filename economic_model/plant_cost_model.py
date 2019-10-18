import numpy as np
import scipy
import matplotlib.pyplot as plt

# TODO
# Add thermal storage costs.
# Add solar contributions.
# Add more options for equipment?
# Move graphing commands to inside of function?
# More costs?
# Find better cost data?
def plant_costs(
        reactor_power = 500e6, 
        thermal_storage_size = 1000e6, 
        turbine_size = 500e6, 
        generator_size = 500e6, 
        max_ramp_up_rate = 30e6):
    
    # Sample grid information.
    out_text ="*** GRID INFORMATION TABLE ***\n"
    out_text+=" Reactor Power Needed:   {:10.3e} MW_e\n"  .format(reactor_power/1e6)
    out_text+=" Thermal Storage Needed: {:10.3e} MW_th*h\n".format(thermal_storage_size/1e6)
    out_text+=" Turbine Size Needed:    {:10.3e} MW_th\n"  .format(turbine_size/1e6)
    out_text+=" Generator Size Needed:  {:10.3e} MW_e\n"   .format(generator_size/1e6)
    out_text+=" Max Ramp Up Rate:  {:10.3e} MW_e/min\n"   .format(max_ramp_up_rate/(60 * 1e6))
    print(out_text)
    print('')
    
    # Checks if input is a valid index.
    def index_check(matrix, comment):
        variable = input(comment)
        while True:
            if variable.isdigit() and int(variable) <= len(matrix) - 2:
               variable = int(variable)
               break
            else:
               print('ERROR: INVALID INDEX')
               variable = input(comment)
               continue
        return variable
    
    # Checks if input is a valid float.
    def float_check(comment):
        variable = input(comment)
        while True:
            try:
               variable = float(variable)
            except ValueError:
               print('ERROR: INVALID INPUT')
               variable = input(comment)
               continue
            if float(variable) < 0:
               print('ERROR: INVALID INPUT')
               variable = input(comment)
               continue
            else:
               variable = float(variable)
               break
        return variable
    
    # Checks if a "YES/NO" input is valid
    def yes_no(comment):
        variable = input(comment)
        while True:
            if variable.upper() == 'YES' or variable.upper() == 'NO':
                break
            else:
                print('ERROR: INVALID ANSWER')
                variable = input(comment)
                continue
        return variable
    
    # Testing bypass
    bypass = yes_no('Would you like to bypass user inputs in order to test code (YES/NO)?: ')
    
    # Chooses which type of fuel salt to use.
    print ('FUEL SALT TYPE TABLE')
    print ('')
    salt_matrix = [['  Salt Type', ' Index', ' Composition', '  Price [$/m^3]'],
                   ['________________________________________________________'],
                   ['LiF-BeF2-UF4' '      1' '      .63-.366-.004    ',       3774.6],
                   ['LiF-BeF2-UF4' '      2' '      .636-.362-.0022  ',    1936.95],
                   ['LiF-BeF2-UF4' '      3' '      .636-.366-.004   ',     869.4],
                   ['LiF-BeF2-UF4' '      4''      .67-.18-.15      ',        522.4],
                   ['LiF-BeF2-ThF4' '     5''      .71-.02-.027     ',       2324],
                   ['LiF-BeF2-ThF4' '     6''      .63-.366-.004    ',    11776.44],
                   ['LiF-BeF2-ThF4' '     7''      .63-.366-.004    ',      34.37],
                   ['LiF-BeF2-ThF4' '     8''      .389-.611        ',          709.89],
                   ['NaBF4-NaF' '         9' '      .92-.08          ',        2068],
                   ['NaBF4-NaF' '         10' '     .389-.611        '   ,         2095]]
    print(np.matrix(salt_matrix))
    print ('')
    
    # Determines the price of the fuel salt based on a given index.
    if bypass.upper() == 'NO':
        salt_opt = index_check(salt_matrix, 'Enter salt index: ')
    else:
        salt_opt = 1
    salt_price = salt_matrix[1+salt_opt][1]
    print('Salt unit price is : ', salt_price)
    
    # Determines the volume of fuel salt needed.
    if bypass.upper() == 'NO':
        vol_salt = float_check('Enter fuel salt volume [m^3]: ')
    else:
        vol_salt = 40
    tot_salt = salt_price * vol_salt
    print ('')
    
    # Chooses what type of coolant salt to use.
    print ('SALT COOLANT TABLE')
    print ('')
    coolant_matrix = [[['  Coolant Type' ' Index' ' Composition', '  Price [$/m^3]'],                                                 ],
    ['___________________________________________________________',],
    ['NaF-KF-ZrF4' '        1' '      4-27-69              ',            11700],
    ['LiF-NaF-KF' '         2' '      29-12-59             ',          24100],
    ['LiF-NaF-BeF2' '       3' '      24-46-30             ',        35000],
    ['LiF-BeF2' '           4''      53-47                ',           52200],
    ['NaNO3-NaNO2-KNO3' '   5''      7-48-45              ',            570],
    ['NaF-NaBF4' '          6''      8-92                 ',              1500],
    ['LiCL-KCL' '           7''      59-41                ',            1800],
    ['Pb' '                 8''      1                    ',                 720],
    ['Pb-Bi' '              9' '      1                    ',             74400],
    ['Bi' '                 10' '     1                    ',                129000]] 
    print(np.matrix(coolant_matrix))
    print ('')
    
    # Determines the price of the coolant salt based on a given index.
    if bypass.upper() == 'NO':
        coolant_opt = index_check(coolant_matrix, 'Enter coolant index: ') 
    else:
        coolant_opt = 1
    coolant_price = coolant_matrix[1+coolant_opt][1]
    print('Coolant unit price is : ', coolant_price)
    
    # Determines the volume of coolant salt needed.
    if bypass.upper() == 'NO':
        vol_coolant = float_check('Enter coolant salt volume [m^3]: ')
    else:
        vol_coolant = 40
    tot_coolant = coolant_price * vol_coolant
    print ('')
    
    # Chooses what turbine model to use.
    print ('TURBINE TABLE')
    print ('')
    turbine_matrix = [['Index' '  Company'      '      Model',    '     Price [$/m^3]'],
                      ['____________________________________________________'],
                      ['  1'     '    Siemens'     '     SST-800     ',        1.55e7],
                      ['  2'     '    Siemens'   '   SST-900      ',       1.85e7],
                      ['  3'      '    Doosan'      '      MTD50         ',         1.02e6],
                      ['  4'        '      GE'     '      9F 3-series   ',      1.5e7],
                      ['  5'        '      GE'     '      9F 5-series   ',      1.75e7],
                      ['  6'       '     DTEC'      '       GMB2550r     ',      8.5e6]]    
    print(np.matrix(turbine_matrix))
    print ('')
    
    # Determines the turbine price based on a given index.
    if bypass.upper() == 'NO':
        turbine_opt = index_check(turbine_matrix, 'Enter turbine index: ')    
    else:
        turbine_opt = 1
    turbine_price = turbine_matrix[1+turbine_opt][1]
    print('Turbine price is: $', turbine_price)
    
    # Chooses what generator model to use.
    print ('GENERATOR TABLE')
    print ('')
    generator_matrix = [['Index' '  Company'      '      Model'      '              Cooling      ',    '     Price [$/m^3]'],
                        ['_______________________________________________________________________________',],
                        ['  1'     '    Siemens'     '     SGen-1000A     '      '      Air      ', 1.55e7],
                        ['  2'      '    Doosan'      '      DGEN-H         '      '  Hydrogen   ', 1.02e6],
                        ['  3'        '      GE'     '        TOPAIR   '      '         Air      ', 1.5e7]]
    print(np.matrix(generator_matrix))
    print ('')
    
    # Determines the generator price based on a given index.
    if bypass.upper() == 'NO':
        generator_opt = index_check(generator_matrix, 'Enter generator index: ')    
    else:
        generator_opt = 1
    generator_price = generator_matrix[1+generator_opt][1]
    print('Generator price is: $', generator_price)
    
    # Determines the construction material prices based on demand
    print ('CONSTRUCTION MATERIALS FOR 500 MWe REACTOR TABLE')
    print ('')
    material_matrix = [['  Material',         ' Estimated Material Amount [tons]',  '  Price [$/ton]'],
                   ['____________________________________________________________'],
                   ['High Quality Graphite [Can]', 700, 10000],
                   ['High Quality Graphite [Core]', 700, 10000],
                   ['Non-structural Concrete', 1000000, 6],
                   ['Steel', 50000, 1000]]
    print(np.matrix(material_matrix))
    print ('')
    
    # Determines construction material costs
    if bypass.upper() == 'NO':
        material_opt = yes_no('Use estimated material amounts (YES/NO)?: ')
    else:
        material_opt = 'YES'
    construction_labor = 0.25 # 25% construction labor cost.
    if material_opt.upper() == 'YES':
        tot_can = (material_matrix[2][1]*material_matrix[2][2]) * construction_labor
        tot_core = (material_matrix[3][1]*material_matrix[3][2]) * construction_labor
        tot_conc = (material_matrix[4][1]*material_matrix[4][2]) * construction_labor
        tot_steel = (material_matrix[5][1]*material_matrix[5][2]) * construction_labor
    else:
        tot_can = (material_matrix[2][1]*material_matrix[2][2]) * construction_labor
        tot_core = (material_matrix[3][1]*material_matrix[3][2]) * construction_labor
        concrete_demand = float_check('Amount of concrete needed [tons]: ')
        tot_conc = (concrete_demand * material_matrix[4][2]) * construction_labor
        steel_demand = float_check('Amount of steel needed [tons]: ')
        tot_steel = (steel_demand * material_matrix[4][2]) * construction_labor
    initial_construction_costs = tot_can + tot_core + tot_conc + tot_steel
    
    # Determine licensing cost
    if bypass.upper() == 'NO':
        license = float_check('Licensing cost: $')
    else:
        license = 100e6

    # Determines plant labor costs.
    if bypass.upper() == 'NO':
        labor_force = input('Number of people working at plant: ')
        while True:
            if labor_force.isdigit():
               labor_force = int(labor_force)
               break
            else:
               print('ERROR: INVALID INPUT')
               labor_force = input('Number of people working at plant: ')
               continue
    else:
        labor_force = 100
    if bypass.upper() == 'NO':
        avg_salary = float_check('Average annual salary of workforce: $')
    else:
        avg_salary = 100e3
    labor_mcost = labor_force * (avg_salary / 12)
    
    # Monthly operating cost of plant.
    month_cost = labor_mcost
    
    # Determines the startup cost of the facility based on choices.
    tot = turbine_price + generator_price + tot_salt + tot_coolant + initial_construction_costs + license
    initial_cost = tot
    print('Facility flat cost without loan: $', initial_cost)
    
    # Input expected monthly revenue.
    if bypass.upper() == 'NO':
        sell_opt = yes_no('Do you have a price that power will be sold at (YES/NO)?: ')
    else:
        sell_opt = 'YES'
    if sell_opt.upper() == 'YES':
        if bypass.upper() == 'NO':
            pwr_cost = float_check('Selling power at [cents/kWh]: ')
        else:
            pwr_cost = 10
        month_rev = (pwr_cost / 100) * ((reactor_power * 24 * 365) / (1000 * 12))
    else:
        month_rev = float_check('Expected monthly revenue: $')
    print('Monthly revenue is: $', month_rev)
    
    # Determine plant life in years.
    if bypass.upper() == 'NO':
        work_length = float_check('Working life of the plant (years): ')
    else:
        work_length = 60

    # Determines if a loan is used.
    if bypass.upper() == 'NO':
        loan_opt = yes_no('Will a loan be used (YES/NO)?: ')
    else:
        loan_opt = 'NO'
    
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
        
        loan_cost = (loan_amount*term_rate)/(1-(1+(term_rate))**(-term_num)) # Monthly loan cost
        loan_tot = loan_cost * term_num
        loan_mcost = loan_tot / (12 * work_length)
        loan_interest = loan_tot - loan_amount
        tot_cost = (tot-loan_amount) + loan_tot
        print('Facility real cost: $', tot_cost)
        print('Interest on loan: $', loan_interest)
        month_tot = month_cost + loan_mcost
        print('Monthly cost is: ', month_tot, ' dollars')
        
        # Calculate plant revenue throughout lifetime.
        time = 0
        fuel_check = 0
        core_check = 0
        can_check = 0
        loan_check = 'YES' # Check to see if loan is active.
        life_profit = [-initial_cost]
        while time <= work_length * 12:
            
            # Increments time checks.
            time = time + 1
            fuel_check = fuel_check + 1
            core_check = core_check + 1
            can_check = can_check + 1
            
            # Fuel salt must be replaced every 8 years.
            if fuel_check <= 8 * 12:
                fuel_salt_replacement = 0
            else:
                fuel_salt_replacement = tot_salt
                fuel_check = 0
            
            # Core graphite must be replaced every 4 years.
            if core_check <= 4 * 12:
                core_replacement = 0
            else:
                core_replacement = tot_core
                core_check = 0
            
            # Can must be replaced every 4 years.
            if can_check <= 4 * 12:
                can_replacement = 0
            else:
                can_replacement = tot_can
                can_check = 0
            
            # Subtracts loan payments after end of loan.
            if t > term_num and loan_check.upper() == 'YES':
                month_tot = month_tot - loan_mcost
                loan_check = 'NO'           
            
            # Calculates monthly profits.
            monthly_profit = month_rev - month_tot
            
            # Calculates profits throughout plant life.
            replacements = fuel_salt_replacement + core_replacement + can_replacement
            loan_remainder = loan_tot - loan_mcost * t
            if loan_remainder < 0:
                loan_remainder = 0
            tot_cost = tot_cost - monthly_profit # Amount in debt [$]
            debt = -1 * tot_cost - replacements # Money plant has made [$]
            life_profit.append(debt)
        life_profit[-1] = life_profit[-1] * 0.9 - loan_remainder  #10% to decommision cost
        print('Total revenue: $', life_profit[-1])

    # If loan is not taken.
    else:
        time = 0
        fuel_check = 0
        core_check = 0
        can_check = 0
        life_profit = [-initial_cost]
        while time <= work_length * 12:
            
            # Increments time checks.
            time = time + 1
            fuel_check = fuel_check + 1
            core_check = core_check + 1
            can_check = can_check + 1
            
            # Fuel salt must be replaced every 8 years.
            if fuel_check <= 8 * 12:
                fuel_salt_replacement = 0
            else:
                fuel_salt_replacement = tot_salt
                fuel_check = 0
            
            # Core graphite must be replaced every 4 years.
            if core_check <= 4 * 12:
                core_replacement = 0
            else:
                core_replacement = tot_core
                core_check = 0
            
            # Can graphite must be replaced every 4 years.
            if can_check <= 4 * 12:
                can_replacement = 0
            else:
                can_replacement = tot_can
                can_check = 0
            
            # Calculates monthly profits.
            monthly_profit = month_rev - month_cost
            
            # Calculates profits throughout plant life. 
            replacements = fuel_salt_replacement + core_replacement + can_replacement
            tot = tot - monthly_profit # Amount in debt [$]
            debt = -1 * tot - replacements # Money plant has made [$]
            life_profit.append(debt)
        life_profit[-1] = life_profit[-1] * 0.9  #10% to decommision cost
        print('Total revenue: $', life_profit[-1])
    
    # Graphing
    month = np.linspace(0, int(work_length)*12,len(life_profit))
    plt.semilogy(month,life_profit,ls='-', marker='.', c='r', markersize=6, label='Profit')
    plt.xlabel('Time (months)', fontsize=14)                
    plt.ylabel('Profits ($)', fontsize=14)
    plt.title('Plant Lifetime Profits', fontsize=15)
    plt.legend()
    plt.tight_layout()
    return 
