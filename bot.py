#Чат-бот ТГ, который поможет подобрать необходимый автомобиль для аренды, оставить заявку, узнать информацию об аренде, оставить отзыв
import telebot
import config
from telebot import types
from requests import get
bot = telebot.TeleBot(config.TOKEN)

name = ''
mail = ''
rev = ''
num = 0

@bot.message_handler(commands=['start'])
def start(message):
    keyboardmain = types.ReplyKeyboardMarkup(resize_keyboard = True)
    item1 = types.KeyboardButton('Подобрать авто')
    item2 = types.KeyboardButton('Рассчитать стоимость')
    item3 = types.KeyboardButton('Оставить заявку')
    item4 = types.KeyboardButton('Информация')
    item5 = types.KeyboardButton('Отзыв')

    keyboardmain.add(item1, item2, item3, item4, item5)

    bot.send_message(message.chat.id,'Привет, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот созданный чтобы помочь подобрать автомобиль в аренду.'.format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=keyboardmain)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text in ['Подобрать авто', 'Рассчитать стоимость', 'Оставить заявку', 'Информация', 'Отзыв']:
            if message.text == 'Подобрать авто':
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard = True)
                func1 = types.KeyboardButton(text='грузовой')
                func2 = types.KeyboardButton(text='пассажирский')
                func3 = types.KeyboardButton(text='промтоварный')
                func4 = types.KeyboardButton(text='специальный')
                backbutton = types.KeyboardButton(text='назад')
                keyboard.add(func1, func2, func3, func4, backbutton)

                bot.send_message(message.chat.id, 'Выберите функцию', reply_markup=keyboard)

            elif message.text == 'Рассчитать стоимость':
                bot.send_message(message.chat.id, 'Для рассчета стоимости перейдите к боту @GazCalc_Bot')

            elif message.text == 'Оставить заявку':
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

            elif message.text == 'Информация':
                keyboard3 = types.ReplyKeyboardMarkup()
                qest1 = types.KeyboardButton(text='Срок аренды')
                qest2 = types.KeyboardButton(text='Оформление аренды')
                qest3 = types.KeyboardButton(text='Предварительный расчет стоимости аренды')
                qest4 = types.KeyboardButton(text='Страхование')
                qest5 = types.KeyboardButton(text='Сервисное обслуживание')
                qest6 = types.KeyboardButton(text='Дополнительные услуги')
                backbutton = types.KeyboardButton(text='назад')
                keyboard3.add(qest1, qest2, qest3, qest4, qest5, qest6, backbutton)
                bot.send_message(message.chat.id, 'Что вас интересует?', reply_markup=keyboard3)

            elif message.text == 'Отзыв':
                bot.send_message(message.chat.id, 'Введите ваш отзыв')
                global rev
                rev = message.text
                bot.send_message(message.chat.id, 'Ваш отзыв: - {}'.format(rev))
                with open('rev.txt', 'a') as fd:
                        fd.write('{}\n'.format(rev))

        if message.text in ['грузовой', 'пассажирский', 'промтоварный', 'специальный', 'назад']:
            if message.text == 'грузовой':
                bot.send_message(message.chat.id, 'Для вас подойдет ГАЗон Next')
                bot.send_photo(message.chat.id, get('https://azgaz.ru/upload/resize_cache/iblock/cbb/950_495_0/cbbfcabcffabef867f2438e0029bb590.jpg').content)
                bot.send_message(message.chat.id, 'или ГАЗель Next')
                bot.send_photo(message.chat.id, get('https://azgaz.ru/upload/resize_cache/iblock/76d/950_495_0/76d347a35b1c275d11a05f15fda153e0.jpg').content)

            elif message.text == 'пассажирский':
                bot.send_message(message.chat.id, 'Для вас подойдет ГАЗель Next')
                bot.send_photo(message.chat.id, get('https://azgaz.ru/upload/resize_cache/iblock/3e3/950_495_0/3e3c8cade88e53f45917a982b787c0db.jpg').content)
                bot.send_message(message.chat.id, 'или ГАЗель City')
                bot.send_photo(message.chat.id, get('https://azgaz.ru/new-style/images/innoprom2021/city_bus.png').content)

            elif message.text == 'промтоварный':
                bot.send_message(message.chat.id, 'Для вас подойдет Валдай Next')
                bot.send_photo(message.chat.id, get('https://azgaz.ru/upload/resize_cache/iblock/043/950_495_0/Valday-Next-Retouch-and-moldindg-replacement-DSC07926-extended-copy.jpg').content)

            elif message.text == 'специальный':
                bot.send_message(message.chat.id, 'Для вас подойдет ГАЗон Next')
                bot.send_photo(message.chat.id, get('https://azgaz.ru/upload/resize_cache/iblock/853/950_495_0/8531b7464b0788a1a1e306e6a15c4689.jpg').content)

            elif message.text == 'назад':
                keyboardmain = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Подобрать авто')
                item2 = types.KeyboardButton('Рассчитать стоимость')
                item3 = types.KeyboardButton('Оставить заявку')
                item4 = types.KeyboardButton('Информация')
                item5 = types.KeyboardButton('Отзыв')

                keyboardmain.add(item1, item2, item3, item4, item5)
                bot.send_message(message.chat.id, 'ок', reply_markup=keyboardmain)

        if message.text in ['Срок аренды', 'Оформление аренды', 'Предварительный расчет стоимости аренды', 'Страхование', 'Сервисное обслуживание', 'Дополнительные услуги', 'назад']:
            if message.text == 'Срок аренды':
                bot.send_message(message.chat.id, 'Срок аренды от 6 месяцев до 3 лет')
            if message.text == 'Оформление аренды':
                bot.send_message(message.chat.id, 'Для оформления аренды необходимо оставить заявку, затем с вами свяжется менеджер для уточнения условий. В офисе компании составляется и подписывается договор аренды.')
            if message.text == 'Предварительный расчет стоимости аренды':
                bot.send_message(message.chat.id, 'Предварительный расчет аренды производится на нашем сайте http://gaz-arenda.tilda.ws/ или в телеграмботе @GazCalc_Bot')
            if message.text == 'Страхование':
                bot.send_message(message.chat.id, 'В аренду входит страховка КАСКО, ОСАГО, НС, а также страхование пассажиров')
            if message.text == 'Сервисное обслуживание':
                bot.send_message(message.chat.id, 'Сервисное обслуживание включает в себя ТО, ремонт и замену деталей')
            if message.text == 'Дополнительные услуги':
                bot.send_message(message.chat.id, 'Среди дополнительных услуг: защита от поломок, подменный автомобиль, коучинг водителей')
            if message.text == 'назад':
                keyboardmain = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Подобрать авто')
                item2 = types.KeyboardButton('Рассчитать стоимость')
                item3 = types.KeyboardButton('Оставить заявку')
                item4 = types.KeyboardButton('Информация')
                item5 = types.KeyboardButton('Отзыв')

                keyboardmain.add(item1, item2, item3, item4, item5)

bot.polling(none_stop=True)