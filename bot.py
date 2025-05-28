import telebot
from config import TOKEN
from extensions import APIException, CurrencyConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help_message(message):
    text = (
        "Помогу конвертировать валюту.\n"
        "Формат запроса:\n"
        "<валюта_из> <валюта_в> <кол-во>\n"
        "Пример: биткоин доллар 10\n\n"
        "Посмотреть доступные валюты: /values"
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values_message(message):
    text = "Доступные валюты:"
    for currency in CurrencyConverter.currencies:
        text += f"\n- {currency}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['text'])
def convert_currency(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            raise APIException("Неверный формат. Используйте: <валюта_из> <валюта_в> <кол-во>")

        base, quote, amount = parts
        total = CurrencyConverter.get_price(base, quote, amount)
        bot.send_message(message.chat.id, f"{amount} {base} = {total:.2f} {quote}")

    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")

    except Exception as e:
        bot.send_message(message.chat.id, f"Непредвиденная ошибка: {e}")

bot.polling()
