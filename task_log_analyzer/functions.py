import constants as c
from sample_data import sample_data


def get_user_selection(nums_tuple:tuple):
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


def section_heading(heading:str):
    print(f"""{heading}
{c.LONG_LINE}""")

def home_menu_screen(filter_states):
    # Home menu
    print(f""" 
{c.LONG_LINE}
[Please choose an option by entering a number below]
1) Load a .csv file --------------------> (Data from the file will be stored)
2) View/Edit Task Logs -----------------> (View, add, edit, and delete data)
3) View Task Log Analytics -------------> (View data summaries and stats)
4) Exit program

** Important **: In order to store and analyze task logs, you must first create\na database instance as specified in the README file
        """)

    # Get user input
    user_num = get_user_selection((1, 2, 3, 4))

    match user_num:
        case 1:
            # Go to upload csv screen
            load_csv_screen(filter_states)
        case 2:
            # Go to view/edit task logs screen
            view_edit_task_logs_screen(filter_states)
        case 3:
            # Go to view task log analytics screen
            pass
        case 4:
            # Exit
            return


def load_csv_screen(filter_states):
    """Instructions and function for user to load csv file"""
    print(c.MSG_PLEASE_CHOOSE)
    print(f"""{c.NAV_TITLE}
1) Return to home menu\n""")
    section_heading("Add a .csv file")
    print(f"""
2) Upload a .csv file\n""")
    section_heading("Instructions")
    print("""
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
To load file, enter 2 if you have not already, then enter the file path of your .csv file.
Enter 1 to cancel.""")

    user_csv_input(filter_states)


def user_csv_input(filter_states):
    """User inputs one or more csv files to be stored/analyzed"""
    # Get user selection
    user_num = get_user_selection((1,2))

    match user_num:
        case 1:
            # Go to home menu
            home_menu_screen(filter_states)
        case 2:
            # Upload csv
            file_path = input("Enter .csv file path: ")
            # Will add cleaning/validation later in microservices
            print("\nFile load successful!")
            print("Enter 1 to return to home screen, or 2 to load another file.")
            user_csv_input(filter_states)


def view_edit_task_logs_screen(filter_states):
    """User can choose between CRUD operations"""
    print(c.MSG_PLEASE_CHOOSE)
    print(c.NAV_TITLE)
    print("1) Return to home menu\n")

    section_heading("View/Edit Task Logs")

    print('{:30} {:30}'.format("2) View task logs", "3) Manually add a task log"))
    print('{:30} {:30}'.format("4) Edit a task log", "5) Delete a task log\n"))

    user_num = get_user_selection((1, 2, 3, 4, 5))

    match user_num:
        case 1:
            # Go to home menu
            home_menu_screen(filter_states)
        case 2:
            # Go to view task logs screen
            view_task_logs_screen(filter_states)
        case 3:
            # Go to add task log screen
            pass
        case 4:
            # Go to edit task log screen
            return
        case 5:
            # Go to delete task log screen
            pass


def view_task_logs_screen(filter_states):
    task_name_filter = filter_states["task name"]
    start_date_filter = filter_states["start date"]
    end_date_filter = filter_states["end date"]
    category_filter = filter_states["category"]
    task_type_filter = filter_states["task type"]


    print(c.MSG_PLEASE_CHOOSE)
    print(c.NAV_TITLE)
    print("""1) Return to home menu
2) Return to View/Edit menu""")

    section_heading("\nActive Data Filters ----- (filter task logs by one or more criteria)")
    print("{:30} {:30} {:30}".format(f"Task Name: {task_name_filter}", f"Start Date: {start_date_filter}",
                                     f"End Date: {end_date_filter}"))
    print("{:30} {:30}".format(f"Category: {category_filter}", f"Task Type: {task_type_filter}\n"))
    print("3) Set or remove a data filter")

    section_heading("\nView Task Logs")
    # Output data
    print(sample_data(), "\n")

    user_num = get_user_selection((1,2,3))
    match user_num:
        case 1:
            # Go to home screen
            home_menu_screen(filter_states)
        case 2:
            # Go to view/edit task logs screen
            view_edit_task_logs_screen(filter_states)
        case 3:
            # Go to set/remove data filter screen
            set_filters_screen(filter_states, "View Task Logs")


def set_filters_screen(filter_states, prev_screen):
    task_name_filter = filter_states["task name"]
    start_date_filter = filter_states["start date"]
    end_date_filter = filter_states["end date"]
    category_filter = filter_states["category"]
    task_type_filter = filter_states["task type"]

    print(c.MSG_PLEASE_CHOOSE)
    print(c.NAV_TITLE)
    print(f"""1) Return to home menu
2) Return to {prev_screen} Screen
""")
    section_heading("\nActive Data Filters ----- (filter task logs by one or more criteria)")
    print("{:30} {:30} {:30}".format(f"Task Name: {task_name_filter}", f"Start Date: {start_date_filter}",
                                     f"End Date: {end_date_filter}"))
    print("{:30} {:30}".format(f"Category: {category_filter}", f"Task Type: {task_type_filter}\n"))

    section_heading("Which data filter would you like to edit?")
    print("{:15} {:15} {:15}".format("4) Task Name", "5) Start Date",
                                     "6) End Date"))
    print("{:15} {:15}".format("7) Category", "8) Task Type\n"))

    user_filter_input(filter_states, prev_screen)


def user_filter_input(filter_states, prev_screen):
    """User inputs filter to add or remove"""
    # Get user selection
    user_num = get_user_selection((1,2,4,5,6,7,8))

    match user_num:
        case 1:
            # Go to home menu
            home_menu_screen(filter_states)
        case 2:
            # Go to previous menu
            if prev_screen == "View Task Logs":
                view_task_logs_screen(filter_states)
            else:
                pass
        case 4:
            # Task Name filter
            update_filter(filter_states, "task name", prev_screen)
        case 5:
            # Start Date filter
            update_filter(filter_states, "start date", prev_screen)
        case 6:
            # End Date filter
            update_filter(filter_states, "end date", prev_screen)
        case 7:
            # Category filter
            update_filter(filter_states, "category", prev_screen)
        case 8:
            # Task Type filter
            update_filter(filter_states, "task type", prev_screen)


def update_filter(filter_states, filter_name, prev_screen):
    user_input = input(f"Enter a new {filter_name} filter, or enter 'any' to remove filter: ")
    # Need to add input validation
    filter_states[filter_name] = user_input
    print(f"{filter_name} filter successfully updated!")
    print(f"Enter 1 to return to home screen, 2 to return to {prev_screen} screen, or 3 to edit another filter.")

    user_num = get_user_selection((1,2,3))

    match user_num:
        case 1:
            # Go to home screen
            home_menu_screen(filter_states)
        case 2:
            # Go to previous menu
            if prev_screen == "View Task Logs":
                view_task_logs_screen(filter_states)
            else:
                pass
        case 3:
            # Go to set/remove data filter
            user_filter_input(filter_states, prev_screen)

