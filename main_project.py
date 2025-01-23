'''
Final Project
Nan Xiao (Kim)
CS5001 Afternoon session
2024-12-09
Description: Apartment Rental Filtering and Ranking Program
'''
from helper_functions import * # import all the functions from the other file
import pandas as pd 


# Read in Data
file_path = 'apartment list.xlsx'
apt_list = pd.read_excel(file_path)

# Main code starts here!
def main():
    # Options dictionary
    user_full_options_dict = {
    1: 'Distance to the Roux',
    2: 'Bus Time',
    3: 'Drive Time',
    4: 'Size',
    5: 'Price',
    6: 'Room layout',
    7: 'Bath/Bedroom Ratio',
    8: 'Safety Level',
    9: 'Restaurant in range',
    10: 'Food market in Range',
    11: 'Utilities Covered',
    12: 'Pet allowed'
    }
    print("Welcome! Let's find the perfect apartment for you.")
    for k, v in user_full_options_dict.items():
        print(f"{k}: {v}") 
    #dealbreakers = [] 
    dealbreakers = get_dealbreakers(user_full_options_dict) #this function will get user's choice of dealbreakers and
    # return a list of keys of user_full_options_dict
    confirm = input("Are you sure about these choices? (y/n): ").strip().lower()
    if confirm != 'y':
        print("\nLet's start again.")
        print()
        return main() #restart the main() function if user wants to re-enter
    
    new_df = apt_list # starting point, keep updating going through the parallel if statements
    new_df = new_df.copy() # very important!
    '''The new_df is a complete, standalone copy.
	new_df.copy() makes sure when modify new_df, we're not affecting the original DataFrame.'''
    # get a bunch of "if statement" to check what filter criterion should execute and function should be called
    if 1 in dealbreakers: # check if key1 of user_input is in the [dealbreakers].
        flag_ = False # avoid using break
        while not flag_: #
            try:
                max_distance = int(input(f"Max distance from the Roux in miles?" #get user input for filter max limit
                                        f"Range:{new_df['Distance to the Roux'].min()} - {new_df['Distance to the Roux'].max()}:"))
                                           # display available choices/values left in the column
                if new_df['Distance to the Roux'].min() <= max_distance <= new_df['Distance to the Roux'].max(): #error handling:make sure in range
                    new_df = filter_with_max(new_df,'Distance to the Roux',max_distance) #call max_filter function
                    if new_df.empty: # error handling: after going through filter several rounds, there might be no apt available to choose
                        print("No apartment left in choice. Now we will have to restarting the program...")
                        main()  # Call main() to restart the process
                        return
                    flag_ = True #break
                else:
                    print(f"Sorry, we don't have any apartments in that range.") 
            except ValueError:
                print("Please enter a valid integer.")

    # the following loop and functions works similarly to the first one 
    if 2 in dealbreakers:
        flag_ = False
        while not flag_:
            try:
                max_bus_time = int(input(f"Max limit for bus travel time?"
                                        f"Range:{new_df['Bus Time'].min()} - {new_df['Bus Time'].max()}:"))
                if new_df['Bus Time'].min() <= max_bus_time <= new_df['Bus Time'].max():
                    new_df = filter_with_max(new_df, 'Bus Time', max_bus_time)
                    if new_df.empty:
                        print("No apartment left in choice. Now we will have to restarting the program...")
                        main()  # Call main() to restart the process
                        return
                    flag_ = True
                else:
                    print(f"Sorry, we don't have any apartments in that range.")
            except ValueError:
                print("Please enter a valid integer.")

    if 3 in dealbreakers:
        flag_ = False
        while not flag_:
            try:
                max_drive_time = int(input(f"Max limit for driving time?"
                                        f"Range:{new_df['Drive Time'].min()} - {new_df['Drive Time'].max()}:")) 
                if new_df['Drive Time'].min() <= max_drive_time <= new_df['Drive Time'].max():
                    new_df = filter_with_max(new_df, 'Drive Time', max_drive_time)
                    if new_df.empty:
                        print("No apartment left in choice. Now we will have to restarting the program...")
                        main()  # Call main() to restart the process
                        return
                    flag_ = True
                else:
                    print(f"Sorry, we don't have any apartments in that range.")
            except ValueError:
                print("Please enter a valid integer.")
        
    if 4 in dealbreakers:
        flag_ = False
        while not flag_:
            try:
                min_size = int(input(f"Min size of the apartment?"
                                    f"Range:{new_df['Size'].min()} - {new_df['Size'].max()}:"))
                if new_df['Size'].min() <= min_size <= new_df['Size'].max():
                    new_df = filter_with_min(new_df, 'Size', min_size)
                    if new_df.empty:
                        print("No apartment left in choice. Now we will have to restarting the program...")
                        main()  # Call main() to restart the process
                        return
                    flag_ = True
                else:
                    print(f"Sorry, we don't have any apartments in that range.")
            except ValueError:
                print("Please enter a valid integer.")
   
        
    if 5 in dealbreakers:
        flag_ = False
        while not flag_:
            try:
                max_price = int(input(f"What\'s the max price you can take?"
                                    f"Range from ${new_df['Price'].min()} - ${new_df['Price'].max()}: "))
                if new_df['Price'].min() <= max_price <= new_df['Price'].max():
                    new_df = filter_with_max(new_df, 'Price', max_price)
                    if new_df.empty:
                        print("No apartment left in choice. Now we will have to restarting the program...")
                        main()  # Call main() to restart the process
                        return
                    flag_ = True
                else:
                    print(f"Sorry, we don't have any apartments in that price range.")
            except ValueError:
                print("Please enter a valid integer.")
        
    if 6 in dealbreakers:
        flag_ = False
        while not flag_:
            try:
                user_layout = int(input("What's your ideal room layout? Enter 0 for Studio, 11 for 1B1B, 22 for" 
                                    "2B2B, 21 for 2B1B or 32 for 3B2B."))
                new_df = filter_with_conditions(new_df, user_layout)
                if new_df.empty:
                    print("No apartment left in choice. Now we will have to restarting the program...")
                    main()  # Call main() to restart the process
                    return
                if user_layout in [0,11,22,21,32]:
                    flag_ = True
                else:
                    print(f"Sorry, please re-enter a valid input.")
            except ValueError:
                print("Please enter a valid integer.")


    if 7 in dealbreakers:
        flag_ = False
        while not flag_:
            try:
                user_ratio = float(input(f"Min bathroom and bedroom ratio?" 
                                        f"Range: {new_df['Bath/Bedroom Ratio'].min().round(2)} - {new_df['Bath/Bedroom Ratio'].max().round(2)}:"))
                if new_df['Bath/Bedroom Ratio'].min() <= user_ratio <= new_df['Bath/Bedroom Ratio'].max():
                    new_df = filter_with_min(new_df, 'Bath/Bedroom Ratio', user_ratio)
                    if new_df.empty:
                        print("No apartment left in choice. Now we will have to restarting the program...")
                        main()  # Call main() to restart the process
                        return
                    flag_ = True
                else:
                    print(f"Sorry, we don't have any apartments in this range.")
            except ValueError:
                print("Please enter a valid float.")
    
    if 8 in dealbreakers:
        flag_ = False
        while not flag_:
            try:
                min_safety = int(input(f"Safety level: 3 being the safest, 1 being the least safe neighbor?"
                                       f"Range: {new_df['Safety Level'].min()} - {new_df['Safety Level'].max()}:"))
                if new_df['Safety Level'].min() <= min_safety <= new_df['Safety Level'].max():
                    new_df = filter_with_min(new_df, 'Safety Level', min_safety)
                    if new_df.empty:
                        print("No apartment left in choice. Now we will have to restarting the program...")
                        main()  # Call main() to restart the process
                        return
                    flag_ = True
                else:
                    print(f"Sorry, please re-enter a valid input.")
            except ValueError:
                print("Please enter a valid integer.")
    
    if 9 in dealbreakers:
        flag_ = False
        while not flag_:
            try:
                min_restaurant = int(input(f"Min restaurants in the neighborhood?"
                                    f"Range:{new_df['Restaurant in range'].min()} - {new_df['Restaurant in range'].max()}:"))
                if new_df['Restaurant in range'].min() <= min_restaurant <= new_df['Restaurant in range'].max():
                    new_df = filter_with_min(new_df, 'Restaurant in range', min_restaurant)
                    if new_df.empty:
                        print("No apartment left in choice. Now we will have to restarting the program...")
                        main()  # Call main() to restart the process
                        return
                    flag_ = True
                else:
                    print(f"Sorry, we don't have any apartments in this range.")
            except ValueError:
                print("Please enter a valid integer.")
    
    if 10 in dealbreakers:
        flag_ = False
        while not flag_:
            try:
                min_market = int(input(f"Min food markets in the neighborhood?"
                                    f"Range: {new_df['Food market in range'].min()} - {new_df['Food market in range'].max()}: "))
                if new_df['Food market in range'].min() <= min_market <= new_df['Food market in range'].max():
                    new_df = filter_with_min(new_df,'Food market in range' , min_market)
                    if new_df.empty:
                        print("No apartment left in choice. Now we will have to restarting the program...")
                        main()  # Call main() to restart the process
                        return
                    flag_ = True
                else:
                    print(f"Sorry, we don't have any apartments in this range.")
            except ValueError:
                print("Please enter a valid integer.")

    if 11 in dealbreakers:
        new_df = filter_utilities(new_df) # if user chose this one, then by default filter by "yes"
        if new_df.empty:
            print("No apartment left in choice. Now we will have to restarting the program...")
            main()  # Call main() to restart the process
            return
    
    if 12 in dealbreakers:
        flag_ = False
        while not flag_:
            try:
                user_pet = input("Do you have dog(s) or cat(s)? Enter 'd' for dogs, 'c' for cats: ").strip().lower()
                if user_pet in ['d', 'c']:
                    new_df = filter_pet(new_df, user_pet)
                    flag_ = True
                else:
                    print("Invalid input. Please enter 'd' for dogs or 'c' for cats.")
            except Exception as e:
                print(f"An error occurred: {e}")
    
    print("\nThank you! We will now use this information to find the best apartment options for you.")

    if dealbreakers:
        print("\nDealbreakers:")
        for dealbreaker in dealbreakers:
            print(f"{dealbreaker}: {user_full_options_dict[dealbreaker]}")
    else:
        print("\nNo dealbreakers specified.")

    print(f"To this point, we've helped you eliminate {len(apt_list) - len(new_df)} options!")
    print(new_df)

    if new_df.empty: # check if after the filter, there's any apartment left
        print("No apartments match your col.")
        print(len(new_df))
    else:
        if len(new_df) > 1: # check if more than one apartment is found, rank them
            # only will prompt user for fixed criteria to sort the apt list
            col = ['Price', 'Size', 'Safety Level', 'Distance to the Roux']
            # Create a new dictions to store the type of each criterion(column), either 'cost' or a 'benefit'
            col_type = {
                'Price': 'cost',               # Lower price is better
                'Size': 'benefit',             # Higher sizes are better
                'Safety Level': 'benefit',     # Higher safety is better
                'Distance to the Roux': 'cost' # lower distance is better
            }
            # Get user importance scores and calculate weights
            user_weights = get_user_importance_scores(col)
            # Apply weighted scoring model, get the weighted average scores
            ranked_df = weighted_ave(new_df, col, user_weights, col_type)
        
            print("\nApartments ranked based on your importance ratings:")
            display_columns = ['ID', 'Property Name', 'Unit Number','Score']
            # also can choose to show other columns: eg:['Price', 'Size', 'Safety Level', 'Distance to the Roux']
            existing_columns = [col for col in display_columns if col in ranked_df.columns]
            print(ranked_df[existing_columns][:5].to_string(index=False)) # show the top five choices; no need to show index
        else:
            # Only one apartment, no need to rank
            print("\nOnly one apartment matched. No ranking needed.") 


if __name__ == "__main__":
    main()