from telegram import ReplyKeyboardMarkup, KeyboardButton

def control_buttons():
    keyboards = [[KeyboardButton("Новый вопрос"), KeyboardButton("Сдаться")],
                 [KeyboardButton("Мой счёт")]]
    return ReplyKeyboardMarkup(keyboards, resize_keyboard=True, one_time_keyboard=False)