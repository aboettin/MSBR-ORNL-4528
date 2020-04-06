import sys
import numpy as np

# Checks if input is a valid index.
def index_check(matrix, comment):
    variable = input(comment)
    attempt = 0
    while True:
        if variable.isdigit() and int(variable) <= len(matrix) - 2:
           variable = int(variable)
           break
        else:
           attempt = attempt + 1
           if attempt > 3:
               print('')
               print('ERROR: TOO MANY INPUT ATTEMPTS. EXITING PROGRAM.')
               sys.exit()
               break
           print('ERROR: INVALID INDEX')
           variable = input(comment)
           continue
    return variable

# Checks if input is a valid float.
def float_check(comment):
    variable = input(comment)
    attempt = 0
    while True:
        try:
           variable = float(variable)
        except ValueError:
           attempt = attempt + 1
           if attempt > 3:
               print('')
               print('ERROR: TOO MANY INPUT ATTEMPTS. EXITING PROGRAM.')
               sys.exit()
               break
           print('ERROR: INVALID INPUT')
           variable = input(comment)
           continue
        if float(variable) < 0:
           attempt = attempt + 1
           if attempt > 3:
               print('')
               print('ERROR: TOO MANY INPUT ATTEMPTS. EXITING PROGRAM.')
               sys.exit()
               break
           print('ERROR: INVALID INPUT')
           variable = input(comment)
           continue
        else:
           variable = float(variable)
           break
    return variable

# Checks if input is valid integer
def int_check(comment):
    variable = input(comment)
    attempt = 0
    while True:
        try:
           variable = int(variable)
        except ValueError:
           attempt = attempt + 1
           if attempt > 3:
               print('')
               print('ERROR: TOO MANY INPUT ATTEMPTS. EXITING PROGRAM.')
               sys.exit()
               break
           print('ERROR: INVALID INPUT')
           variable = input(comment)
           continue
        if int(variable) < 0:
           attempt = attempt + 1
           if attempt > 3:
               print('')
               print('ERROR: TOO MANY INPUT ATTEMPTS. EXITING PROGRAM.')
               sys.exit()
               break
           print('ERROR: INVALID INPUT')
           variable = input(comment)
           continue
        else:
           variable = int(variable)
           break
    return variable

# Checks if a "YES/NO" input is valid
def yes_no(comment):
    variable = input(comment)
    attempt = 0
    while True:
        if variable.upper() == 'YES' or variable.upper() == 'NO':
            break
        if variable.upper() == 'MAYBE':
            thermal_check = input('Is this value repeating and varying (YES/NO)?: ')
            if thermal_check.upper() == 'YES':
                break
            else:
                attempt = attempt + 1
                if attempt > 3:
                    print('')
                    print('ERROR: TOO MANY INPUT ATTEMPTS. EXITING PROGRAM.')
                    sys.exit()
                    break
                print('ERROR: INVALID ANSWER')
                variable = input(comment) 
        else:
            attempt = attempt + 1
            if attempt > 3:
                print('')
                print('ERROR: TOO MANY INPUT ATTEMPTS. EXITING PROGRAM.')
                sys.exit()
                break
            print('ERROR: INVALID ANSWER')
            variable = input(comment)
    return variable

# Replacement function. Checks for periodic replacements.
def replace(replacement, check, year):
    check = check + 1
    if check < year:
        value = 0
    else:
        value = replacement
        check = 0
    return value, check

