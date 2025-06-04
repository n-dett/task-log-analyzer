import functions as f


def main():
    # Display title and main menu on program start
    print(r"""
___ ____ ____ _  _    _    ____ ____    ____ _  _ ____ _    _   _ ___  ____ ____ 
 |  |__| [__  |_/     |    |  | | __    |__| |\ | |__| |     \_/    /  |___ |__/ 
 |  |  | ___] | \_    |___ |__| |__]    |  | | \| |  | |___   |    /__ |___ |  \ """, end='')

    filter_states = {
        "Task Name": "any",
        "Start Date": "any",
        "End Date": "any",
        "Category": "any",
        "Task Type": "any"
    }
    f.home_menu_screen(filter_states)

if __name__ == "__main__":
    main()