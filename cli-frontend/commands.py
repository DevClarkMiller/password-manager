import requests, json, globals
from enum import Enum
from helpers import check_index_validity, isNumber, print_sources
from termcolor import colored, cprint

class Commands(Enum):
    ADD_SOURCE = 1
    EDIT_SOURCE = 2
    VIEW_FULL_SOURCE = 3
    DELETE_SOURCE = 4
    LIST_SOURCES = 5
    EDIT_ACCOUNT = 6
    VIEW_ACCOUNT = 7
    DELETE_ACCOUNT = 8
    CREATE_NEW_ACCOUNT = 9

def set_account(email=None, password=None):
    try:
        if password is None or email is None:
            print('Input the following fields to login')

        if email is None:
            email = input("Enter email: ")

        if password is None:
            password = input("Enter password: ")

        if not email or not password: 
            raise Exception("Email or password wasn't entered in")
        
        # Update the config file
        globals.config = {
            "email": email,
            "password": password,
            "token": ""
        }

        config_json = json.dumps(globals.config, indent=4)

        with open(globals.CONFIG_PATH, "w") as outfile:
            outfile.write(config_json)

        return True
    except Exception as ex:
        print(colored(ex, "light_red"))

# def input_for_new_account():
# email = input("Enter email: ")
# password = input("Enter password: ")
# firstname = input("Enter firstname: ")
# lastname = input("Enter lastname: ")
# create_account(email, password, firstname, lastname)

def create_account(email=None, password=None, firstname=None, lastname=None):
    # Only displays this message if this function needs user input
    if email is None or password is None or firstname is None or lastname is None:
        print("Fill in the following fields to create your account: ")

    if email is None:
        email = input("Enter email: ")

    if password is None:
        password = input("Enter password: ")

    if firstname is None:
        firstname = input("Enter firstname: ")

    if lastname is None:
        lastname = input("Enter lastname: ")

    try:
        url = f'{globals.BASE_URL}/account/create'
        data = {
            "email": email,
            "password": password,
            "firstname": firstname,
            "lastname": lastname
        }

        response = requests.post(url, json=data, timeout=10)
        if response.status_code > 205:
            raise Exception("Return code is abnormal: ", response.status_code)
        else:
            cprint("Account successfully created!", "green")
            return True

    except Exception as ex:
        cprint("Something went wrong with creating your account", "red")
        return False

def delete_account():
    return True

def view_account():
    add_dashes = lambda n: f"{"":─<{n}}"
    print(f"┌{add_dashes(48)}┐")
    print(f"│{"Account Details":<47} │")
    print(f"│{add_dashes(48)}│")
    print(f"│{"Email:":<10}{globals.config["email"]:<38}│")
    print(f"│{"Password:":<10}{globals.config["password"]:<38}│")
    print(f"└{add_dashes(48)}┘")
    # To do, also show first and last name here too!
    return True

def edit_account():
    return True

def view_full_source():    
    
    return True

def edit_source():
    index = input("Enter index to edit: ")
    if not check_index_validity(index, len(globals.passwords)):
        return False
    
    index = int(index) - 1

    source = globals.passwords[index]

    # TODO - EDIT LINES WITH CURSES

    old_site = source["site"]

    username = input(f"Enter new site username, original was {source["username"]}: ")
    if not username:
        username = source["username"]

    password = input(f"Enter new site password, original was {source["pass"]}: ")
    if not password:
        password = source["pass"]

    note = input(f"Enter new site note, original was {source["note"]}: ")
    if not note:
        note = source["note"]

    site = input(f"Enter new site url, original was {source["site"]}: ")
    if not site:
        site = source["site"]

    try:
        url = f"{globals.BASE_URL}/password"

        data = {
            "username": username,
            "pass": password,
            "note": note,
            "old_site": old_site,
            "new_site": site
        }
        response = requests.put(url, json=data, cookies={"token": globals.config["token"]})
        if response.status_code > 205:
            raise Exception(response.text)
        else:
            cprint(response.text, "green")
            source = {
                "username": username,
                "pass": password,
                "note": note,
                "site": site
            }
            globals.passwords[index] = source   # Updates the index of the edited source
    except Exception as ex:
        cprint(ex, "red")
        cprint("Something went wrong with updating this source", "red")
        return False

    return True

def delete_source():
    index = input("Enter index to delete: ")
    if not check_index_validity(index, len(globals.passwords)):
        return False
    
    index = int(index) - 1
    source = globals.passwords[index]
    globals.passwords.pop(index)
    try:
        url = f'{globals.BASE_URL}/password'
        response = requests.delete(url, params={"site": source["site"]}, cookies={"token": globals.config["token"]})
        print(response.text)
    except Exception as ex:
        print("Error when deleting source: ", ex)

    return True

def print_commands():
    #print(menu_text)
    print("\nMenu Options: ")
    for command in Commands:
        print(f"{command.value}. {command.name}")


def add_new_pass(username=None, password=None, note=None, site=None):
    if username is None:    
        username = input("Enter site username: ")

    if password is None:  
        password = input("Enter site password: ")

    if note is None:  
        note = input("Enter site note: ")

    if site is None:  
        site = input("Enter site url: ")

    cookies = {"token": globals.config["token"]}
    try:
        url = f'{globals.BASE_URL}/password'

        data = {
            "username": username,
            "pass": password,
            "note": note,
            "site": site
        }
        response = requests.post(url, json=data, cookies=cookies, timeout=10)
        if(response.status_code == 200):
            print(colored("Successfully added new source", "green"))

        globals.passwords.append(data)
        return True
    except:
        cprint("Something went wrong with creating password in database!", "red")
        return False

def get_commands():
    print_commands()
    cmd = input("\nEnter digit or char/string to quit: ")

    if not isNumber(cmd):
        return False
    else:
        cmd = int(cmd)

    if cmd < 0 or cmd > len(Commands):
        return False
    
    # ADD_SOURCE = 1
    # EDIT_SOURCE = 2
    # VIEW_FULL_SOURCE = 3
    # DELETE_SOURCE = 4
    # LIST_SOURCES = 5
    # EDIT_ACCOUNT = 6
    # VIEW_ACCOUNT = 7
    # DELETE_ACCOUNT = 8
    
    match cmd:
        case Commands.ADD_SOURCE.value:
            return add_new_pass()

        case Commands.EDIT_SOURCE.value:
            return edit_source()
        
        case Commands.VIEW_FULL_SOURCE.value:
            return view_full_source()

        case Commands.DELETE_SOURCE.value:
            return delete_source()

        case Commands.LIST_SOURCES.value:
            # Doesn't really matter what the return is, 
            # this shouldn't make the program exit
            print_sources() 

        case Commands.EDIT_ACCOUNT.value:
            return edit_account()

        case Commands.VIEW_ACCOUNT.value:
            return view_account()

        case Commands.DELETE_ACCOUNT.value:
            return delete_account()
        
        case Commands.CREATE_NEW_ACCOUNT.value:
            return create_account()
        
        case _:
            print("Valid option not entered!")

    return True

def login_or_create():
    print(f'Here are your options: ')
    print(f'1. Sign in')
    print(f'2. Create account')

    cmd = input('Select valid choice or a non number to exit: ')

    if check_index_validity(cmd, 3):
        cmd = int(cmd)
    else:
        return False

    if cmd - 1 == 0:
        return set_account()
    else:
        return create_account()