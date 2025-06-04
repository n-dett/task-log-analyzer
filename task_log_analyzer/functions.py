import constants as c
from constants import MSG_PLEASE_CHOOSE, NAV_TITLE
from task_log_analyzer.sockets import data_clean_socket, validator_socket, database_socket, summary_socket
from temp_data import temp_data
import pandas as pd
import io
import json



def get_user_selection(nums_tuple:tuple):
    """Get user selection and validate"""
    # Get user input
    user_num = None
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
            task_log_analytics_screen(filter_states)
        case 4:
            # Exit
            return


def load_csv_screen(filter_states):
    """Instructions and function for user to load csv file"""
    print(c.MSG_PLEASE_CHOOSE)
    print(f"{c.NAV_TITLE}\n1) Return to home menu\n")
    section_heading("Add a .csv file")
    print(f"2) Upload a .csv file\n")
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


def send_to_cleaner(df):
    # Convert to csv string
    csv_string = df.to_csv(header=True, index=False)

    # Send data to cleaning microservice
    data_clean_socket.send_string(csv_string)

    # Receive cleaned csv from microservice
    data_clean_message = data_clean_socket.recv()
    cleaned_csv_string = data_clean_message.decode()

    return cleaned_csv_string



def send_to_validator(csv_string):
    # Send data to validator microservice
    df_lines = csv_string.splitlines()
    csv_string = ','.join(df_lines)
    validator_socket.send_string(csv_string)

    # Receive validated data from microservice
    valid_data_message = validator_socket.recv()
    valid_data_string = valid_data_message.decode()

    # Convert back to csv
    valid_data_list = valid_data_string.split('\n')
    valid_data = ""
    status_msg = ""
    if len(valid_data_list) > 1:
        # Split into two string arrays
        valid_data = valid_data_list[0].strip()
        status_msg = valid_data_list[1].strip()
    else:
        status_msg = valid_data_list[0].strip()

    # Remove "Valid data:"
    valid_data = valid_data.replace("Valid data: ", "")

    # Remove braces
    valid_data = valid_data.replace("]", "")
    valid_data = valid_data.replace("[", "")

    # Remove apostrophes
    valid_data = valid_data.replace("'", "")

    # Remove extra spaces
    valid_data = valid_data.replace(", ", ",")

    # Add \n to recreate rows; save in new string
    comma_count = 0
    new_string = ""
    for char in valid_data:
        if char == ',':
            comma_count += 1
            if comma_count % 6 == 0:
                char = '\n'
        new_string += char

    # Convert back to data frame
    valid_df = pd.read_csv(io.StringIO(new_string), sep=",")
    valid_df_string = valid_df.to_string()

    print(status_msg)
    return valid_df


def insert_csv_in_db(df):
    # Send load data event num to database microservice
    database_socket.send_string("1")
    # Receive response from microservice
    event_message = database_socket.recv()
    # Send csv to database microservice
    csv_string = df.to_csv(header=True, index=False)
    database_socket.send_string(csv_string)
    # Receive response from microservice
    confirmation_message = database_socket.recv()


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

            # Read into data frame
            df = pd.read_csv(file_path)

            # Send to data cleaner and back
            cleaned_csv_string = send_to_cleaner(df)
            #print(f"CLEANED DATA:\n{cleaned_csv_string}")

            # Send to validator and back
            valid_df = send_to_validator(cleaned_csv_string)
            #print(f"VALID DF:\n{valid_df}")

            # Send to database microservice
            insert_csv_in_db(valid_df)

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
            add_task_log_screen(filter_states)
        case 4:
            # Go to edit task log screen
            edit_task_log_screen(filter_states)
        case 5:
            # Go to delete task log screen
            delete_task_log_screen(filter_states)


def view_task_logs_screen(filter_states):
    task_name_filter = filter_states["Task Name"]
    start_date_filter = filter_states["Start Date"]
    end_date_filter = filter_states["End Date"]
    category_filter = filter_states["Category"]
    task_type_filter = filter_states["Task Type"]


    print(c.MSG_PLEASE_CHOOSE)
    print(c.NAV_TITLE)
    print("1) Return to home menu\n2) Return to View/Edit menu")

    display_active_filters(filter_states)
    print("3) Set or remove a data filter\n")

    section_heading("\nView Task Logs")

    # Retrieve and display task logs
    # Send select data event num to database microservice
    database_socket.send_string("2")
    # Receive response from microservice
    event_message = database_socket.recv()
    # Send csv to database microservice
    database_socket.send_string("Main program: requesting db data")
    # Receive response from microservice
    csv_message = database_socket.recv()
    csv_string = csv_message.decode()
    df = pd.read_csv(io.StringIO(csv_string))

    print(df.to_string(index=False), "\n")

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
    task_name_filter = filter_states["Task Name"]
    start_date_filter = filter_states["Start Date"]
    end_date_filter = filter_states["End Date"]
    category_filter = filter_states["Category"]
    task_type_filter = filter_states["Task Type"]

    print(c.MSG_PLEASE_CHOOSE)
    print(c.NAV_TITLE)
    print(f"1) Return to home menu\n2) Return to {prev_screen} screen")
    display_active_filters(filter_states)
    print("3) Set or remove a data filter\n")

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
                task_log_analytics_screen(filter_states)
        case 4:
            # Task Name filter
            update_filter(filter_states, "Task Name", prev_screen)
        case 5:
            # Start Date filter
            update_filter(filter_states, "Start Date", prev_screen)
        case 6:
            # End Date filter
            update_filter(filter_states, "End Date", prev_screen)
        case 7:
            # Category filter
            update_filter(filter_states, "Category", prev_screen)
        case 8:
            # Task Type filter
            update_filter(filter_states, "Task Type", prev_screen)


