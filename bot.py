#Чат-бот ТГ, который поможет подобрать необходимый автомобиль для аренды, оставить заявку, узнать информацию об аренде, оставить отзыв
import telebot
import config
from telebot import types
bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    #keyboard
    keyboardmain = types.InlineKeyboardMarkup(row_width=4)
    item1 = types.InlineKeyboardButton(text='Подобрать авто', callback_data='first')
    item2 = types.InlineKeyboardButton(text='Оставить заявку', callback_data='second')
    item3 = types.InlineKeyboardButton(text='Информация', callback_data='third')
    item4 = types.InlineKeyboardButton(text='Отзыв', callback_data='fourth')

    keyboardmain.add(item1, item2, item3, item4)
#приветствие клиента
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы помочь подобрать автомобиль в аренду.'.format(message.from_user, bot.get_me()),parse_mode='html', reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    if call.data == 'mainmenu':
        keyboardmain = types.InlineKeyboardMarkup(row_width=4)
        item1 = types.InlineKeyboardButton(text='Подобрать авто', callback_data='first')
        item2 = types.InlineKeyboardButton(text='Оставить заявку', callback_data='second')
        item3 = types.InlineKeyboardButton(text='Информация', callback_data='third')
        item4 = types.InlineKeyboardButton(text='Отзыв', callback_data='fourth')
        keyboardmain.add(item1, item2, item3, item4)
bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text='меню',reply_markup=keyboardmain)

    if call.data == 'first':
        keyboard = types.InlineKeyboardMarkup()
        func1 = types.InlineKeyboardMarkup(text='грузовой', callback_data='g')
        func2 = types.InlineKeyboardMarkup(text='пассажирский', callback_data='p')
        func3 = types.InlineKeyboardMarkup(text='промтоварный', callback_data='t')
        func4 = types.InlineKeyboardMarkup(text='специальный', callback_data='s')
        backbutton = types.InlineKeyboardButton(text='назад', callback_data= 'mainmenu')
        keyboard.add(func1, func2, func3, func4, backbutton)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='выберите функцию', reply_markup=keyboard)
    elif call.data == 'second':
        name = ''
        mail = ''
        num = 0
        def req(message):
            if message.text == 'Заявка':
                bot.send_message(message.from_user.id, 'Введите ваши Фамилию Имя')
                bot.register_next_step_handler(message, get_name) #следующий шаг – функция get_name
            else:
                bot.send_message(message.from_user.id, 'Напишите Заявка')

        def get_name(message): #получаем ФИ
            global name
            name = message.text
            bot.send_message(message.from_user.id, 'Введите вашу почту')
            bot.register_next_step_handler(message, get_mail)

        def get_mail(message):
            global mail
            mail = message.text
            bot.send_message('Введите ваш телефон')
            bot.register_next_step_handler(message, get_num)

        def get_num(message):
            global num
            while num == 0:
                try:
                     num = int(message.text) #проверяем, что телефон введен корректно
                except Exception:
                     bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')
            bot.send_message(message.from_user.id, 'Проверь введеную информацию')

    elif call.data == 'third':
        keyboard3 = types.InlineKeyboardMarkup()
        qest1 = types.InlineKeyboardMarkup(text='На какой срок я могу взять автомобиль в аренду?', callback_data='q1')
        qest2 = types.InlineKeyboardMarkup(text='Как происходит оформление аренды?', callback_data='q2')
        qest3 = types.InlineKeyboardMarkup(text='Могу ли я провести предварительный расчет стоимости аренды?', callback_data='q3')
        qest4 = types.InlineKeyboardMarkup(text='Входит ли страхование в аренду?', callback_data='q4')
        qest5 = types.InlineKeyboardMarkup(text='Сервисное обслуживание автомобиля по сервисному контракту', callback_data='q5')
        qest6 = types.InlineKeyboardMarkup(text='Дополнительные услуги', callback_data='q6')
        backbutton = types.InlineKeyboardButton(text='назад', callback_data= 'mainmenu')
        keyboard3.add(qest1, qest2, qest3, qest4, qest5, qest6, backbutton)
        bot.send_message(message.chat.id, 'Что вас интересует?')

    elif call.data == 'fourth':
        rev = ''
        global rev
        rev = message.text
        bot.send_message('Введите отзыв')


    elif call.data == 'g' or call.data == 'p' or call.data == 't' or call.data == 's':
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text='грузоподъемность')
        keyboard5 = types.InlineKeyboardMarkup()
        gp1 = types.InlineKeyboardButton(text='1 т - 2,6 т', callback_data='light')
        gp2 = types.InlineKeyboardButton(text='2,7 т - 6,2 т', callback_data='heavy')
        backbutton = types.InlineKeyboardButton(text='назад', callback_data= 'mainmenu')
        keyboard5.add(gp1, gp2, backbutton)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='выбор сделан', reply_markup=keyboard3)

bot.polling(none_stop=True)


