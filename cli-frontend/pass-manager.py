import requests, json, os
from colorama import init
from termcolor import colored, cprint

# Custom scripts
import helpers, globals
from commands import login_or_create, get_commands

init()

def init_config():
    try:
        #1. Open config json file
        config_json = open(globals.CONFIG_PATH)

        if os.path.getsize(globals.CONFIG_PATH) == 0:
            raise FileNotFoundError("Config file is empty")

        #2. Process the json file into a dictionary then close the file
        globals.config = json.load(config_json) 
        config_json.close()
    except FileNotFoundError as e:
        cprint(f"Config file {globals.CONFIG_PATH} not found or was empty!", "red")
        
        login_or_create()

def print_password(source):
    print(source["username"])
    print(source["pass"])
    print(source["note"])
    print(source["site"])

def get_all_passwords():
    if not globals.config.get("token"):
        return
    
    cookies = {"token": globals.config["token"]}
    try:
        url = f'{globals.BASE_URL}/password/all'
        response = requests.get(url, cookies=cookies)
        if(response.status_code == 200):
            globals.passwords = response.json()
        else:
            cprint(response.text, "yellow")

    except Exception as e:
        cprint(f"Error with getting all passwords: {e}", "red")

def login():
    url = f'{globals.BASE_URL}/account'
    try:
        cookies = {"token": globals.config["token"]}
        response = requests.get(url, cookies=cookies, timeout=10)
        if response.status_code <= 205: # If token is valid
            data = response.json()
            if(response.cookies.get_dict()):
                helpers.update_config(cookies=response.cookies, data=data)
        else:   # If token is not valid
            # Do a login request, append new token to the config file
            data = {
                "email": globals.config["email"],
                "password": globals.config["password"],
            }

            response = requests.post(url, json=data, cookies=cookies, timeout=10)
            if response.status_code > 205:
                raise Exception(response.text)
            data = response.json()

            if(response.cookies.get_dict()):
                helpers.update_config(cookies=response.cookies, data=data)
                
        return True
    except Exception as ex:
        cprint(f'Error: {ex}', "yellow")
        while True:
            resolved = login_or_create()
            if resolved:
                break
        return True

def start():
    try:
        helpers.get_ascii_art()
        print(helpers.splash_text)
        #1. Initialize your programs configuration from the json file
        init_config()

        #2. Make auth request to the rest api, if fails, make login request
        if not login():
            cprint("Our servers seem to be down :/", "red")
            cprint("Please try logging in or creating an account later", "yellow")
            exit()

        print() # Simply prints a newline character
        print(f"Signed in as: {colored(globals.config["email"], 'green')}")

        get_all_passwords()

        helpers.print_sources() # Prints off all of the users 'sources'

        running = True
        while running:
            running = get_commands()
    except KeyboardInterrupt:
        cprint("\nExiting program", "yellow")

start()