def update_filter(filter_states, filter_name, prev_screen):
    user_input = input(f"Enter a new {filter_name} filter, or enter 'any' to remove filter: ")
    # Need to add input validation
    filter_states[filter_name] = user_input
    print(f"{filter_name} filter successfully updated!")
    print(f"When you return to the {prev_screen} screen, the filter will be applied.")
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
                task_log_analytics_screen(filter_states)
        case 3:
            # Go to set/remove data filter
            user_filter_input(filter_states, prev_screen)


def add_task_log_screen(filter_states):
    """User manually inputs a task log"""
    print(MSG_PLEASE_CHOOSE)
    print(NAV_TITLE)
    print("""1) Return to home menu
2) Return to View/Edit menu\n""")
    section_heading("Manually Add a Task Log")
    print("3) Add a task log\n")

    user_add_task_log_input(filter_states)


def user_add_task_log_input(filter_states):
    user_num = get_user_selection((1,2,3))

    match user_num:
        case 1:
            # Go to home screen
            home_menu_screen(filter_states)
        case 2:
            # Go to view task logs screen
            view_task_logs_screen(filter_states)
        case 3:
            # Add a task log
            add_task_log(filter_states)


def add_task_log(filter_states):
    task_date = input("Enter task date (YYYY-MM-DD): ")
    task_name = input("Enter task name: ")
    task_type = input("Enter task type: ")
    task_category = input("Enter category name: ")
    start_time = input("Enter start time: ")
    end_time = input("Enter end time: ")

    # Need to validate
    # Add inputs to database

    print(f"\nYour task, {task_name}, was successfully added!")
    print("Enter 1 to return to home menu, or 2 to return to View/Edit menu, or 3 to add another task log.")
    user_num = get_user_selection((1,2,3))
    match user_num:
        case 1:
            # Go to home screen
            home_menu_screen(filter_states)
        case 2:
            # Go to view task logs screen
            view_task_logs_screen(filter_states)
        case 3:
            # Add a task log
            add_task_log(filter_states)


def edit_task_log_screen(filter_states):
    print(MSG_PLEASE_CHOOSE)
    print(NAV_TITLE)
    print("1) Return to home menu\n2) Return to View/Edit Menu\n")

    section_heading("Edit a Task Log")
    print("3) Edit task log\n")

    user_edit_task_log_input_1(filter_states)


def user_edit_task_log_input_1(filter_states):
    user_num = get_user_selection((1,2,3))

    match user_num:
        case 1:
            # Go to home screen
            home_menu_screen(filter_states)
        case 2:
            # Go to view_edit task logs screen
            view_edit_task_logs_screen(filter_states)
        case 3:
            # Edit a task log
            user_edit_task_log_input_2(filter_states)


def user_edit_task_log_input_2(filter_states):
    print("\nEnter the ID of the task log you would like to edit.")
    print("(To find a task log ID, visit the View Task Logs screen and filter as needed.)")

    task_id = get_task_id()

    print(f"\nCurrent data for the task log with ID {task_id}:")

    # Temp sample data
    data = temp_data()
    print(data.iloc[[0]].to_string(index=False), "\n")

    print("Which field would you like to update?")
    print(c.SHORT_LINE + c.SHORT_LINE)
    print("{:15} {:15} {:15}".format("4) Date", "5) Task Name", "6) Task Type"))
    print("{:15} {:15} {:15}".format("7) Category", "8) Start Time", "9) End Time\n"))

    user_num = get_user_selection((1,2,4,5,6,7,8,9))
    match user_num:
        case 1:
            # Go to home screen
            home_menu_screen(filter_states)
        case 2:
            # Go to view task logs screen
            view_task_logs_screen(filter_states)
        case 4:
            # Edit Date
            edit_task_log(filter_states, "Date")
        case 5:
            # Edit Task Name
            edit_task_log(filter_states, "Task Name")
        case 6:
            # Edit Task Type
            edit_task_log(filter_states, "Task Type")
        case 7:
            # Edit Category
            edit_task_log(filter_states, "Category")
        case 8:
            # Edit Start Time
            edit_task_log(filter_states, "Start Time")
        case 9:
            # Edit End Time
            edit_task_log(filter_states, "End Time")


