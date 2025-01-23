'''
Final Project
Nan Xiao (Kim)
CS5001 Afternoon session
2024-12-09
Description: Testing Program for Apartment Rental Filtering and Ranking Program
'''
import unittest
import pandas as pd
from helper_functions import * # import all the functions from the other file
from unittest.mock import patch # need to mock user_input
filepath = 'test_apartment.xlsx'
class TestHelperFunctions(unittest.TestCase):

    def setUp(self):
        # read in file as an object 
        self.df = pd.read_excel(filepath)
    
    @patch('builtins.input', side_effect = ['1,2,5']) # side_effect is a keyword argument, as mock user inputs
    def test_get_dealbreakers(self,user_full_options_dict):
        user_full_options_dict = {1: 'Price', 2: 'Size', 3: 'Safety Level', 4:'Distance to the Roux', 5:'Room layout'}
        result = get_dealbreakers(user_full_options_dict)
        self.assertEqual(result, [1, 2, 5]) # should return the same values as what user entered

    @patch('builtins.input', side_effect = ['']) #test for empty string
    def test_get_dealbreakers(self,user_full_options_dict):
        user_full_options_dict = {1: 'Price', 2: 'Size', 3: 'Safety Level', 4:'Distance to the Roux', 5:'Room layout'}
        result = get_dealbreakers(user_full_options_dict)
        self.assertEqual(result, [])
    
    @patch('builtins.input', side_effect=['a','1,2']) # first test for invalid, second time user input = [1,2]
    def test_get_dealbreakers(self,user_full_options_dict):
        user_full_options_dict = {1: 'Price', 2: 'Size', 3: 'Safety Level', 4:'Distance to the Roux', 5:'Room layout'}
        result = get_dealbreakers(user_full_options_dict)
        self.assertEqual(result, [1,2])

    def test_filter_with_max(self): # test with max limit too low, then return empty series(in pandas, [] isn't a list)
        filtered_df = filter_with_max(self.df, 'Price', 1000)
        self.assertEqual((filtered_df['Price'] <= 1000),[]) 
    
    def test_filter_with_max(self):# test with a number would filter 2 numbers out in the series
        filtered_df = filter_with_max(self.df, 'Price', 2000)
        self.assertTrue((filtered_df['Price'] <= 2000).tolist(), [True, True, True])

    def test_filter_with_min(self): # test with a number would filter 3 numbers out in the series
        filtered_df = filter_with_min(self.df, 'Size', 700)
        self.assertEqual((filtered_df['Size'] >= 700).tolist(),[True, True])

    def test_filter_with_min(self): # test with a number that's too high to be the min limit, return empty series
        filtered_df = filter_with_min(self.df, 'Size', 1001)
        self.assertTrue((filtered_df['Size'] >= 1001).empty)

    def test_filter_with_conditions(self):
        filtered_df = filter_with_conditions(self.df, 11)
        self.assertEqual(len(filtered_df),1) # we have one of each of room layout in the test file

    def test_filter_utilities(self): # this function only keeps the 'yes' rows by default because when user chose 
        # this criterion, they bt default considered utilites covered is important
        filtered_df = filter_utilities(self.df)
        self.assertTrue(len(filtered_df),3) # three rows have 'yes'

    def test_filter_pet(self): # three unique entries available, when user chooses 'dog', then would filter out 
        # the ones with row_values == 'no' and 'cat only'
        filtered_df = filter_pet(self.df, 'd')
        self.assertTrue(len(filtered_df),2) # two rows with 'yes', filtered the 'no' and 'cat only' out

    def test_normalize_column_benefit(self):
        #test normalized_column function for 'benefit' type
        df = normalize_column(self.df.copy(), 'Size', 'benefit') # set up a view only copy
        normalized_col = df['Size_normalized'] # Numerator = (value - col_min)
        self.assertTrue(normalized_col.min() == 0) #check if the min value in the column after normalized is 0.
        self.assertTrue(normalized_col.max() == 1)#check if the min value in the column after normalized is 0.

    def test_normalize_column_cost(self):
        #Test normalize_column function for 'cost' type.
        df = normalize_column(self.df.copy(), 'Price', 'cost')
        normalized_col = df['Price_normalized']# Numerator = (col_max - value)
        self.assertTrue(normalized_col.min() == 0)
        self.assertTrue(normalized_col.max() == 1)

    def test_normalize_column_all_equal(self):
        #test when all values are the same
        df = self.df.copy() # create a view copy not affect the original file
        df['Price'] = 500  # set all values to the same 
        df = normalize_column(df, 'Price', 'cost') #apply the function to this column
        self.assertEqual(sum(df['Price_normalized']), 1 * len(df['Price_normalized'])) #check if the all the 
        # normalized value equals 1

    @patch('builtins.input', side_effect=['5', '4', '1']) # mock user_input
    def test_get_user_importance_scores(self,col):
        col = ['Price', 'Size', 'Safety Level'] # use 3 columns as criteria
        weights = get_user_importance_scores(col) #sum of the weights should equal to 1.0 according to our function
        self.assertAlmostEqual(weights['Price'], 0.5) # in this case, user_input for 'price' column is 5, which should be
        # 0.5/1 = 0.5

    def test_weighted_ave(self):#combine normalized columns with weights to get scores
        col = ['Price', 'Size', 'Safety Level']# choose 3 columns of criteria
        col_type = {'Price': 'cost', 'Size': 'benefit', 'Safety Level': 'benefit'} # specify the column-type
        weights = {'Price': 0.5, 'Size': 0.3, 'Safety Level': 0.2} 
        ranked_df = weighted_ave(self.df.copy(), col, weights, col_type)
        self.assertTrue('Score' in ranked_df.columns) # in the new copy, ranked dataframe has column 'score'
        self.assertTrue(ranked_df['Score'].is_monotonic_decreasing) # check if dataframe is ranked top down(>=)

            
if __name__ == '__main__':
    unittest.main()