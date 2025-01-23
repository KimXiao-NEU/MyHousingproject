'''
Final Project
Nan Xiao (Kim)
CS5001 Afternoon session
2024-12-09
Description: Apartment Rental Filtering and Ranking Program
'''
#Prompt the user to specify dealbreakers from the full preference options dictionary to filter the apt list file.
def get_dealbreakers(user_full_options_dict):
    valid = False #flag
    while not valid:
        user_input = input("Enter the numbers of any dealbreakers, separated by commas (or press Enter to skip): ").strip()
        # user doesn't have to choose for dealbreakers/filters
        if not user_input: # if nothing chosen
            return [] # will return empty list and exit 
        try: #error handling for invalid input (not even int type) or wrong formality
            dealbreaker_choices = [int(x) for x in user_input.split(",")] # list the choices
            invalid_choices = [x for x in dealbreaker_choices if x not in user_full_options_dict] # if entered integers not in dictoinary keys,
            if invalid_choices: # will return invalid input
                print(f"Invalid dealbreakers: {invalid_choices}. Please select from your chosen aspects.") 
            else:
                valid = True #flag
        except ValueError:
            print("Invalid input. Please enter numbers separated by commas.")
    return dealbreaker_choices #will return a list with dictionary keys


'''Here are a bunch of filter functions which will be called in the main function according to their filter type.'''
def filter_with_max(new_df, col, user_max): # filter with user's max limit
    new_df = new_df[new_df[col] <= user_max]
    return new_df


def filter_with_min(new_df, col, user_min):# filter with user's min limit
    new_df = new_df[new_df[col] >= user_min]
    return new_df


def filter_with_conditions(new_df, user_input): # only keep the apt layouts user chose
    room_layout_dict = {
        0: 'Studio',
        11: '1B1B',
        21: '2B1B',
        22: '2B2B',
        32: '3B2B'
    }
    room_layout = room_layout_dict.get(user_input) # retrieve the value associated with a given key, 
    #if invalid input, would return None
    if room_layout:
        return new_df[new_df['Room layout'] == room_layout] # return the rows matches with user_input
    else:
        print("Invalid input. Please enter a valid value.")
        return new_df # unchanged


def filter_utilities(new_df):# if user chose this one, then by default filter by "yes"
    new_df = new_df[new_df['Utilities Covered'] == 'yes']
    return new_df


def filter_pet(new_df, user_pet):# three unique entries available, when user chooses 'dog', then would filter out 
        # the ones with row_values == 'no' and 'cat only'
    if user_pet == 'd':
        return new_df[new_df['Pet allowed'] == 'yes']
    elif user_pet =='c':
        return new_df[new_df['Pet allowed'] != 'no']
    else:
        print("invalid input.")
        return new_df


def normalize_column(new_df, column, ctype):
    ''' Use of Mathematical reasoning: Min-Max normalization ( Min-Max Scaling):
rescale the data in the columns to a uniform range, in order to compare the data between columns,
the rescaling system convert the data in a column into a relative value towards the columns' max or min value,
return the data in range of [0,1],successfully removes the difference of data scale in different columns. '''
    col_min = new_df[column].min() 
    col_max = new_df[column].max()
    if col_min == col_max:
        # All values are the same
        new_df[column + '_normalized'] = 1.0 # add a column of normalized column, if all the data equals to each other,
        # then all the data will be convert to 1, because no difference occurs.
    else:
        if ctype == 'benefit': # Higher Value is better, like size, restaurants/market in range...
            # (value - min) / (max - min)
            new_df.loc[:, column + '_normalized'] = (new_df[column] - col_min) / (col_max - col_min) # add new converted-data column
            # .loc-->label based indexing, [:, column + '_normalized'] this syntax select all the rows in this new column
        elif ctype == 'cost': 
            # cost criterion: (max - value) / (max - min)
            new_df.loc[:, column + '_normalized'] = (col_max - new_df[column]) / (col_max - col_min) # Lower Value is better,	
            # .loc tells Pandas should operate on the full DataFrame, not a view or temporary copy.
        else:
            raise ValueError(f"Invalid ctype: {ctype}. Must be 'benefit' or 'cost'.")
    
    return new_df


def get_user_importance_scores(col):
        '''
        Prompt user for importance ratings (1-5) for each category(column) and let
        the user enter weights for importance for each given category of column.
        '''
        print("\nTo rank the apartments, we need to know how important each category is to you.")
        print("Rate each from 1 (not important) to 5 (very important).")
        importance = {} # created a dictionary
        for k in col: # for each column as categories
            while True:
                val = int(input(f"How important is '{k}' to you? (1-5): ").strip()) # go over the columns for ratings
                if 1 <= val <= 5: # check for valid integers
                    importance[k] = val # add user ratings as values in the dictionary 
                    break
                else:
                    print("Please enter a number between 1 and 5.")

        total = sum(importance.values()) #add up the total ratings
        weights = {k: importance[k]/total for k in col} #create another dictionary called weights, keys are column names, values are weights of 
        # the rating of each column out of total ratings
        return weights #return the weights dictionary and exit

def weighted_ave(new_df, col, weights, col_type):
    # normalize each column
    for c in col: 
        if c not in new_df.columns: # error handling check
            raise ValueError(f"Column '{c}' not found in DataFrame.")
        normalize_column(new_df, c, col_type[c]) # normalize the columns that will be used to show importance
    # compute score as dot product of normalized values and weights, which in this case is to 
    # get the weighted-average of each normalized column's scores.
    new_df = new_df.copy() # Was warned SettingWithCopyWarning, so here I created another copy not to affect the original code
    new_df['Score'] = 0 # create a new column called 'score' 
    for c in col: # going over all the columns that will be taken into account
        new_df['Score'] += new_df[c + '_normalized'] * weights[c]# which will return the weighted average scores of all the normalized columns
    # then sort the rows by score descending order 
    new_df = new_df.sort_values(by='Score', ascending=False).reset_index(drop=True) # new_df will be sorted with highest scores on the top
    return new_df