def edit_task_log(filter_states, column_name):
    new_value = input(f"Enter a new {column_name} value, or 3 to cancel: ")

    match new_value:
        case 3:
            # Cancel edit and return to main edit screen
            edit_task_log_screen(filter_states)
        case _:
            # Validate the input
            # Update the selected column
            print(f"{column_name} updated!")
            edit_task_log_screen(filter_states)


def get_task_id():
    """Get user selection and validate"""
    # Get user input
    user_num = None
    invalid = True

    while invalid:
        user_num = int(input("Enter an ID: "))

        # Check if number is valid
        if not isinstance(user_num, int):
            print("Invalid ID. Please try again.")
        else:
            invalid = False
    return user_num


def delete_task_log_screen(filter_states):
    print(MSG_PLEASE_CHOOSE)
    print(NAV_TITLE)
    print("1) Return to home screen\n2) Return to View/Edit menu\n")

    section_heading("Delete a Task Log")
    print("3) Delete a task log\n")

    user_delete_task_log_input(filter_states)


def user_delete_task_log_input(filter_states):
    user_num = get_user_selection((1,2,3))

    match user_num:
        case 1:
            # Go to home screen
            home_menu_screen(filter_states)
        case 2:
            # Go to view task logs screen
            view_edit_task_logs_screen(filter_states)
        case 3:
            # Add a task log
            delete_task_log(filter_states)


def delete_task_log(filter_states):
    print("\nEnter the ID of the task log you would like to delete.")
    print("(To find a task log ID, visit the View Task Logs screen and filter as needed.)")

    task_id = get_task_id()

    #print(f"\nCurrent data for the task log with ID {task_id}:")

    # Temp sample data
    # data = temp_data()
    # print(data.iloc[[0]].to_string(index=False), "\n")

    # Delete confirmation
    print(f"Are you sure you want to delete the task log with ID {task_id}? (enter 1 for yes or 2 for no)")

    user_num = get_user_selection((1,2))

    if user_num == 1:
        # Delete task log

        # Send select data event num to database microservice
        database_socket.send_string("4")
        # Receive response from microservice
        event_message = database_socket.recv()
        # Send task ID to database microservice
        database_socket.send_string(str(task_id))
        # Receive response from microservice
        confirmation_message = database_socket.recv()
        confirmation_string = confirmation_message.decode()

        print(f"{confirmation_string}\n")
        #print("Task log deleted!")
        delete_task_log_screen(filter_states)
    else:
        delete_task_log_screen(filter_states)



def task_log_analytics_screen(filter_states):
    print(MSG_PLEASE_CHOOSE)
    print(NAV_TITLE)
    print("1) Return to home menu")

    display_active_filters(filter_states)
    print("2) Set or remove a data filter\n")

    section_heading("Task Log Analytics")

    # Retrieve task log data
    # Send select data event num to database microservice
    database_socket.send_string("2")
    # Receive response from microservice
    event_message = database_socket.recv()
    # Send csv to database microservice
    database_socket.send_string("Main program: requesting db data")
    # Receive response from microservice
    csv_message = database_socket.recv()
    csv_string = csv_message.decode()
    #df = pd.read_csv(io.StringIO(csv_string))


    # Send data to summary microservice
    summary_socket.send_string(csv_string)
    # Receive data summary
    summary_message = summary_socket.recv()
    summary_data_json = summary_message.decode()
    summary_data_dict = json.loads(summary_data_json)


    print(f"Total number of task logs: {summary_data_dict["total_task_logs"]}")
    print(f"Total time logged: {summary_data_dict["total_time"]}")
    print(f"Average duration per task log: {summary_data_dict["avg_duration"]}")
    print(f"Time logged per task type: {summary_data_dict["time_by_type"]}")
    print(f"Time logged per category type: {summary_data_dict["time_by_category"]}\n")

    user_num = get_user_selection((1,2))

    match user_num:
        case 1:
            home_menu_screen(filter_states)
        case 2:
            set_filters_screen(filter_states, "Task Log Analytics")


def display_active_filters(filter_states):
    task_name_filter = filter_states["Task Name"]
    start_date_filter = filter_states["Start Date"]
    end_date_filter = filter_states["End Date"]
    category_filter = filter_states["Category"]
    task_type_filter = filter_states["Task Type"]

    section_heading("\nActive Data Filters ---------- (filter task logs by one or more criteria)")
    print("{:30} {:30} {:30}".format(f"Task Name: {task_name_filter}", f"Start Date: {start_date_filter}",
                                     f"End Date: {end_date_filter}"))
    print("{:30} {:30}".format(f"Category: {category_filter}", f"Task Type: {task_type_filter}\n"))