# Estimated costs of nuclear island.
def overnight_cost(table_opt):        
    nuc_table = [['Item                  ', '  Amount   ', 'Cost per Unit [Million $]'],
                 ['__________________________________________________________________'],
                 ['Pond                          ', 1, '                    ' , 1.605],
                 ['Pond Condensers               ', 8, '                    ' , 0.206],
                 ['Silo Hall                     ', 1, '                   ' , 21.271],
                 ['PMOD Grid                     ', 4, '                    ' , 3.518],
                 ['Basement                      ', 4, '                     ', 0.76],
                 ['Can Silo Radtank              ', 8, '                    ', 1.019],
                 ['Can Silo and Membrane Wall    ', 8, '                    ', 0.711],
                 ['Fuelsalt Drain Tank, Heat Sink', 8, '                    ', 2.153],
                 ['Offgas Holdup Tanks and Silos ', 8, '                    ', 0.597],
                 ['PLP Motor/Impeller            ', 5, '                      ', 0.3],
                 ['Secondary Loop Pump           ', 5, '                    ', 0.595],
                 ['Steam Generating Cell         ', 4, '                    ', 1.778],
                 ['Secondary Heat Exchangers     ', 4, '                    ', 0.228],
                 ['Tertiary Heat Exchangers      ', 4, '                    ', 0.267],
                 ['Tertiary Loop Pump            ', 5, '                    ', 0.443],
                 ['Coolant Salt Drain Tank       ', 1, '                      ', 3.0],
                 ['Off-gas Clean-up System       ', 1, '                      ', 5.0],
                 ['Gantry Crane                  ', 1, '                     ', 15.0],
                 ['Control Room                  ', 1, '                     ', 24.0]]
    if table_opt.upper() == 'YES':
        print('ESTIMATED NUCLEAR PLANT COSTS')
        print('')
        print(np.matrix(nuc_table))
    nuc_cost = 0
    for i in range(len(nuc_table)-2):
        nuc_cost += (nuc_table[i+2][1] * nuc_table[i+2][-1]) * 1e6
    sae_table = [['Item                  ', '  Amount   ', 'Cost per Unit [Million $]'],
                 ['__________________________________________________________________'],
                 ['Land                          ', 0, '                    ', 0.005],
                 ['Steam Plant Buildings         ', 2, '                    ', 23.140],
                 ['Feedwater System              ', 2, '                   ', 37.866],
                 ['Steam Piping                  ', 2, '                   ', 24.432],
                 ['Condenser                     ', 2, '                    ', 8.609],
                 ['Cooling (misc)                ', 2, '                   ', 18.612],
                 ['Electrical                    ', 2, '                   ', 38.555],
                 ['Control Room                  ', 2, '                   ', 16.548]]
    sae_cost = 0 # Initial $100 million includes incidentals
    for i in range(len(sae_table)-2):
        sae_cost += (sae_table[i+2][1] * sae_table[i+2][-1]) * 1e6
    if table_opt.upper() == 'YES':
        print('Total Nuclear Island Costs: $', nuc_cost)
        print('')
        print('ESTIMATED STEAM AND ELECTRICAL COSTS')
        print('')
        print(np.matrix(sae_table))
        print('Total Nuclear Island Costs: $', sae_cost)
        print('')
    budget_factor = 2.5 # Presume everything will be 2.5x the price.
    cost = budget_factor * (nuc_cost + sae_cost)
    return cost    

# Estimated fuel costs.
def fuel_cost(table_opt):    
    price = [['Material', 'Price per Unit [$/kg]'],
                       ['________________________________________________'],
                       ['Uranium   ', 44.38],
                       ['U-235     ', 40159.17],
                       ['Thorium   ', 50]]
    table = [['Year', 'Initial U-235 [kg]', 'U-235 Additions [kg]', 'Thorium [kg]'],
                       ['__________________________________________________________________'],
                       ['0', '             ', 636.0, '             ', 194.0, '     ', 11964],
                       ['1', '               ', 0.0, '             ', 194.0, '         ', 0],
                       ['2', '               ', 0.0, '             ', 194.0, '         ', 0],
                       ['3', '               ', 0.0, '             ', 194.0, '         ', 0],
                       ['4', '               ', 0.0, '             ', 194.0, '         ', 0],
                       ['5', '               ', 0.0, '             ', 194.0, '         ', 0],
                       ['6', '               ', 0.0, '             ', 194.0, '         ', 0],
                       ['7', '               ', 0.0, '             ', 194.0, '         ', 0]]
    cost = np.zeros(shape=(len(table)-2,1),dtype='f')
    for i in range(len(table)-2):
        cost[i] = 5*table[i+2][2] * (0.2*price[3][-1]+0.8*price[2][-1]) + 5*table[i+2][4] * (0.2*price[3][-1]+0.8*price[2][-1]) + table[i+2][6] * price[4][-1]
    if table_opt.upper() == 'YES':
        print('ESTIMATED FUEL COSTS OVER FUEL LIFE')
        print('')
        print(np.matrix(table))
        print('Total Fuel Costs Over 8 Years: $', sum(cost))
        print('')
    return cost

