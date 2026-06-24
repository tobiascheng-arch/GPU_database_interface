'''Interface of a GPU database, so people can access it and find out what they want. 
    They can pick from multiple options and queries to find out things that meet their requirments'''

#All of the imports used in this code is stores here
import sqlite3
from tabulate import tabulate
import sys
from easygui import *

# Contains the file name, and the script used to connect all of the specific tables in the relational database
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


#Print parameter function - prints out a table based on the info you give it, e.g. a model that your interested in
def print_parameter_query(fields:str, where:str, parameter):
    """ Prints the results for a parameter query in tabular form. """
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    sql = ("SELECT " + fields + " FROM " + TABLES + " WHERE " + where)
    cursor.execute(sql,(parameter,))
    results = cursor.fetchall()
    codebox("Here are the results:", "Results:", tabulate(results,fields.split(",")))
    db.close()
    
#Print parameter function with 2 parameters instead - does the same as the first one but has two parameters e.g. min and max limit for cost
def print_parameter_query2(fields:str, where:str, parameter, parameter2):
    """ Prints the results for a parameter query in tabular form. """
    db = sqlite3.connect(DB_NAME)
    cursor = db.cursor()
    sql = ("SELECT " + fields + " FROM " + TABLES + " WHERE " + where)
    cursor.execute(sql,(parameter, parameter2, ))
    results = cursor.fetchall()
    codebox("Here are the results:", "Results:", tabulate(results,fields.split(",")))
    db.close()  

#added ALL_FIELDS to make it look cleaner
ALL_FIELDS = "Manufacturer, Model, VRAM_GB, Memory_type, Bus_bit, Release_year, GPU_boost_clock_MHz, Power_W, Interface, Length_mm, Ray_tracing, Price_USD, Performance_rated_by_ai, Upscaling_gen"

