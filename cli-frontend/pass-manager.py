import requests, json

CONFIG_PATH = 'config.json'
BASE_URL = 'http://localhost:3250'

def start():
    #1. Open config json file
    config_json = open(CONFIG_PATH)

    #2. Process the json file into a dictionary then close the file
    config = json.load(config_json) 
    config_json.close()

    #3. Make auth request to the rest api, if fails, make login request
    url = f'{BASE_URL}/account'
    response = requests.get(url, params={'token': config['token']})

    if response.status_code <= 205:
       print("Token is still valid")
       
    else:
        # Do a login request, append new token to the config file
        data = {
            "email": config["email"],
            "password": config["password"],
            "is_non_browser": "true"
        }
        response = requests.post(url, json=data)
        data = response.json()

        account = data["account"]
        token = data["token"]

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

start()