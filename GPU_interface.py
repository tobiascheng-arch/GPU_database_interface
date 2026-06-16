import sqlite3
from tabulate import tabulate
import sys
from easygui import *

# This is the filename of the database to be used
DB_NAME = 'GPU_database.db'

#Print query function - prints out existing queries from sqlite
def print_query(view_name:str):
    # Set up the connection to the database
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    # Get the results from the view
    sql = "SELECT * FROM '" + view_name + "'"
    cursor.execute(sql)
    results = cursor.fetchall()
    # Get the field names to use as headings
    field_names = "SELECT name from pragma_table_info('" + view_name + "') AS tblInfo"
    cursor.execute(field_names)
    headings = list(sum(cursor.fetchall(),()))
    # Print the results in a table with the headings
    codebox("Here are the results of your query:", "Query results", tabulate(results,headings))
    db.close()

choice = ''
while True:
    msg ="What do you want to see?"
    title = "Music lessons"
    choices = ["All_info", "Avg_to_good_performance", "GPUs_below_or_equal_$500", "NVIDIA_with_great_upscaling_gen", "Top_10_cheapest", "Top_10_expensive", "Value_for_money", "avg_to_cheap_NVIDIA"]
    choice = choicebox(msg, title, choices)
    if choice == None: sys.exit()
    print_query(choice)