import requests, json, globals
from enum import Enum
from helpers import check_index_validity, isNumber, print_sources, add_dashes, update_config
from termcolor import colored, cprint
from xtra_chars import Xtra_Chars
from prompt_toolkit import prompt

class Commands(Enum):
    ADD_SOURCE = 1
    EDIT_SOURCE = 2
    VIEW_FULL_SOURCE = 3
    DELETE_SOURCE = 4
    LIST_SOURCES = 5
    EDIT_ACCOUNT = 6
    VIEW_ACCOUNT = 7
    SIGNOUT = 8
    DELETE_ACCOUNT = 9
    CREATE_NEW_ACCOUNT = 10

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

        return False
    except Exception as ex:
        print(colored(ex, "light_red"))

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
            cprint("Check your email for activation link, but act quickly as it expires in 15 minutes!", "yellow")
            exit(0) # Exits since you won't be able to do anything with the new account anyways until you activate it

    except Exception as ex:
        cprint("Something went wrong with creating your account", "red")
        return False

def delete_account():
    try:
        url = f"{globals.BASE_URL}/account"
        response = requests.delete(url, cookies={"token": globals.config["token"]})
        if response.status_code > 205:
            raise Exception(response.text)
        else:
            cprint("Account successfully deleted!", "light_green")
            exit(0)
    except Exception as ex:
        cprint(f"Error: {ex}", "red")

    return True

def view_account():
    print(f"┌{add_dashes(48)}┐")
    print(f"│{"Account Details":<47} │")
    print(f"│{add_dashes(48)}│")
    print(f"│{"Email:":<12}{globals.config["email"]:<36}│")
    print(f"│{"Password:":<12}{globals.config["password"]:<36}│")
    print(f"│{"Firstname:":<12}{globals.config["firstname"]:<36}│")
    print(f"│{"Lastname:":<12}{globals.config["lastname"]:<36}│")
    print(f"└{add_dashes(48)}┘")
    # To do, also show first and last name here too!
    return True

def edit_account(new_firstname=None, new_lastname=None, new_password=None):
    try:
        # TODO - Store first & last name in config 
        if new_firstname is None:
            new_firstname = prompt("Edit firstname: ", default=globals.config["firstname"])

        if new_lastname is None:
            new_lastname = prompt("Edit lastname: ", default=globals.config["lastname"])

        if new_password is None:
            new_password = prompt("Enter new password: ", default=globals.config["password"])

        print() # Just for a newline character

        # Set each back to original if they weren't changed

        url = f"{globals.BASE_URL}/account"

        data = {
            "new_firstname": new_firstname, 
            "new_lastname": new_lastname, 
            "new_password": new_password
        }

        response = requests.put(url, json=data, cookies={"token": globals.config["token"]})

        if(response.cookies.get_dict()):
            globals.config["password"] = new_password
            updated_account = {
                "first_name": new_firstname,
                "last_name": new_lastname
            }

            update_config(cookies=response.cookies, data=updated_account)
            cprint(response.text, "light_green")
        return True
    except Exception as ex:
        print(ex)
        return False
   

def view_full_source(index=None):    
    if not index:
        index = input("Enter index to view: ")
        if not check_index_validity(index, len(globals.passwords)):
            return False
    
    index = int(index) - 1

    source = globals.passwords[index]
    TLC = Xtra_Chars.TLC.value
    TRC = Xtra_Chars.TRC.value
    BLC = Xtra_Chars.BLC.value
    BRC = Xtra_Chars.BRC.value
    LNG_LN = Xtra_Chars.LNG_LN.value

    print(f"{TLC}{add_dashes(108)}{TRC}")
    print(f"{LNG_LN}{"Site":<10}{source["site"]:<98}{LNG_LN}")
    print(f"{LNG_LN}{"User":<10}{source["username"]:<98}{LNG_LN}")
    print(f"{LNG_LN}{"Pass":<10}{source["pass"]:<98}{LNG_LN}")
    print(f"{LNG_LN}{"Note":<10}{source["note"]:<98}{LNG_LN}")
    print(f"{BLC}{add_dashes(108)}{BRC}")
    
    return True

def edit_source():
    index = input("Enter index to edit: ")
    if not check_index_validity(index, len(globals.passwords)):
        return False
    
    index = int(index) - 1

    source = globals.passwords[index]

    # TODO - EDIT LINES WITH PROMPTS INSTEAD

    old_site = source["site"]

    username = prompt("Edit site username: ", default=source["username"])

    password = prompt("Edit site password: ", default=source["pass"])

    note = prompt("Edit site note: ", default=source["note"])

    site = prompt("Edit site url: ", default=source["site"])

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
            view_full_source(index + 1)  # Displays the source right after modifying it
            return True
    except Exception as ex:
        cprint(ex, "red")
        cprint("Something went wrong with updating this source", "red")
        return False

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
        print_sources()
        return True
    except Exception as ex:
        print("Error when deleting source: ", ex)
        return False

def print_commands():
    #print(menu_text)
    print("\nMenu Options: ")
    for command in Commands:
        print(f"{f"{command.value}.":<3} {command.name}")


def add_new_pass(username=None, password=None, note=None, site=None):
    if username is None:    
        username = prompt("Enter site username: ", default="username")

    if password is None:  
        password = prompt("Enter site password: ", default="password")

    if note is None:  
        note = prompt("Enter site note: ", default="no note found here...")

    if site is None:  
        site = prompt("Enter site url: ", default="https://ex@test.com")

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
        print_sources() 
        return True
    except:
        cprint("Something went wrong with creating password in database!", "red")
        return False
    
# All this does is remove all content from your config file
def signout():
    f = open(globals.CONFIG_PATH, "w")
    f.write("")
    f.close()
    cprint("Successfully signed out!", "green")
    exit(0)

def get_commands():
    print_commands()
    cmd = input("\nEnter digit or char/string to quit: ")

    if not isNumber(cmd):
        return False
    else:
        cmd = int(cmd)

    if cmd < 0 or cmd > len(Commands):
        return False
    
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
            if len(globals.passwords) == 0:
                cprint("No user passwords found", "yellow")
                return True
            print_sources() 

        case Commands.EDIT_ACCOUNT.value:
            return edit_account()

        case Commands.VIEW_ACCOUNT.value:
            return view_account()
        
        case Commands.SIGNOUT.value:
            signout()

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
    print(f'3. Exit')

    cmd = input('Select valid choice or a non number to exit: ')

    if check_index_validity(cmd, 3):
        cmd = int(cmd)
    else:
        exit()

    if cmd == 1:
        return set_account()
    elif cmd == 2:
        return create_account()
    else:
        exit(0)