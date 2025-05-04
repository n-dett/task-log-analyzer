def main():
    print(r"""
___ ____ ____ _  _    _    ____ ____    ____ _  _ ____ _    _   _ ___  ____ ____ 
 |  |__| [__  |_/     |    |  | | __    |__| |\ | |__| |     \_/    /  |___ |__/ 
 |  |  | ___] | \_    |___ |__| |__]    |  | | \| |  | |___   |    /__ |___ |  \ """, end='')

    # Home menu
    print(""" 
―――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――――
Please choose an option by entering a number below:
1) Load a .csv file --------------------> (Data from the file will be stored)
2) View/Edit Task Logs -----------------> (View, add, edit, and delete data)
3) View Task Log Analytics -------------> (View data summaries and stats)
4) Exit program

** Important **: In order to store and analyze task logs, you must first create\na database instance as specified in the README file
    """)

    while True:
        # Get user input
        user_num = 0
        invalid = True

        while invalid:
            user_num = int(input("Enter a number: "))

            # Check if number is valid
            if not user_num in (1, 2, 3, 4):
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
            case 4:
                return

if __name__ == "__main__":
    main()