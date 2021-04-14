
### Preperation
* [Creating the api](https://binance.zendesk.com/hc/en-us/articles/360002502072-How-to-create-API)
* [Creating Discord bot](https://youtu.be/SPTfmiYiuok)
* Install the necessary libraries
  ```commandline
  $ pip install -r requirements.txt
  ```
* Run the `my_cypher.py` and provide **bot token** to generate encrypted token
  ```commandline
  $ python my_cypher.py
  [!] Please provide the password :
  [!] Add any string to encrypt: bot_token
  [!] Please Enter api key :
  [!] Please Enter secret_key :
  [*] Encrypted random string : b'gAAAAABgdajqnciy9bqXwtziiEZ45wjeo-17ZcTNkvq7r0GKpxaA=='
  [*] Encrypted key pair object :
  ```
* Copy the **encrypted bot key** from previous output and paste it as the value of the `key` variable in **main.py** script
* Get the channel ID from Discord which you want to send notifications to and set that value as the value of **channel_id** variable

### Running

* Run the script and provide the password which you used to encrypt the key pairs.
  ```commandline
  $ python main.py  
  [!] Please provide the password :
  
  ```

### To do

* Change the Discord code to make it easily customisable
