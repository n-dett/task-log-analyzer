def home_menu():
    # Home menu
    print(""" 
―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
[Please choose an option by entering a number below]
1) Load a .csv file --------------------> (Data from the file will be stored)
2) View/Edit Task Logs -----------------> (View, add, edit, and delete data)
3) View Task Log Analytics -------------> (View data summaries and stats)
4) Exit program

** Important **: In order to store and analyze task logs, you must first create\na database instance as specified in the README file
        """)

    # Get user input
    user_num = get_user_input((1, 2, 3, 4))

    match user_num:
        case 1:
            # Go to upload csv screen
            load_csv()
        case 2:
            # Go to view/edit task logs screen
            pass
        case 3:
            # Go to view task log analytics screen
            pass
        case 4:
            # Exit
            return


def load_csv():
    print("""\n\n[Please choose an option below by entering a number below]
―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――\n""")
    print("""Navigation
――――――――――――――――――――
1) Return to home menu\n""")
    print("""Add a .csv file
――――――――――――――――――――
2) Upload a .csv file\n
Instructions:
――――――――――――――――――――
Task log data from your .csv file will be stored in your database.
Multiple .csv files can be uploaded (one at a time), but duplicate rows will be ignored.
Rows missing a Date, Task Name, Start Time, or End Time will be dropped.
Rows with invalid data types will be dropped.\n
Task Log Analyzer can accept .csv files with the following columns and data types:
Columns must be in this order and any extra columns will be ignored.
    • Date (MM/DD/YYYY or MM-DD-YYYY or YYYY/MM/DD or YYYY-MM-DD)
    • Task Name (text)
    • Task Type (text)
    • Category (text)
    • Start Time (e.g. 6:00 PM or 18:00) 
    • End Time (e.g. 6:00 PM or 18:00)\n
To load file, enter 2 if you have not already.
Then enter the file path of your .csv file, or enter 1 to cancel.""")

    # Get user selection
    user_num = get_user_input((1,2))

    match user_num:
        case 1:
            # Go to home menu
            home_menu()
        case 2:
            # Upload csv
            pass


def get_user_input(nums_tuple=tuple):
    """Get user selection and validate"""
    # Get user input
    user_num = 0
    invalid = True

    while invalid:
        user_num = int(input("Enter a number: "))

        # Check if number is valid
        if not user_num in nums_tuple:
            print("Invalid number. Please try again.")
        else:
            invalid = False
    return user_num

# load_csv()