#While loop that loops until "x" or cancel is pressed, loops through asking the user what they need
while True:
    #ASks user for what they want, queries, or individual thing that becomes a parameter
    msg ="What do you want to see?"
    title = "GPU database"
    choices = ["Queries", "Manufacturer", "Model", "VRAM", "Memory type", "Bus (in bits)", "Release year", "GPU boost clock (MHz)","Power (W)", "Interface", "Length", "Ray tracing", "Price range", "Performance rated by ai", "Upscaling Gen"]
    choice = choicebox(msg, title, choices)
    
    #Chcks if the x buttons is pressed
    if choice == None: sys.exit()
    #If the chosen thing is queries, it would as the user to pick one then print it into a codebox
    elif choice == "Queries":
        msg ="What query do you want to see?"
        title = "GPU database"
        query_choices = ["All_info", "Avg_to_good_performance", "GPUs_below_or_equal_$500", "NVIDIA_with_great_upscaling_gen", "Top_10_cheapest", "Top_10_expensive", "Value_for_money", "avg_to_cheap_NVIDIA"]
        query = choicebox(msg, title, query_choices)
        if query == None: continue
        print_query(query)
    
    #If they chose Manufacturers, it asks them to pick one, then prints the table into a codebox
    elif choice == "Manufacturer":
        msg ="What manufacturer do you want to see?"
        title = "GPU database"
        choices = ["NVIDIA", "AMD", "Intel"]
        manu_choice = choicebox(msg, title, choices)
        if manu_choice == None: continue
        print_parameter_query(ALL_FIELDS, 
                            "Manufacturer = ? ORDER BY Model Asc",manu_choice)

    #If they choose model, it asks them to pick one, then prints the table into a codebox
    elif choice == "Model":
        msg ="What model do you want to see?"
        title = "GPU database"
        choices = ["RTX", "GTX", "RX", "Arc"]
        model_choice = choicebox(msg, title, choices)
        if model_choice == None: continue
        print_parameter_query(ALL_FIELDS, 
                            "Model LIKE ? ORDER BY Model Asc", f"%{model_choice}%")

    #If the choose VRAM, it asks the user to input a number between 4 - 32, that will be the min, 
    # Then asks the user to input their max between their chosen min and 32.
    # If the num is already 32, it skips the asking for the max stage, then prints the table into a codebox
    elif choice == "VRAM":
        msg ="How much Vram do you need? (4 GB - 32 GB, can only be multiples of 4)\nPick your minimum:"
        title = "GPU database"
        while True:
            ramchoice1 = integerbox(msg, title, default=8,
                            lowerbound= 4,
                            upperbound=32)
            if ramchoice1 == None: break
            if ramchoice1 % 4 == 0:
                break
            msgbox("You must pick a number that is a multiple of 4!", title)
        if ramchoice1 == None: continue
        
        if ramchoice1 != 32:
            while True:
                msg = f"Now pick your maximum (Between {ramchoice1} and 32):"
                ramchoice2 = integerbox(msg, title, default=ramchoice1,
                                lowerbound=ramchoice1,
                                upperbound=32)
                if ramchoice2 == None: break
                if ramchoice2 % 4 == 0:
                    break
                msgbox("You must pick a number that is a multiple of 4!", title)
        elif ramchoice1 == 32: ramchoice2 = 32
        if ramchoice2 == None: continue
        print_parameter_query2(ALL_FIELDS, "VRAM_GB BETWEEN ? AND ? ORDER BY VRAM_GB DESC, Model ASC", ramchoice1, ramchoice2)

    #If they chose Memory, it asks them to pick one, then prints the table into a codebox
    elif choice == "Memory type":
        msg ="What type of memory do you want to see?"
        title = "GPU database"
        choices = ["GDDR7", "GDDR6X", "GDDR6", "GDDR5", "GDDR5X"]
        mem_choice = choicebox(msg, title, choices)
        if mem_choice == None: continue
        print_parameter_query(ALL_FIELDS,   
                            "Memory_type = ? ORDER BY Memory_type Asc, Model ASC", mem_choice)

    #If they choose Bus in bits, IT asks the user to pick a minimun num and a max num that must be equal or bigger than the min, 
    #That is the range, then prints out a table with a Bit range of that range given
    elif choice == "Bus (in bits)":
        msg ="Pick your minimum between 64 & 512:"
        title = "GPU database"
        bus_choice1 = integerbox(msg, title, default=64,
                        lowerbound= 64,
                        upperbound=512)
        if bus_choice1 == None: continue
        if bus_choice1 != 512:
            msg = f"Now pick your maximum (Between {bus_choice1} and 512):"
            bus_choice2 = integerbox(msg, title, default=bus_choice1,
                            lowerbound=bus_choice1,
                            upperbound=512)
        elif bus_choice1 == 512: bus_choice2 = 512
        if bus_choice2 == None: continue
        print_parameter_query2(ALL_FIELDS, "Bus_bit BETWEEN ? AND ? ORDER BY VRAM_GB DESC, Model ASC", bus_choice1, bus_choice2)

    #If release year is chosen, It asks the user to type a year between 2016 and 2025, then prints out all of the GPUs release on that year
    elif choice == "Release year":
        msg ="Type down the year you want to see, (make sure it is between 2016 and 2025):"
        title = "GPU database"
        year_choice = integerbox(msg, title, default=2016,
                        lowerbound= 2016,
                        upperbound= 2025)
        if choice == None: sys.exit()
        print_parameter_query(ALL_FIELDS, "Release_year = ? ORDER BY Manufacturer ASC, Model ASC", year_choice)

    #If they choose GPU_boost_clock, IT asks the user to pick a minimun num and a max num that must be equal or bigger than the min, 
    #That is the range, then prints out a table with a MHz of that range given
    elif choice == "GPU boost clock (MHz)":
        msg ="Pick your minimum between 1582MHz & 2815MHz:"
        title = "GPU database"
        boost_choice1 = integerbox(msg, title, default=1582,
                        lowerbound= 1582,
                        upperbound=2815)
        if boost_choice1 == None: sys.exit()
        if boost_choice1 != 2815:
            msg = f"Now pick your maximum (Between {boost_choice1}MHz and 2815MHz):"
            boost_choice2 = integerbox(msg, title, default=boost_choice1,
                            lowerbound=boost_choice1,
                            upperbound=2815)
        elif boost_choice1 == 2815: boost_choice2 = 2815
        if boost_choice2 == None: continue
        print_parameter_query2(ALL_FIELDS, "GPU_boost_clock_MHz BETWEEN ? AND ? ORDER BY GPU_boost_clock_MHz DESC, Model ASC", boost_choice1, boost_choice2)

    #If they choose Power (w), IT asks the user to pick a minimun num and a max num that must be equal or bigger than the min, 
    #That is the range, then prints out a table with a Power usage range of that range given
    elif choice == "Power (W)":
        msg ="Pick your minimum between 53W & 600W:"
        title = "GPU database"
        power_choice1 = integerbox(msg, title, default=53,
                        lowerbound= 53,
                        upperbound=600)
        if power_choice1 == None: continue
        if power_choice1 != 600:
            msg = f"Now pick your maximum (Between {power_choice1}W and 600W):"
            power_choice2 = integerbox(msg, title, default=power_choice1,
                            lowerbound=power_choice1,
                            upperbound=600)
        elif power_choice1 == 600: power_choice2 = 600
        if power_choice2 == None: continue
        print_parameter_query2(ALL_FIELDS, "Power_W BETWEEN ? AND ? ORDER BY Power_W ASC, Model ASC", power_choice1, power_choice2)

    #if the pick Interface, it asks them to pick one, then prints the table into a codebox
    elif choice == "Interface":
        msg ="Pick an interface"
        title = "GPU database"
        choices = ["PCIe 5.0 x16", "PCIe 4.0 x16", "PCIe 4.0 x8", "PCIe 3.0 x16", "PCIe 4.0 x4"]
        interface_choice = choicebox(msg, title, choices)
        if interface_choice == None: continue
        print_parameter_query(ALL_FIELDS, "Interface = ? ORDER BY Interface ASC, Model ASC", interface_choice)

    #If they choose Length, IT asks the user to pick a minimun num and a max num that must be equal or bigger than the min, 
    #That is the range, then prints out a table with a Size range of that range given
    elif choice == "Length":
        msg ="Pick your minimum size between 170mm & 345mm:"
        title = "GPU database"
        length_choice1 = integerbox(msg, title, default=170,
                        lowerbound= 170,
                        upperbound=345)
        if length_choice1 == None: continue
        if length_choice1 != 345:
            msg = f"Now pick your maximum (Between {length_choice1}mm and 345mm):"
            length_choice2 = integerbox(msg, title, default=length_choice1,
                            lowerbound=length_choice1,
                            upperbound=345)
        elif length_choice1 == 345: length_choice2 = 345
        if length_choice2 == None: continue
        print_parameter_query2(ALL_FIELDS, "Length_mm BETWEEN ? AND ? ORDER BY Length_mm ASC, Model ASC", length_choice1, length_choice2)

    #IF they pick Ray tracing, it asks them to pick yes or no, then prints the table into a codebox
    elif choice == "Ray tracing":
        msg ="Do you want Ray tracing?"
        title = "GPU database"
        choices = ["Yes", "No"]
        ray_choice = choicebox(msg, title, choices)
        if ray_choice == None: continue
        print_parameter_query(ALL_FIELDS, "Ray_tracing = ? ORDER BY Manufacturer ASC, Model ASC", ray_choice)

    #If they choose price range, IT asks the user to pick a minimun num and a max num that must be equal or bigger than the min, 
    #That is the range, then prints out a table with a price range of that range given
    elif choice == "Price range":
        msg ="Pick your minimum price between 119 & 1999 USD:"
        title = "GPU database"
        price_choice1 = integerbox(msg, title, default=119,
                        lowerbound= 119,
                        upperbound=1999)
        if price_choice1 == None: continue
        if price_choice1 != 1999:
            msg = f"Now pick your maximum (Between {price_choice1} and 1999 USD):"
            price_choice2 = integerbox(msg, title, default=price_choice1,
                            lowerbound=price_choice1,
                            upperbound=1999)
        elif price_choice1 == 1999: price_choice2 = 1999
        if price_choice2 == None: continue
        print_parameter_query2(ALL_FIELDS, "Price_USD BETWEEN ? AND ? ORDER BY PRICE_USD ASC, Performance_rated_by_ai DESC", price_choice1, price_choice2)

    #If they choose Performance, IT asks the user to pick a minimun num and a max num that must be equal or bigger than the min, 
    #That is the range, then prints out a table with a Performance range of that range given
    elif choice == "Performance rated by ai":
        msg ="Pick the minimun rating you want:"
        title = "GPU database"
        rating = integerbox(msg, title,
                        lowerbound= 0,
                        upperbound=100)
        if rating == None: continue
        print_parameter_query2(ALL_FIELDS, "Performance_rated_by_ai = ? ORDER BY Performance_rated_by_ai ASC, Model ASC", rating, 100)

    #If they pick Upscaling Gen, it asks them to pick one, then prints the table into a codebox
    elif choice == "Upscaling Gen":
        msg ="What Upscaling Gen do you want?"
        title = "GPU database"
        choices = ["DLSS (next-gen)", "DLSS 2", "DLSS 3", "None", "FSR 3", "FSR 2", "XeSS"]
        gen_choice = choicebox(msg, title, choices)
        if gen_choice == None: sys.exit()
        print_parameter_query(ALL_FIELDS, "Upscaling_gen = ? ORDER BY Upscaling_Gen ASC, Model ASC", gen_choice)
