import time
import discord
from datetime import datetime
from trade_api import TradeApi
from trade_cypher import TradeCypher


class AlertBot:
    # Class variables : same for every instance unless
    #  - use just to initialize a variable
    #  - using instance variable to redefine it
    discord_c = discord.Client()
    now = datetime.now()

    def __init__(self, key, channel_id):
        # Instance variables
        self.channel_id = channel_id
        self.trade_api = TradeApi()
        self.cypher = TradeCypher()
        self.current_time = self.now.strftime("%H:%M:%S")

        # register an event
        # discord.py is an asynchronous library
        # This are done with callbacks (A function which is gonna call if something happened)
        @self.discord_c.event  # event decorator
        async def on_ready():
            print("[*] Logged in as {0.user}".format(self.discord_c))
            # first find the channel ID
            # Settings -> Advanced -> Turn on Developer Mode
            # Go to the channel and right click on it & then -> Copy ID 629504251311423494
            channel = self.discord_c.get_channel(self.channel_id)

            # Getting coin change for predefined coins
            fav_coin_pairs = ['BNBETH', 'BNBUSDT', 'ETHUSDT']
            recent_trade_total = 0.15105000  # total column value of recent trade
            recent_trade_executed = 0.57  # executed column value of recent trade
            previous_int_set = [0, 0, 0]  # To store the previous change rounded off value
            while True:
                await self.trade_check_selling_margin(channel, fav_coin_pairs[0], recent_trade_total, recent_trade_executed)
                time.sleep(10)
                # setting recent pair change rounded off value
                # previous_int_set = await self.get_coin_change(channel, fav_coin_pairs, previous_int_set)

        self.discord_c.run(self.cypher.decryption(self.cypher.get_key(), key))

    async def cs_decision_taker(self, channel, value_set, previous_int_set):
        """change stats decision taker"""

        current_int_set = []
        # recording current rounded off price change percent for each coin pairs
        for key in value_set.keys():
            current_int_set.append(value_set[key]['princeChangeIntRoundOff'])

        for key in value_set.keys():
            if current_int_set[list(value_set.keys()).index(key)] > previous_int_set[list(value_set.keys()).index(key)]:
                value_set[key]['sign'] = '+'
            elif current_int_set[list(value_set.keys()).index(key)] < previous_int_set[
                list(value_set.keys()).index(key)]:
                value_set[key]['sign'] = '-'
            else:
                value_set[key]['sign'] = '!'

        f_message = """```diff\n{} {}\nPrice Change Percent : {}\nPrice : {}\n\n""" \
                    """{} {}\nPrice Change Percent : {}\nPrice : {}\n\n""" \
                    """{} {}\nPrice Change Percent : {}\nPrice : {}```""".format(
            value_set['BNBETH']['sign'], value_set['BNBETH']['symbol'], value_set['BNBETH']['priceChangePercent'],
            value_set['BNBETH']['lastPrice'],
            value_set['BNBUSDT']['sign'], value_set['BNBUSDT']['symbol'], value_set['BNBUSDT']['priceChangePercent'],
            value_set['BNBUSDT']['lastPrice'],
            value_set['ETHUSDT']['sign'], value_set['ETHUSDT']['symbol'], value_set['ETHUSDT']['priceChangePercent'],
            value_set['ETHUSDT']['lastPrice'])

        if current_int_set > previous_int_set:
            await channel.send("```diff\n+ [#] Price is getting Increase\n```\n" + f_message)
        elif current_int_set < previous_int_set:
            await channel.send("```diff\n- [!] Price is getting Decrease\n```\n" + f_message)
        else:
            pass

        return current_int_set

    async def get_coin_change(self, channel, fav_coin_pairs, previous_int_set):
        change_stats_sets = {}

        for symbol in fav_coin_pairs:
            # getting the stats & adding coin pairs stats to dict
            change_stats_sets[symbol] = self.trade_api.get_change_stats(symbol)

        return await self.cs_decision_taker(channel, change_stats_sets, previous_int_set)

    async def trade_check_selling_margin(self, channel, symbol, recent_trade_total, recent_trade_executed):

        crypto_stats = self.trade_api.get_change_stats('BNBETH')
        current_sell_crypto_price = crypto_stats['lastPrice']
        f_message = """```diff\n# {}\nPrice : {}\nPrice Change Percent : {}\n```""" \
                    .format(crypto_stats['symbol'], crypto_stats['lastPrice'], crypto_stats['priceChangePercent'])

        if current_sell_crypto_price * recent_trade_executed > recent_trade_total:
            await channel.send("```diff\n+ [#] Comes to a profitable margin point. Keep in touch\n```\n" + f_message)
        else:
            print("[!] {} Bot is running".format(self.current_time))

