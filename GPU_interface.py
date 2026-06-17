import sqlite3
from tabulate import tabulate
import sys
from easygui import *

# This is the filename of the database to be used
DB_NAME = 'GPU_database.db'
TABLES = (" GPU_database "
        "LEFT JOIN Interfaces ON GPU_database.Interface_id = Interfaces.Interface_id "
        "LEFT JOIN Manufacture ON GPU_database.Manufacture_ID = Manufacture.Manufacture_ID "
        "LEFT JOIN Memory ON GPU_database.Memory_id = Memory.Memory_id "
        "LEFT JOIN Upscaling ON GPU_database.Upscaling_id = Upscaling.Upscaling_id ")

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

def print_parameter_query(fields:str, where:str, parameter):
    """ Prints the results for a parameter query in tabular form. """
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    sql = ("SELECT " + fields + " FROM " + TABLES + " WHERE " + where)
    cursor.execute(sql,(parameter,))
    results = cursor.fetchall()
    codebox("Here are the results:", "Results:", tabulate(results,fields.split(",")))
    db.close()  

while True:
    msg ="What do you want to see?"
    title = "GPU database"
    choices = ["Queries", "Manufacturer", "Model", "VRAM", "Memory type", "Bus (in bits)", "Release year", "GPU boost clock (MHz)","Power (W)", "Interface", "Length", "Ray tracing", "Price range", "Performance rated by ai", "Upscaling Gen"]
    choice = choicebox(msg, title, choices)

    if choice == "Queries":
        msg ="What query do you want to see?"
        title = "GPU database"
        query_choices = ["All_info", "Avg_to_good_performance", "GPUs_below_or_equal_$500", "NVIDIA_with_great_upscaling_gen", "Top_10_cheapest", "Top_10_expensive", "Value_for_money", "avg_to_cheap_NVIDIA"]
        query = choicebox(msg, title, query_choices)
        if choice == None: sys.exit()
        print_query(query)
    
    elif choice == "Manufacturer":
        msg ="What manufacturer do you want to see?"
        title = "GPU database"
        choices = ["NVIDIA", "AMD", "Intel"]
        choice = choicebox(msg, title, choices)
        if choice == None: sys.exit()
        print_parameter_query("Manufacturer, Model, [VRAM_(GB)], Memory_type, [Bus_(bit)], Release_year, [GPU_boost_clock_(MHz)], [Power_(W)], Interface, [Length_(mm)], Ray_tracing, [Price_(USD)], [Performance_(rated_by_ai)], Upscaling_gen", 
                            "Manufacturer = ? ORDER BY Model Asc",choice)


    elif choice == "Model":
        msg ="What model do you want to see?"
        title = "GPU database"
        choices = [""]
        choice = choicebox(msg, title, choices)
        if choice == None: sys.exit()
        print_parameter_query("Manufacturer, Model, [VRAM_(GB)], Memory_type, [Bus_(bit)], Release_year, [GPU_boost_clock_(MHz)], [Power_(W)], Interface, [Length_(mm)], Ray_tracing, [Price_(USD)], [Performance_(rated_by_ai)], Upscaling_gen", 
                            "Manufacturer = ? ORDER BY Model Asc",choice)

    elif choice == "VRAM":
        msg ="How much Vram do you need?"
        title = "GPU database"
        choices = [""]
        choice = choicebox(msg, title, choices)
        if choice == None: sys.exit()
    elif choice == "Memory type":
        msg ="What type of memory do you want to see?"
        title = "GPU database"
        choices = [""]
        choice = choicebox(msg, title, choices)
        if choice == None: sys.exit()
    elif choice == "Bus (in bits)":
        msg ="How much do you need?"
        title = "GPU database"
        choices = [""]
        choice = choicebox(msg, title, choices)
        if choice == None: sys.exit()
    elif choice == "Release year":
        msg ="What year do you want to see?"
        title = "GPU database"
        choices = [""]
        choice = choicebox(msg, title, choices)
        if choice == None: sys.exit()
    elif choice == "GPU boost clock (MHz)":
        msg ="What do you want to see?"
        title = "GPU database"
        choices = [""]
        choice = choicebox(msg, title, choices)
        if choice == None: sys.exit()
    elif choice == "Power (W)":
        msg ="How efficient do you want it?"
        title = "GPU database"
        choices = [""]
        choice = choicebox(msg, title, choices)
        if choice == None: sys.exit()
    elif choice == "Interface":
        msg ="What do you want to see?"
        title = "GPU database"
        choices = [""]
        choice = choicebox(msg, title, choices)
        if choice == None: sys.exit()
    elif choice == "Length":
        msg ="What size do you want to see?"
        title = "GPU database"
        choices = [""]
        choice = choicebox(msg, title, choices)
        if choice == None: sys.exit()
    elif choice == "Ray tracing":
        msg ="Do you want Ray tracing?"
        title = "GPU database"
        choices = ["Yes", "No"]
        choice = choicebox(msg, title, choices)
        if choice == None: sys.exit()
    elif choice == "Price range":
        msg ="What query do you want to see?"
        title = "GPU database"
        choices = [""]
        choice = choicebox(msg, title, choices)
        if choice == None: sys.exit()
    elif choice == "Performance rated by ai":
        msg ="How fast do you want your GPU?"
        title = "GPU database"
        choices = [""]
        choice = choicebox(msg, title, choices)
        if choice == None: sys.exit()
    elif choice == "Upscaling Gen":
        msg ="What Upscaling Gen do you want?"
        title = "GPU database"
        choices = [""]
        choice = choicebox(msg, title, choices)
        if choice == None: sys.exit()
    else:
        sys.exit()
