# Copyright (c) KANE

# All rights reserved

# ----------------------------------------------------------------------------------------------------------------------------------------------------------|

#     - Any modification of the code is strictly prohibited.

#     - Reselling, redistributing, or claiming ownership of this tool is not allowed.

from Config.Util import *
from Config.Config import *
try:
    import requests
except Exception as e:
    ErrorModule(e)

Title("Id Details")

try:
    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}

    print(f"\n{BEFORE + AFTER} {INFO} Selected User-Agent: {white + user_agent}")
    roblox_id = input(f"{BEFORE + AFTER} {INPUT} ID -> {color.RESET}")
    print(f"{BEFORE + AFTER} {WAIT} Retrieving Information..{reset}")
    try:

        api_response = requests.get(f"https://users.roblox.com/v1/users/{roblox_id}", headers=headers)
        user_data = api_response.json()

        user_id = user_data.get('id', "None")
        display_name = user_data.get('displayName', "None")
        username = user_data.get('name', "None")
        description = user_data.get('description', "None")
        account_created = user_data.get('created', "None")
        banned_status = user_data.get('isBanned', "None")
        external_app_name = user_data.get('externalAppDisplayName', "None")
        verified_badge = user_data.get('hasVerifiedBadge', "None")

        print(f"""
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} Username       : {white}{username}{red}
 {INFO_ADD} Display Name   : {white}{display_name}{red}
 {INFO_ADD} Id             : {white}{user_id}{red}
 {INFO_ADD} Created        : {white}{account_created}{red}
 {INFO_ADD} Banned         : {white}{banned_status}{red}
 {INFO_ADD} Verified  : {white}{verified_badge}{red}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    """)
        Continue()
        Reset()
    except:
        ErrorId()
except Exception as e:
    Error(e)

