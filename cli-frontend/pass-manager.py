import requests, json, os
from enum import Enum
from termcolor import colored

CONFIG_PATH = './config.json'
MENU_TEXT_PATH = './menuText.txt'
SPLASH_TEXT_PATH = './splashText.txt'
BASE_URL = 'http://localhost:3250'

config = None
passwords = []
max_source_lengths = None
splash_text = ""
menu_text = ""

class Commands(Enum):
    ADD_SOURCE = 1
    EDIT_SOURCE = 2
    DELETE_SOURCE = 3
    LIST_SOURCES = 4
    EDIT_ACCOUNT = 5
    VIEW_ACCOUNT = 6
    DELETE_ACCOUNT = 7

def get_ascii_art():
    global splash_text
    global menu_text
    f = open(SPLASH_TEXT_PATH, "r")
    splash_text = f.read()
    f.close()

    f = open(MENU_TEXT_PATH, "r")
    menu_text = f.read()
    f.close()


def set_account():
    global config
    
    print('Input the following fields to login')
    email = input("Enter email: ")
    password = input("Enter password: ")

    if not email or not password: return None
    
    # Update the config file
    config = {
        "email": email,
        "password": password,
        "token": ""
    }

    config_json = json.dumps(config, indent=4)

    with open(CONFIG_PATH, "w") as outfile:
        outfile.write(config_json)


def init_config():
    global config
    try:
        #1. Open config json file
        config_json = open(CONFIG_PATH)

        if os.path.getsize(CONFIG_PATH) == 0:
            raise FileNotFoundError("Config file is empty")

        #2. Process the json file into a dictionary then close the file
        config = json.load(config_json) 
        config_json.close()
    except FileNotFoundError as e:
        print(f"Config file {CONFIG_PATH} not found or was empty!")
        set_account()

def print_password(source, sources_max_lengths):
    print(source["username"])
    print(source["pass"])
    print(source["note"])
    print(source["site"])

# Purpose of this function is for proper outputting
def find_max_source_lengths():
    global passwords
    global max_source_lengths
    maxs = {
        "user": 0,
        "pass": 0,
        "note": 0,
        "site": 0
    }

    for source in passwords:
        user_length = len(source["username"])
        pass_length = len(source["pass"])
        note_length = len(source["note"])
        site_length = len(source["site"])

        if user_length > maxs["user"]: maxs["user"] = user_length
        if pass_length > maxs["pass"]: maxs["pass"] = pass_length
        if note_length > maxs["note"]: maxs["note"] = note_length
        if site_length > maxs["site"]: maxs["site"] = site_length

    max_source_lengths = maxs

def print_sources():
    global passwords
    global max_source_lengths

    find_max_source_lengths()

    if not passwords or not max_source_lengths: return

    # First sorts the sources by the sites name
    passwords.sort(key=lambda source:source["site"])

    COL_SPACING = 3
    max_user = max_source_lengths["user"] + COL_SPACING
    max_pass = max_source_lengths["pass"] + COL_SPACING
    max_note = max_source_lengths["note"] + COL_SPACING
    max_site = max_source_lengths["site"] + COL_SPACING + 3 # The extra 3 spacings is for the index listing

    add_dashes = lambda n: f"{"":―<{n}}"
    num_dashes = max_user + max_pass + max_note + max_site - 2
    
    # Prints off a header with correct spacing for each of the source lengths
    print(f"┌{add_dashes(num_dashes)}┐")
    print(f"│{'Site':<{max_site}}{'User':<{max_user}}{'Pass':<{max_pass}}{'Note':<{max_note - 2}}│")

    # Prints dashes to seperate the header
    print(f"│{add_dashes(num_dashes)}│")

    for i in range(0, len(passwords)):
        source = passwords[i]
        print(f"│{f"{i + 1}. {source["site"]}":<{max_site}}{source["username"]:<{max_user}}{source["pass"]:<{max_pass}}{source["note"]:<{max_note - 2}}│")

    print(f"└{add_dashes(num_dashes)}┘")

