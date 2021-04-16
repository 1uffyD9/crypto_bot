#!/usr/bin/env python3

import os,sys
from decouple import config
from alert_bot import AlertBot


# run the code only if it's running directly from the command line
# not when importing through a file
if __name__ == "__main__":

    try:
        key = str.encode(config('CRYPTO_BOT_KEY'))  # Discord Bot key
        channel_id = int(config('CHANNEL_ID'))      # Discord channel ID
        AlertBot(key, channel_id)

    except KeyboardInterrupt:
        print("[!] Safely exiting the program")
    except Exception as e:
        print(e)
        print("[!] Password is incorrect ! Please try again")
