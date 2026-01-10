# Copyright (c) KANE

# All rights reserved

# ----------------------------------------------------------------------------------------------------------------------------------------------------------|

#     - Any modification of the code is strictly prohibited.

#     - Reselling, redistributing, or claiming ownership of this tool is not allowed.

from Config.Util import *
from Config.Config import *
import webbrowser

Title("Discord RAt (PAID)")

try:
    print(f"{BEFORE + AFTER} {INFO} This is a paid feature.")
    webbrowser.open("https://t.me/kane_tools")
    Continue()
    Reset()

except Exception as e:
    Error(e)

