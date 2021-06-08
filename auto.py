@bot.message_handler(commands=['function'])
def get_function(message):
markup = types.InlineKeyboardMarkup(resize_keyboard=True)
    func1 = types.KeyboardButton('грузовой')
    func2 = types.KeyboardButton('пассажирский')
    func3 = types.KeyboardButton('промтоварный')
    func4 = types.KeyboardButton('специальный')

    markup.add(func1, func2, func3, func4)
    bot.send_message(message.chat.id, 'Выберите какую функцию будет выполнять авто?')
    bot.register_next_step_handler(message, get_capacity)

def get_capacity(message):
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    gp1 = types.KeyboardButton('1 т - 2,6 т')
    gp2 = types.KeyboardButton('2,7 т - 6,2 т')

    markup.add(gp1, gp2)
bot.send_message(message.chat.id, 'Выберите какая грузоподъемность авто необходима')