def get_all_passwords():
    global config
    global passwords
    if not config.get("token"):
        return
    
    cookies = {"token": config["token"]}
    try:
        url = f'{BASE_URL}/password/all'
        response = requests.get(url, cookies=cookies)
        if(response.status_code == 200):
            passwords = response.json()
        else:
            print(response.text)

    except Exception as e:
        print(f"Error with getting all passwords: {e}")

def add_new_pass(username="username", password="password", note="no note provided", site="google.ca"):
    global config
    global passwords
    cookies = {"token": config["token"]}
    try:
        url = f'{BASE_URL}/password'

        data = {
            "username": username,
            "pass": password,
            "note": note,
            "site": site
        }
        response = requests.post(url, json=data, cookies=cookies, timeout=10)
        if(response.status_code == 200):
            print("Successfully added new source")

        passwords.append(data)
        return True
    except:
        print("Something went wrong with creating password in database!")
        return False

def update_config(cookies):
    global config
    token = cookies["token"]
    # Update the config file
    config = {
        "email": config["email"],
        "password": config["password"],
        "token": token
    }

    config_json = json.dumps(config, indent=4)

    with open(CONFIG_PATH, "w") as outfile:
        outfile.write(config_json)

    print('Updated your config file')

def login():
    global config
    url = f'{BASE_URL}/account'
    try:
        cookies = {"token": config["token"]}
        response = requests.get(url, cookies=cookies, timeout=10)
        if response.status_code <= 205: # If token is valid
            data = response.json()
            if(response.cookies.get_dict()):
                update_config(response.cookies)
        else:   # If token is not valid\
            # Do a login request, append new token to the config file
            data = {
                "email": config["email"],
                "password": config["password"],
            }

            response = requests.post(url, json=data, cookies=cookies, timeout=10)
            data = response.json()

            if(response.cookies.get_dict()):
                update_config(response.cookies)
    except Exception as e:
        print(f'Error with logging in', e)
        set_account()

def isNumber(s):
    for char in s:
        if not char.isdigit():
            return False
    return True

def check_index_validity(index, list_length):
    if not isNumber(index):
        return False
    
    index = int(index) - 1
    if index < 0 or index > list_length - 1:
        return False

    return True

def delete_account():

    return True
def view_account():
    return True

def edit_account():
    return True

def edit_source():
    index = input("Enter index to edit: ")
    if not check_index_validity(index, len(passwords)):
        return False
    
    index = int(index) - 1

    return True

def delete_source():
    index = input("Enter index to delete: ")
    if not check_index_validity(index, len(passwords)):
        return False
    
    index = int(index) - 1
    source = passwords[index]
    passwords.pop(index)
    try:
        url = f'{BASE_URL}/password'
        response = requests.delete(url, params={"site": source["site"]}, cookies={"token": config["token"]})
        print(response.text)
    except Exception as ex:
        print("Error when deleting source: ", ex)

    return True

def print_commands():
    #print(menu_text)
    print("\nMenu Options: ")
    for command in Commands:
        print(f"{command.value}. {command.name}")

def get_commands():
    print_commands()
    command = input("\nEnter digit or char/string to quit: ")

    if not isNumber(command):
        return False
    else:
        command = int(command)

    if command < 0 or command > len(Commands):
        return False
    
    match command:
        case Commands.ADD_SOURCE.value:
            username = input("Enter site username: ")
            password = input("Enter site password: ")
            note = input("Enter site note: ")
            site = input("Enter site url: ")
            return add_new_pass(username=username, password=password, note=note, site=site)

        case Commands.EDIT_SOURCE.value:
            return edit_source()

        case Commands.DELETE_SOURCE.value:
            return delete_source()

        case Commands.LIST_SOURCES.value:
            print_sources()

        case Commands.EDIT_ACCOUNT.value:
            return edit_account()

        case Commands.VIEW_ACCOUNT.value:
            return view_account()

        case Commands.DELETE_ACCOUNT.value:
            return delete_account()
        
        case _:
            print("Valid option not entered!")
    return True

def start():
    global passwords
    get_ascii_art()
    print(splash_text)
    #1. Initialize your programs configuration from the json file
    init_config()

    #2. Make auth request to the rest api, if fails, make login request
    login()

    print(f"Signed in as: {colored(config["email"], 'green')}")

    get_all_passwords()

    print_sources() 

    running = True
    while running:
        running = get_commands()
start()