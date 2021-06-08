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
