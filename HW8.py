#Jai Advani

import matplotlib.pyplot as plt
import os
import sqlite3
import unittest

def get_restaurant_data(db_filename):
    """
    This function accepts the file name of a database as a parameter and returns a list of
    dictionaries. The key:value pairs should be the name, category, building, and rating
    of each restaurant in the database.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    list_of_restaurant_dicts = []

    categories_dict = {}
    cur.execute("SELECT * FROM categories")
    for row in cur:
        categories_dict[row[0]] = row[1]

    buildings_dict = {}
    cur.execute("SELECT * FROM buildings")
    for row in cur:
        buildings_dict[row[0]] = row[1]

    cur.execute("SELECT * FROM restaurants")
    for row in cur:
        dict = {}
        dict['name'] = row[1]
        dict['category'] = categories_dict[row[2]]
        dict['building'] = buildings_dict[row[3]]
        dict['rating'] = row[4]
        list_of_restaurant_dicts.append(dict)

    return list_of_restaurant_dicts

def barchart_restaurant_categories(db_filename):
    """
    This function accepts a file name of a database as a parameter and returns a dictionary. The keys should be the
    restaurant categories and the values should be the number of restaurants in each category. The function should
    also create a bar chart with restaurant categories and the counts of each category.
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    restaurant_categories_lst = []
    lst = []

    cur.execute("SELECT category_id FROM restaurants")
    for row in cur:
        restaurant_categories_lst.append(row[0])

    for id in restaurant_categories_lst:
        cur.execute(f"SELECT category FROM categories WHERE id = {id}")
        for row in cur:
            lst.append(row[0])

    lst = sorted(lst)
    categories_dict = {}
    for type in lst:
        if type in categories_dict:
            categories_dict[type] += 1
        else:
            categories_dict[type] = 1
    
    sorted_dict = sorted(categories_dict.items(), key = lambda item : item[1], reverse = True)
    sorted_dict = dict(sorted_dict)
    

    x_axis = list(sorted_dict.keys())
    y_axis = list(sorted_dict.values())
    fig = plt.figure(figsize = (7,5))
    plt.barh(x_axis, y_axis)
    plt.title("Types of Restaurant on South University Ave")
    plt.xlabel("Number of Restaurants")
    plt.xticks([1,2,3,4])
    plt.ylabel("Restaurant Categories")
    plt.tight_layout()
    plt.gca().invert_yaxis()
    plt.show()

    return sorted_dict

#EXTRA CREDIT
def highest_rated_category(db_filename):#Do this through DB as well
    """
    This function finds the average restaurant rating for each category and returns a tuple containing the
    category name of the highest rated restaurants and the average rating of the restaurants
    in that category. This function should also create a bar chart that displays the categories along the y-axis
    and their ratings along the x-axis in descending order (by rating).
    """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_filename)
    cur = conn.cursor()

    category_totals_dict = barchart_restaurant_categories(db_filename)
    category_total_ratings_dict = {}
    category_avg_ratings_dict = {}

    categories_id_dict = {}
    cur.execute("SELECT * FROM categories")
    for row in cur:
        categories_id_dict[row[0]] = row[1]

    cur.execute("SELECT * FROM restaurants")
    for row in cur:
        category = categories_id_dict[row[2]]
        rating = row[4]
        if category in category_total_ratings_dict:
            category_total_ratings_dict[category] += rating
        else:
            category_total_ratings_dict[category] = rating
    
    for key in category_total_ratings_dict:
        category_avg_ratings_dict[key] = round(category_total_ratings_dict[key] / category_totals_dict[key], 1)

    sorted_category_avg_ratings_dict = sorted(category_avg_ratings_dict.items(), key = lambda item : item[1], reverse = True)
    sorted_category_avg_ratings_dict = dict(sorted_category_avg_ratings_dict)


    x_axis = list(sorted_category_avg_ratings_dict.keys())
    y_axis = list(sorted_category_avg_ratings_dict.values())
    fig = plt.figure(figsize = (7,5))
    plt.barh(x_axis, y_axis)
    plt.title("Average Restaurant Ratings by Category")
    plt.xlabel("Ratings")
    plt.xticks([0,1,2,3,4])
    plt.ylabel("Categories")
    plt.tight_layout()
    plt.gca().invert_yaxis()
    plt.show()
    
    highest_rated_restaurant_category_average_rating = list(sorted_category_avg_ratings_dict.items())[0]

    return highest_rated_restaurant_category_average_rating


#Try calling your functions here
def main():
    get_restaurant_data("South_U_Restaurants.db")
    barchart_restaurant_categories("South_U_Restaurants.db")
    highest_rated_category("South_U_Restaurants.db")
class TestHW8(unittest.TestCase):
    def setUp(self):
        self.rest_dict = {
            'name': 'M-36 Coffee Roasters Cafe',
            'category': 'Cafe',
            'building': 1101,
            'rating': 3.8
        }
        self.cat_dict = {
            'Asian Cuisine ': 2,
            'Bar': 4,
            'Bubble Tea Shop': 2,
            'Cafe': 3,
            'Cookie Shop': 1,
            'Deli': 1,
            'Japanese Restaurant': 1,
            'Juice Shop': 1,
            'Korean Restaurant': 2,
            'Mediterranean Restaurant': 1,
            'Mexican Restaurant': 2,
            'Pizzeria': 2,
            'Sandwich Shop': 2,
            'Thai Restaurant': 1
        }
        self.best_category = ('Deli', 4.6)

    def test_get_restaurant_data(self):
        rest_data = get_restaurant_data('South_U_Restaurants.db')
        self.assertIsInstance(rest_data, list)
        self.assertEqual(rest_data[0], self.rest_dict)
        self.assertEqual(len(rest_data), 25)

    def test_barchart_restaurant_categories(self):
        cat_data = barchart_restaurant_categories('South_U_Restaurants.db')
        self.assertIsInstance(cat_data, dict)
        self.assertEqual(cat_data, self.cat_dict)
        self.assertEqual(len(cat_data), 14)

    def test_highest_rated_category(self):
        best_category = highest_rated_category('South_U_Restaurants.db')
        self.assertIsInstance(best_category, tuple)
        self.assertEqual(best_category, self.best_category)

if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)
