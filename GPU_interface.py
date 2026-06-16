import sqlite3
from tabulate import tabulate
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
    print(tabulate(results,headings))
    db.close()

choice = ''
while choice != 'Z':
    choice = input('Welcome to the GPU interface\n\n'
                   'Type the letter for the info you want:\n'
                   'A: ALl info in our database\n'
                   'B: Average to cheap NVIDIA products\n'
                   'C: GPUs with average or better preformance (include top of the end ones)\n'
                   'D: GPUs that are cheaper than 500 USD\n'
                   'E: NVIDIA products with an upscaling gen of DLSS 4 and DLSS next gen\n'
                    'Z: Exit\n\nType option here: ').upper()
    if choice == 'A':
        print_query('All_info')
    elif choice == 'B':
        print_query('avg_to_cheap_NVIDIA')
    elif choice == 'C':
        print_query('Avg_to_good_performance')
    elif choice == 'D':
        print_query('GPUs_below_or_equal_$500')
    elif choice == 'E':
        print_query('NVIDIA_with_great_upscaling_gen')
    else:
        print("bye")