# Estimated costs of can.
def can_cost(bypass, number, table_opt):   
    print('ESTIMATED CAN COSTS')
    print('')
    table = [['Material                    ', ' Amount   ', 'Units', 'Price per Unit ($)'],
                       ['_________________________________________________________________________'],
                       ['Titanium-Zirconium-Molybdenum    ', 529, '       kg                ', 50],
                       ['Synthetic Graphite            ', 162452, '       kg                ' , 20],
                       ['SUS304                         ', 94688, '       kg                 ', 4],
                       ['Graphite Rings                  ', 7099, '       kg                 ', 9],
                       ['SUS316                        ', 116999, '       kg                 ', 6],
                       ['PLP Pump                        ', 2213, '       kW                ', 75],
                       ['Heating Tape                     ', 170, '      m^2              ', 1600],
                       ['Aerogel Insulation               ', 170, '      m^2                ', 63]]
    cost = 0
    for i in range(len(table)-2):
        cost += table[i+2][1] * table[i+2][-1]
    if bypass.upper() == 'NO' and table_opt.upper() == 'YES':
        number = int_check('Number of cans used in 4 year cycle: ')
    elif bypass.upper() == 'YES' and table_opt.upper() == 'NO':
        number = number
    else:
        number = 8
    can_cost = number * cost
    if table_opt.upper() == 'YES':
        print(np.matrix(table))
        print('Total Can Costs: $', can_cost)
        print('')
    return can_cost, number

# Chooses which type of fuel salt to use.
def nuc_salt_cost(bypass, index_repeat, prim_repeat, sec_repeat, table_opt):
    # TODO: add more salts, find better pricing data, find heat capacity info
    table = [['  Salt Type', ' Index', ' Weight Composition', '  Price [$/kg]'],
                   ['______________________________________________________________'],
                   ['   NaF-BeF2' '         1' '                .54-.46            ',       35]]
    if table_opt.upper() == 'YES':
        print('NUCLEAR ISLAND SALT TYPE TABLE')
        print('')
        print(np.matrix(table))
        print('')    
    # Determines the price of the fuel salt based on a given index.
    if bypass.upper() == 'NO' and table_opt == 'YES':
        index = index_check(table, 'Enter salt index: ')
    elif bypass.upper() == 'NO' and table_opt == 'NO':
        index = index_repeat
    else:
        index = 1
    price = table[1+index][1]
    # Determines the volume of fuel salt needed.
    # TODO: find a way to determine volume based on plant size
    if bypass.upper() == 'NO' and table_opt == 'YES':
        mass_prim = float_check('Enter primary loop salt amount [kg]: ')
    elif bypass.upper() == 'NO' and table_opt == 'NO':
        mass_prim = prim_repeat
    else:
        mass_prim = 48434
    prim_cost = price * mass_prim
    if table_opt.upper() == 'YES':
        print('Primary loop salt price is: $', prim_cost)
        print('')
    if bypass.upper() == 'NO' and table_opt == 'YES':
        mass_sec = float_check('Enter secondary loop salt amount [kg]: ')
    elif bypass.upper() == 'NO' and table_opt == 'NO':
        mass_sec = sec_repeat
    else:
        mass_sec = 65034
    sec_cost = price * mass_sec
    if table_opt.upper() == 'YES':
        print('Secondary loop salt price is: $', sec_cost)
        print('')
    return prim_cost, sec_cost, mass_prim, mass_sec

