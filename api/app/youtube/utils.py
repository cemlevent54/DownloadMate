# helper/utils.py

import re

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', '', name)
