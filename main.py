from alert_bot import AlertBot


# run the code only if it's running directly from the command line
# not when importing through a file
if __name__ == "__main__":

    try:
        key = b'xxxxxxxxxxxxxxxxxxxxx' \
              b'xxxxxxxxxxxxxxxxxxxxx'  # Discord bot client key goes here
        channel_id = 00000000000000     # Discord channel ID
        AlertBot(key, channel_id)

    except KeyboardInterrupt:
        print("[!] Safely exiting the program")
    except Exception as e:
        print(e)
        print("[!] Password is incorrect ! Please try again")