# Chooses what type of coolant salt to use.
def storage_salt_cost(thermal_storage_size, bypass, index_repeat, vol_repeat, thermal_check, table_opt):
    # TODO: add more salts, find better pricing data, find heat capacity info
    table = [[['   Coolant Type' ' Index' ' Composition', '  Price [$/kg]'],                                                 ],
    ['___________________________________________________________',],
    ['NaNO3-NaNO2-KNO3' '     1''     7-48-45           ',            0.5]] 
    if table_opt.upper() == 'YES':
        print('STORAGE SALT COOLANT TABLE')
        print('')
        print(np.matrix(table))
        print('')       
    # Determines the price of the thermal storage salt based on a given index.
    if bypass.upper() == 'NO' and table_opt == 'YES':
        index = index_check(table, 'Enter thermal storage salt index: ') 
    elif bypass.upper() == 'NO' and table_opt == 'NO':
        index = index_repeat
    else:
        index = 1
    price = table[1+index][1]
    heat_mcapacity = 130 # Heat capacity of index 5 salt [J/mol]
    mol_mass = 101.1*0.45 + 84.99*0.07 + 69.00*0.48 # [g/mol]
    heat_capacity = heat_mcapacity / mol_mass
    # Determines the volume of thermal storage salt needed.
    # TODO: find a way to determine volume based on plant size
    if bypass.upper() == 'NO' and table_opt == 'YES' and thermal_check.upper() == 'MAYBE':
        thermal_check = yes_no('Would you like to calculate based on thermal storage value (YES/NO)?: ')
        if thermal_check.upper() == 'YES':
            vol = 1.1*(((thermal_storage_size*3600)/(heat_capacity*(570-344)))/1e3)
        else:
            vol = float_check('Enter thermal storage salt volume [kg]: ')
    elif bypass.upper() == 'NO' and table_opt == 'NO' and thermal_check == 'NO':
        vol = vol_repeat
    elif bypass.upper() == 'NO' and table_opt == 'NO' and thermal_check == 'YES':
        vol = 1.1*(((thermal_storage_size*3600)/(heat_capacity*(570-344)))/1e3)
    else:
        vol = 1.1*(((thermal_storage_size*3600)/(heat_capacity*(570-344)))/1e3)
    cost = price * vol
    if table_opt.upper() == 'YES':
        print('Thermal storage salt price is: $', cost)
        print('')
    return cost, index, vol, thermal_check

# Chooses what turbine model to use.
def turbine_cost(bypass, turbine_size, index_repeat, table_opt):
    # TODO: more turbine options, better pricing data
    table = [['Index   ' '  Company   '      '      Model',    '     Price [$/m^3]'],
                      ['____________________________________________________'],
                      ['    1'   '     Company A'   '       Model A        ', 0.1],
                      ['    2'   '     Company B'   '       Model B        ', 0.1],
                      ['    3'   '     Company C'   '       Model B        ', 0.1],
                      ['    4'   '     Company D'   '       Model B        ', 0.1],
                      ['    5'   '     Company E'   '       Model B        ', 0.1],
                      ['    6'   '     Company F'   '       Model B        ', 0.1]]    
    if table_opt.upper() == 'YES':
        print('TURBINE TABLE')
        print('')
        print(np.matrix(table))
        print('')  
    # Determines the turbine price based on a given index.
    # TODO: determine number of turbines based on plant size
    if bypass.upper() == 'NO' and table_opt == 'YES':
        index = index_check(table, 'Enter turbine index: ')
    elif bypass.upper() == 'NO' and table_opt == 'NO':
        index = index_repeat   
    else:
        index = 1
    cost = table[1+index][1] * turbine_size
    if table_opt.upper() == 'YES':
        print('Turbine price is: $', cost)
        print('')
    return cost, index

# Chooses what generator model to use.
def generator_cost(bypass, generator_size, index_repeat, table_opt):
    # TODO: add more generator options, better pricing data
    table = [['Index   ' '  Company   '      '      Model'      '        Cooling      ',    '     Price [$/m^3]'],
                        ['__________________________________________________________________________',],
                        ['    1'     '    Company A '     '    Model A   '      ' Air              ', 0.1],
                        ['    2'     '    Company B '     '    Model B   '      ' Air              ', 0.1],
                        ['    3'     '    Company C '     '    Model C   '      ' Air              ', 0.1]]
    if table_opt.upper() == 'YES':
        print ('GENERATOR TABLE')
        print ('')
        print(np.matrix(table))
        print ('')   
    # Determines the generator price based on a given index.
    # TODO: determine number of generators based on plant size
    if bypass.upper() == 'NO' and table_opt == 'YES':
        index = index_check(table, 'Enter generator index: ')   
    elif bypass.upper() == 'NO' and table_opt == 'NO':
        index = index_repeat
    else:
        index = 1
    cost = table[1+index][1] * generator_size
    if table_opt.upper() == 'YES':
        print('Generator price is: $', cost)
    return cost, index
