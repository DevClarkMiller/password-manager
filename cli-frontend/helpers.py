import globals
splash_text = ""
menu_text = ""
MENU_TEXT_PATH = './ascii_art/menuText.txt'
SPLASH_TEXT_PATH = './ascii_art/splashText.txt'
max_source_lengths = None

def get_ascii_art():
    global splash_text
    global menu_text
    f = open(SPLASH_TEXT_PATH, "r")
    splash_text = f.read()
    f.close()

    f = open(MENU_TEXT_PATH, "r")
    menu_text = f.read()
    f.close()

# Purpose of this function is for proper outputting
def find_max_source_lengths(sources):
    global max_source_lengths
    maxs = {
        "user": 0,
        "pass": 0,
        "note": 0,
        "site": 0
    }

    for source in sources:
        user_length = len(source["username"])
        pass_length = len(source["pass"])
        note_length = len(source["note"])
        site_length = len(source["site"])

        if user_length > maxs["user"]: maxs["user"] = user_length
        if pass_length > maxs["pass"]: maxs["pass"] = pass_length
        if note_length > maxs["note"]: maxs["note"] = note_length
        if site_length > maxs["site"]: maxs["site"] = site_length

    max_source_lengths = maxs

def isNumber(s):
    for char in s:
        if not char.isdigit():
            return False
    return True

def check_index_validity(index, list_length):
    if not isNumber(index) or not index:
        return False
    
    index = int(index) - 1
    if index < 0 or index > list_length - 1:
        return False

    return True

def print_sources():
    find_max_source_lengths(globals.passwords)

    if not globals.passwords or not max_source_lengths: return

    # First sorts the sources by the sites name
    globals.passwords.sort(key=lambda source:source["site"])

    COL_SPACING = 3
    max_user = max_source_lengths["user"] + COL_SPACING
    max_pass = max_source_lengths["pass"] + COL_SPACING
    max_note = max_source_lengths["note"] + COL_SPACING
    max_site = max_source_lengths["site"] + COL_SPACING + 3 # The extra 3 spacings is for the index listing

    add_dashes = lambda n: f"{"":─<{n}}"
    num_dashes = max_user + max_pass + max_note + max_site - 2
    
    # Prints off a header with correct spacing for each of the source lengths
    print(f"┌{add_dashes(num_dashes)}┐")
    print(f"│{'Site':<{max_site}}{'User':<{max_user}}{'Pass':<{max_pass}}{'Note':<{max_note - 2}}│")

    # Prints dashes to seperate the header
    print(f"│{add_dashes(num_dashes)}│")

    for i in range(0, len(globals.passwords)):
        source = globals.passwords[i]
        print(f"│{f"{i + 1}. {source["site"]}":<{max_site}}{source["username"]:<{max_user}}{source["pass"]:<{max_pass}}{source["note"]:<{max_note - 2}}│")

    print(f"└{add_dashes(num_dashes)}┘")