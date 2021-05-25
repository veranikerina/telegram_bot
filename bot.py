#Чат-бот ТГ, который поможет подобрать необходимый автомобиль для аренды, оставить заявку, узнать информацию об аренде, оставить отзыв
import telebot
import config

from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    #keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Подобрать авто')
    item2 = types.KeyboardButton('Оставить заявку')
    item3 = types.KeyboardButton('Информация')
    item4 = types.KeyboardButton('Отзыв')

    markup.add(item1, item2, item3, item4)
#приветствие клиента
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы помочь подобрать автомобиль в аренду.'.format(message.from_user, bot.get_me()),parse_mode='html', reply_markup=markup)

def close_keyboard(bot, update):
    update.message.reply_text('Ok', reply_markup=ReplyKeyboardRemove())

#меню функций чат-бота (подбор авто в аренду, оставить заявку на аренду, выбрать часто задаваемые вопросы)

@bot.message_handler(content_types=['text'])
def msg(message):
    if message.chat.type == 'private':
        if message.text == 'Подобрать авто':
            bot.send_message(message.chat.id, 'Какую функцию будет выполнять авто?')
        elif message.text == 'Оставить заявку':
            bot.send_message(message.chat.id, 'Заявка')
        elif message.text == 'Информация':
            bot.send_message(message.chat.id, 'Список вопросов')
        elif message.text == 'Отзыв':
            bot.send_message(message.chat.id, 'Нам очень важно знать ваше мнение об аренде ГАЗ')
        else:
            bot.send_message(message.chat.id, 'На это я не могу ответить')

#RUN
#bot.polling(none_stop=True)

#парсинг сайта ГК ГАЗ

#Библиотеки: requests, BeautifulSoup, csv

#Пользователь пошагово выбирает подходящие ему параметры авто:
#1.функциональность (грузовой, пассажирский, промтоварный, специальный)
#2.грузоподъемность авто (1 т - 2,6 т, 2,7 т - 6,2 т)
@bot.message_handler(commands=['function'])
def get_function(message):
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
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


#Пользователь оставляет заявку:
#1."Введите ФИО"
#2."Введите номер телефона для связи"
#3."Введите почту для связи"
#4.Услуга "подменный парк" (да/нет)
#5.Услуга "помощь на дороге" (да/нет_
#6."Введите комментарий или введите команду "отправить заявку"
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

bot.polling(none_stop=True)



#Пользователь хочет узнать информацию об аренде:
#1.На какой срок я могу взять автомобиль в аренду?
#2.Как происходит оформление аренды?
#3.Могу ли я провести предварительный расчет стоимости аренды?
#4.Входит ли страхование в аренду?
#5.Сервисное обслуживание автомобиля по сервисному контракту
#6.Дополнительные услуги

@bot.message_handler(commands=['question'])
def get_question(message):
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    qest1 = types.KeyboardButton('На какой срок я могу взять автомобиль в аренду?')
    qest2 = types.KeyboardButton('Как происходит оформление аренды?')
    qest3 = types.KeyboardButton('Могу ли я провести предварительный расчет стоимости аренды?')
    qest4 = types.KeyboardButton('Входит ли страхование в аренду?')
    qest5 = types.KeyboardButton('Сервисное обслуживание автомобиля по сервисному контракту')
    qest6 = types.KeyboardButton('Дополнительные услуги')

    markup.add(qest1, qest2, qest3, qest4, qest5, qest6)
    bot.send_message(message.chat.id, 'Что вас интересует?')
    bot.register_next_step_handler(message, pass)

#Программа парсит сайт и вытягивает необходимую информацию: г/п, функционал



