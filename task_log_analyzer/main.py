def main():
    print(r"""
___ ____ ____ _  _    _    ____ ____    ____ ____ _  _ ____ ____ ____ ___ ____ ____ 
 |  |__| [__  |_/     |    |  | | __    | __ |___ |\ | |___ |__/ |__|  |  |  | |__/ 
 |  |  | ___] | \_    |___ |__| |__]    |__] |___ | \| |___ |  \ |  |  |  |__| |  \ """, end='')

    # Home menu
    print(""" 
―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
Please choose an option by entering a number below:
1) Load a .csv file --------------------> (Data from the file will be stored)
2) View/Edit Task Logs -----------------> (View, add, edit, and delete data)
3) View Task Log Analytics -------------> (View data summaries and stats)

** Important **: In order to store and analyze task logs, you must first create\na database instance as specified in the README file
    """)

    # Get user input
    user_num = 0
    invalid = True

    while invalid:
        user_num = int(input("Enter a number: "))

        # Check if number is valid
        if not user_num in (1, 2, 3):
            print("Invalid number. Please try again.")
        else:
            invalid = False


    match user_num:
        case 1:
            # Go to upload csv screen
            pass
        case 2:
            # Go to view/edit task logs screen
            pass
        case 3:
            # Go to view task log analytics screen
            pass
        case _:
            pass

if __name__ == "__main__":
    main()