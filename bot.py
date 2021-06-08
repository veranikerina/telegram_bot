#Чат-бот ТГ, который поможет подобрать необходимый автомобиль для аренды, оставить заявку, узнать информацию об аренде, оставить отзыв
import telebot
import config
from telebot import types
from requests import get
bot = telebot.TeleBot(config.TOKEN)

name = ''
mail = ''
num = 0

def create_main_menu():
    keyboardmain = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton(text='Подобрать авто', callback_data='first')
    item2 = types.InlineKeyboardButton(text='Рассчитать стоимость', callback_data='second')
    item3 = types.InlineKeyboardButton(text='Оставить заявку', callback_data='third')
    item4 = types.InlineKeyboardButton(text='Информация', callback_data='fourth')
    item5 = types.InlineKeyboardButton(text='Отзыв', callback_data='fifth')

    keyboardmain.add(item1, item2, item3, item4, item5)
    return keyboardmain

@bot.message_handler(commands=['start'])
def welcome(message):
    # keyboard
    keyboardmain = create_main_menu()
    # приветствие клиента
    bot.send_message(message.chat.id,'Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы помочь подобрать автомобиль в аренду.'.format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=keyboardmain)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    message = call.message
    if call.data == 'mainmenu':
        keyboardmain = create_main_menu()
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='меню', reply_markup=keyboardmain)

    if call.data in ['first', 'second', 'third', 'fourth', 'fifth']:
        if call.data == 'first':
            keyboard = types.InlineKeyboardMarkup()
            func1 = types.InlineKeyboardButton(text='грузовой', callback_data='g')
            func2 = types.InlineKeyboardButton(text='пассажирский', callback_data='p')
            func3 = types.InlineKeyboardButton(text='промтоварный', callback_data='t')
            func4 = types.InlineKeyboardButton(text='специальный', callback_data='s')
            backbutton = types.InlineKeyboardButton(text='назад', callback_data='mainmenu')
            keyboard.add(func1, func2, func3, func4, backbutton)

            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='выберите функцию', reply_markup=keyboard)

        elif call.data == 'second':
            bot.send_message(message.chat.id, 'Для рассчета стоимости перейдите к боту @GazCalc_Bot')

        elif call.data == 'third':
            def req(message):
                bot.send_message(message.chat.id, 'Введите ваши ФИО')
                bot.register_next_step_handler(message, get_name)  # следующий шаг – функция get_name

            def get_name(message):  # получаем ФИ
                global name
                name = message.text
                bot.send_message(message.chat.id, 'Введите вашу почту')
                bot.register_next_step_handler(message, get_mail)

            def get_mail(message):
                global mail
                mail = message.text
                bot.send_message(message.chat.id, 'Введите ваш телефон')
                bot.register_next_step_handler(message, get_num)

            def get_num(message):
                global num
                try:
                    num = int(message.text)  # проверяем, что телефон введен корректно
                    bot.send_message(message.chat.id, 'Данные вашей заявки: ФИО - {}, почта - {}, телефон - {}. Заявка отправлена.'.format(name, mail, num))
                    with open('req.txt', 'a') as fd:
                        fd.write('{}, {}, {}\n'.format(name, mail, num))
                except Exception:
                    bot.send_message(message.chat.id, 'Цифрами, пожалуйста')
                    bot.register_next_step_handler(message, get_num)

            req(message)

        elif call.data == 'fourth':
            keyboard3 = types.InlineKeyboardMarkup(row_width=1)
            qest1 = types.InlineKeyboardButton(text='Срок аренды', callback_data='q1')
            qest2 = types.InlineKeyboardButton(text='Оформление аренды', callback_data='q2')
            qest3 = types.InlineKeyboardButton(text='Предварительный расчет стоимости аренды',callback_data='q3')
            qest4 = types.InlineKeyboardButton(text='Страхование', callback_data='q4')
            qest5 = types.InlineKeyboardButton(text='Сервисное обслуживание',callback_data='q5')
            qest6 = types.InlineKeyboardButton(text='Дополнительные услуги', callback_data='q6')
            backbutton = types.InlineKeyboardButton(text='назад', callback_data='mainmenu')
            keyboard3.add(qest1, qest2, qest3, qest4, qest5, qest6, backbutton)
            bot.send_message(message.chat.id, 'Что вас интересует?', reply_markup=keyboard3)

        elif call.data == 'fifth':
            global rev
            rev = ''
            rev = message.text
            bot.send_message(message.chat.id, 'Введите отзыв')

    if call.data in ['g', 'p', 't', 's']:
        if call.data == 'g':
            bot.send_message(message.chat.id, 'Для вас подойдет ГАЗон Next')
            bot.send_photo(message.chat.id, get('https://azgaz.ru/upload/resize_cache/iblock/cbb/950_495_0/cbbfcabcffabef867f2438e0029bb590.jpg').content)
            bot.send_message(message.chat.id, 'или ГАЗель Next')
            bot.send_photo(message.chat.id, get('https://azgaz.ru/upload/resize_cache/iblock/76d/950_495_0/76d347a35b1c275d11a05f15fda153e0.jpg').content)
        elif call.data == 'p':
            bot.send_message(message.chat.id, 'Для вас подойдет ГАЗель Next')
            bot.send_photo(message.chat.id, get('https://azgaz.ru/upload/resize_cache/iblock/3e3/950_495_0/3e3c8cade88e53f45917a982b787c0db.jpg').content)
            bot.send_message(message.chat.id, 'или ГАЗель City')
            bot.send_photo(message.chat.id, get('https://azgaz.ru/new-style/images/innoprom2021/city_bus.png').content)

        elif call.data == 't':
            bot.send_message(message.chat.id, 'Для вас подойдет Валдай Next')
            bot.send_photo(message.chat.id, get('https://azgaz.ru/upload/resize_cache/iblock/043/950_495_0/Valday-Next-Retouch-and-moldindg-replacement-DSC07926-extended-copy.jpg').content)

        elif call.data == 's':
            bot.send_message(message.chat.id, 'Для вас подойдет ГАЗон Next')
            bot.send_photo(message.chat.id, get('https://azgaz.ru/upload/resize_cache/iblock/853/950_495_0/8531b7464b0788a1a1e306e6a15c4689.jpg').content)

    if call.data in ['q1', 'q2', 'q3', 'q4', 'q5', 'q6']:
        if call.data == 'q1':
            bot.send_message(message.chat.id, 'Срок аренды от 6 месяцев до 3 лет')
        if call.data == 'q2':
            bot.send_message(message.chat.id, 'Для оформления аренды необходимо оставить заявку, затем с вами свяжется менеджер для уточнения условий. В офисе компании составляется и подписывается договор аренды.')
        if call.data == 'q3':
            bot.send_message(message.chat.id, 'Предварительный расчет аренды производится на нашем сайте http://gaz-arenda.tilda.ws/ или в телеграмботе @GazCalc_Bot')
        if call.data == 'q4':
            bot.send_message(message.chat.id, 'В аренду входит страховка КАСКО, ОСАГО, НС, а также страхование пассажиров')
        if call.data == 'q5':
            bot.send_message(message.chat.id, 'Сервисное обслуживание включает в себя ТО, ремонт и замену деталей')
        if call.data == 'q6':
            bot.send_message(message.chat.id, 'Среди дополнительных услуг: защита от поломок, подменный автомобиль, коучинг водителей')

bot.polling(none_stop=True)
