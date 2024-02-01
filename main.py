import telebot
from telebot import types
import re

TOKEN = '6361558655:AAGuCAZALMvTL75kAJuNPQ0_ax8TntiNRms'


bot = telebot.TeleBot(TOKEN)

#phone_number_regex = re.compile(r'^(\+9|8)\d{11}$')
age_regex = re.compile(r'^\d.*')
district_regex = re.compile(r'^\D.*')
data = {}
request_chat_id = '-4187417462'


@bot.message_handler(commands=['start'])

def enter_district(message):
    clear_data(message)
    data[message.chat.id] = {'stage':0}
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text='Сысерть', callback_data='Сысерть')
    itembtn2 = types.InlineKeyboardButton(text='КП "Заповедник"', callback_data='КП "Заповедник"')
    
    
    markup.add(itembtn1, itembtn2)
    bot.send_photo(message.chat.id, open('kiber1.png', 'rb'))
    bot.send_message(message.chat.id, 'Школа программирования для детей KIBERone в КП "Заповедник" и в Сысерти приветствует вас!\U0001F60A\n \nКаждое воскресение мы проводим бесплатный мастер-класс по программированию для детей 6-14 лет\U0001F4BB\n \n \U00002705Расскажем, как избавить ребенка от игромании и научить компьютерной грамотности, чтобы подготовить к успешному будущему\n \n\U00002705Длительность занятия 2 часа. Все необходимое предоставим. Ничего брать с собой не нужно.\n Занятия проходят по адресам:\n\n г.Сысерть, ул. Мкр-н Новый, д. 18\n\nпос. Габиевский, проезд 1, здание 12. (КП "Заповедник")\n\nВыберите удобный для обучения район\U0001F447' , reply_markup=markup)
    
def enter_age(message):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton(text='6-8 лет', callback_data='6-8')
    itembtn2 = types.InlineKeyboardButton(text='9-11 лет', callback_data='9-11')
    itembtn3 = types.InlineKeyboardButton(text='12-14 лет', callback_data='12-14')
    markup.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.chat.id, 'Пожалуйста, укажите возраст вашего ребенка\U0001F447',reply_markup=markup)


def enter_phone_number(message):
    if data[message.chat.id]['stage'] == 2:
        bot.send_message(message.chat.id, 'Спасибо! Остался последний шаг\U0001F60A\n \nПожалуйста, отправьте контакт, по которому мы можем с Вами связаться\U0001F4F1')
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, selective=True, resize_keyboard=True)
        markup.add(types.KeyboardButton('Отправить контакт', request_contact=True))
        bot.send_message(message.chat.id, '*Нажмите на кнопку ниже, чтобы поделиться контактом*\U0001F447',parse_mode= "Markdown" , reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if data[message.chat.id]['stage'] == 2:
        data[message.chat.id]['phone_number'] = message.contact.phone_number
        data[message.chat.id]['stage'] = 3
        check_and_send(message)
    
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text.startswith('/start'):
        return
    if message.text.startswith('/getID'):
        bot.send_message(message.chat.id, message.chat.id)
        return
    if message.text.startswith('/'):
        bot.send_message(message.chat.id, 'Неверная команда')
        return 
    
def check_and_send(message):
    if district_regex.match(data[message.chat.id]['district']) and age_regex.match(data[message.chat.id]['age']):
        bot.send_message(message.chat.id, 'Спасибо! Скоро с вами свяжется наш администратор, отправит вам расписание мастер-классов на ближайшую неделю и согласует точное время\n \nДо встречи на уроке!\U0001F60A')
        bot.send_message(request_chat_id, 'Район: ' + data[message.chat.id]['district']+' Возраст: '+data[message.chat.id]['age']+' '+data[message.chat.id]['phone_number'])
        clear_data(message)
    else:
        bot.send_message(message.chat.id, 'Неправильно сформированы ответы на вопросы, поробуйте еще раз')
        enter_district(message)
    
def clear_data(message):
    if message.chat.id in data:
        del data[message.chat.id]
  
@bot.callback_query_handler(func=lambda call: True)
def answering(call):
    if call.message.chat.id in data:
        if data[call.message.chat.id]['stage'] == 0:
            data[call.message.chat.id]['district'] = call.data
            data[call.message.chat.id]['stage'] = 1
            enter_age(call.message)
        elif data[call.message.chat.id]['stage'] == 1:
            data[call.message.chat.id]['age'] = call.data
            data[call.message.chat.id]['stage'] = 2
            enter_phone_number(call.message)
bot.infinity_polling()
