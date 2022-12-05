from calendar import calendar, month
from datetime import date

import telebot
from telebot import types
from telegram_bot_calendar import (DAY, LSTEP, MONTH, YEAR,
                                   DetailedTelegramCalendar,
                                   WMonthTelegramCalendar)

from geocoder import *
from schedule_parser import *
from taxi import *
from weather import *

DTC = DetailedTelegramCalendar
bot = telebot.TeleBot('token')
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_taxi = types.KeyboardButton("Такси")
btn_weather = types.KeyboardButton("Погода")
btn_schedule = types.KeyboardButton("Расписание")
btn_feedback = types.KeyboardButton("Отзыв")
markup.add(btn_taxi, btn_weather, btn_schedule, btn_feedback)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, text="Привет, {0.first_name}! Представляем твоему вниманию чат-бота Helping Hand!\n\n\N{LARGE BLUE CIRCLE} С помощью данного бота вы можете узнать расписание своей группы, оценить погоду или узнать цену и время в пути в такси.\n\n\N{LARGE GREEN CIRCLE} Бот предназначен для облегчения вашей жизни путём объединения некоторых функций наиболее часто используемых приложений в одно место. Таким образом, пользователи бота могут экономить время, застрачиваемое ранее на переход между приложениями.\n\n\N{LARGE RED CIRCLE} Также вы можете поддержать приложение, пожертвовав ваши кровно заработанные 25 рублей на отключение рекламы.\n\n\N{LARGE YELLOW CIRCLE} Жалобы и предложения по функционалу чат-бота можете оставить в разделе Книга жалоб".format(message.from_user), reply_markup=markup)
    





@bot.message_handler(commands=['schd'])
def start(m):
    calendar, step = WMonthTelegramCalendar(min_date=date.today(), locale='ru').build()
    bot.send_message(m.chat.id,
                     "\N{Calendar}Выберите дату!",
                     reply_markup=calendar)


@bot.callback_query_handler(func=WMonthTelegramCalendar().func())
def cal(c):
    result, key, step = WMonthTelegramCalendar(
        min_date=date.today(),locale='ru').process(c.data)
    calendar, step = WMonthTelegramCalendar(min_date=date.today()).build()
    if not result and key:
        bot.edit_message_text("\N{Calendar}Выберите дату!",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
        
    elif result:
        convert_date = datetime.strftime(result, '%d.%m.%Y')
        if result.weekday() != 6:
            bot.edit_message_text(f'Расписание на {convert_date}:\n\n {get_lesson_data(result)}',
                              c.message.chat.id, c.message.message_id)
        else: 
            bot.edit_message_text('В воскресенье отдыхаем!',c.message.chat.id, c.message.message_id)


@bot.message_handler(content_types=['text'])
def gui_handler(message):
    if (message.text.lower() == "такси"):
        markup = types.ReplyKeyboardRemove(selective=False)

        address = bot.send_message(
            message.chat.id, text="\N{World Map}Откуда вы хотите поехать? Введите адрес начальной точки в формате: Город, Улица номер дома\nНапример: Новосибирск, Достоевского 12\n\nP.S. Можно просто 'нск'\N{Winking Face}", reply_markup=markup)
        bot.register_next_step_handler(address, step_addres)

    elif (message.text.lower() == "погода"):
        markup = types.ReplyKeyboardRemove(selective=False)

        bot.send_message(message.chat.id, text=weather())

    elif (message.text.lower() == "расписание"):
        markup = types.ReplyKeyboardRemove(selective=False)

        calendar = WMonthTelegramCalendar(
            min_date=date.today(), locale='ru').build()
        bot.send_message(message.chat.id,
                         "\N{Calendar}Выберите дату!",
                         reply_markup=calendar)
    elif (message.text.lower() == "отзыв"):
        markup = types.ReplyKeyboardRemove(selective=False)
        feedback = bot.send_message(message.chat.id, "Здесь вы можете оставить свои пожелания или замечания!\N{Face with Cowboy Hat}")
        bot.register_next_step_handler(feedback,step_feedback)

    else:
        bot.send_message(message.chat.id, 'Извини, я не понимаю о чем ты :(')

def step_feedback(message):
    cid = message.chat.id
    bot.forward_message(-1001613633684,cid,message.message_id)
    #with open("pipe.txt",'w') as modified: modified.write("Новый отзыв: " + message.text + '\n')
    bot.send_message(cid,"\N{White Heavy Check Mark}Отзыв отправлен, спасибо, что помогаете улучшить бота!")

def step_addres(message):
    cid = message.chat.id
    user_addres = message.text
    global glat, glon
    glat = geo_lat(user_addres)
    glon = geo_lon(user_addres)
    end_point = bot.send_message(cid, text="\N{World Map}Куда вы хотите приехать? Введите адрес конечной точки все в том же формате!")
    bot.register_next_step_handler(end_point, end_point_ad)


def end_point_ad(message):
    cid = message.chat.id
    user_end_point = message.text

    endlat = geo_lat(user_end_point)
    endlon = geo_lon(user_end_point)

    bot.send_message(cid, taxi(glon, glat, endlat, endlon), reply_markup=markup)

    
    


bot.polling()
