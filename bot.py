from config import TOKEN
import telebot
from telebot import types
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_instructions(message):
    instructions = ("Welcome to Currency Converter Bot!\n\n"
                    "To get the price of a certain amount of currency, "
                    "type the message in the following format:\n\n"
                    "<currency_to_convert> <desired_currency> <amount>\n\n"
                    "For example: USD EUR 100\n\n"
                    "To see the list of available currencies, type /values")
    bot.reply_to(message, instructions)

@bot.message_handler(commands=['values'])
def send_currency_list(message):
    currency_list = ("Available currencies:\n"
                     "USD - US Dollar\n"
                     "EUR - Euro\n"
                     "RUB - Russian Ruble\n"
                     "and more...")
    bot.reply_to(message, currency_list)

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        text = message.text.split()
        if len(text) != 3:
            raise APIException("Invalid input. Please use the format: <currency_to_convert> <desired_currency> <amount>")
        base_currency, quote_currency, amount = text
        converted_amount = CurrencyConverter.get_price(base_currency, quote_currency, float(amount))
        response = f"{amount} {base_currency} equals {converted_amount:.2f} {quote_currency}"
        bot.reply_to(message, response)
    except APIException as e:
        bot.reply_to(message, f"Error: {e}")

bot.polling()