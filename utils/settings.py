import json

def read_settings():
    """Reads the data from the /shared/settings.json file and returns the dictionary"""
    with open ("./shared/settings.json") as settings_file:
        return json.load(settings_file)

def save_settings(settings):
    """Saves the given settings into the /shared/settings.json file and returns whether it was successful or not"""
    try:
        with open("./shared/settings.json", "w") as settings_file:
            json.dump(settings, settings_file)
        return True
    except:
        return False
