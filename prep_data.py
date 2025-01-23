'''
Final Project
Nan Xiao (Kim)
CS5001 Afternoon session
Description: Dataframe Preparation for Apartment Rental Filtering and Ranking Program
'''
from openpyxl import Workbook
import pandas as pd
import random

file_path = '/Users/kim/CS5001/final project/final_submission/apartment list.xlsx'
apt_list = pd.read_excel(file_path)
#print(df.head()) --> this is to check if python reads the right file, this code will 
# display first 5 rows in this file

'''
Generate random Unit Number: I used the actual property names and actual addresses, but for unit listings, I will
use the randon int method to generate, suppose each property has no more than 20 floor,
and each floor has no more than 20 rooms'''
apt_list["Unit Number"] = [f"{random.randint(1, 20):02d}{random.randint(1, 20):02d}" for _ in range(len(apt_list))]
#using list comprehension to populate the 'Unit Number' Column

#save the changes to the file
apt_list.to_excel('new_file_list.xlsx', index=False)

'''Generate Unique ID: For each apartment, we will use the address and room layout info to generate their unique ID number, later
will be applied in our housing recommendation program. each ID will be 13 characters long, with the first four characters stand
for street address, the next 2 digits stands for room layout, the next four stands for unit number, the last 3 digits
stands for zip code.
street address(4 char) --> three number digits for street number plus the street initial letter
room layout --> studio:00; 1B1B:11; 2B2B: 22; 3B2B:32; 2B1B:21 ...
unit number --> stays the same
zip code --> the last three digits of the actual zip code'''
apt_list['Address'] = apt_list['Address'].astype(str)
def generate_uniq_id(row):
    # the char values stored in excel are strings, so we can used split method to turn them into list
    address_parts = row['Address'].split()# so the street number will be [0]
    street_info = address_parts[0].zfill(3) #zfill()method zero-pads result to 3 digits if the actual street number
    # is less than 3 digits.
    street_init = address_parts[1][0].upper()
    # using dictionary to assign room layout column values as keys and assign codes as values.
    layout = {'Studio':'00', '1B1B':'11', '2B2B': '22', '3B2B':'32', '2B1B':'21'}
    layout_code = layout[row['Room layout']]
    unit_number = str(row.get('Unit Number','0')).zfill(4)
    zip_code = str(row['Zip Code'])[-3:]
    return f"{street_info}{street_init}{layout_code}{unit_number}{zip_code}"
apt_list["ID"] = apt_list.apply(generate_uniq_id, axis=1)
#apt_list.to_excel('4new_file_list.xlsx', index = False)

'''We will randomely generate the size of each apartment according to their room layout in sqft
Studios --> 400 -- 550
1B1B --> 551 -- 750
2B1B --> 650 -- 850
2B2B --> 700 -- 900
3B2B --> 800 --1000'''
def generate_size(layout):
    size_ranges = {
        "Studio": (400, 550),
        "1B1B": (551, 750),
        "2B1B": (650, 850),
        "2B2B": (700, 900),
        "3B2B": (800, 1000)
    }
    if layout in size_ranges:
        return random.randint(*size_ranges[layout]) # syntax *size_ranges[layout] unpack the dictionary value tuple
    else:
        return 
apt_list["Size"] = apt_list['Room layout'].apply(generate_size)


'''We will randomely generate the price/month of each apartment according to their room layout
Studios --> 1400 -- 2550
1B1B --> 2050 -- 2750
2B1B --> 2650 -- 2850
2B2B --> 2700 -- 2900
3B2B --> 2900 -- 3500
but if their zip code is not in 04101 area, then price will be decreased by 20%'''
apt_list['Zip Code'] = apt_list['Zip Code'].astype(str).str.zfill(5)
def generate_price(row):
    price_ranges = {
    "Studio": (1400, 2550),
    "1B1B": (2050, 2750),
    "2B1B": (2650, 2850),
    "2B2B": (2700, 2900),
    "3B2B": (2900, 3500)
}
    layout = row['Room layout']
    zip_code = row['Zip Code']
    if layout in price_ranges:
        price = row["Price"] = random.randint(*price_ranges[layout])
        if zip_code != '04101':
            return price * 0.8
        return price     
    else:
        return None
    
apt_list['Price'] = apt_list.apply(generate_price, axis = 1)
print(apt_list['Zip Code'].dtype)

def BB_ratio(row):
    layout = row['Room layout']
    if layout == 'Studio':
        return 1
    else:
        bed = int(layout[0])
        bath = int(layout[2])
        return bath/bed
apt_list['Bath/Bedroom Ratio'] = apt_list.apply(BB_ratio, axis = 1)

def restaurant(row):
    id = row['ID']
    id = int(id[0])
    if id == 0:
        return 5
    elif id == 9:
        return 2
    elif id == 6:
        return 8
    elif id == 2:
        return 9
    elif id == 1:
        return 15
    else:
        return 6
# apt_list['Restaurant in one mile'] = apt_list.apply(restaurant, axis = 1)  

def food_market(row):
    id = row['ID']
    id = int(id[0])
    if id == 0:
        return 1
    elif id == 1:
        return 4
    elif id == 9:
        return 3
    elif id == 6:
        return 2
    else:
        return 0
#apt_list['Food market in range'] = apt_list.apply(food_market, axis = 1)  

def convert_layout(row):
    layout = {'Studio':'00', '1B1B':'11', '2B2B': '22', '3B2B':'32', '2B1B':'21'}
    layout_code = layout[row['Room layout']]
    return layout_code
apt_list['Room Layout'] = apt_list.apply(convert_layout, axis = 1) 

def convert_utilities(row):
    utili_convert = {'yes':1, 'no':0}
    utili_code = utili_convert[row['Utilities Covered']]
    return utili_code
apt_list['utilities'] = apt_list.apply(convert_utilities, axis = 1) 

def convert_pet(row):
    pet_convert = {'yes':2, 'no':0, 'cat only':1}
    pet_code = pet_convert[row['Pet allowed']]
    return pet_code
apt_list['pet'] = apt_list.apply(convert_pet, axis = 1) 

apt_list.to_excel('6new_file_list.xlsx', index = False)
