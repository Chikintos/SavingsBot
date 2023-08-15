import telebot
from telebot import types
# start keyboard
button_create = types.KeyboardButton('🌱 Створити заощадження')
button_edit = types.KeyboardButton('✏️ Редагува заощадження')
button_view = types.KeyboardButton('👁️‍🗨️ Переглянути заощадження')
button_delete= types.KeyboardButton('❌ Видалити заощадження')
button_story= types.KeyboardButton('📖 Переглянути історію')
button_stop= types.KeyboardButton('🤚🏻 Припинит дію')

button_UAH = types.KeyboardButton('🇺🇦 UAH')
button_USD = types.KeyboardButton('🇺🇸 USD')
button_EUR = types.KeyboardButton('🇪🇺 EUR')

# default keyboard
def_keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True)
def_keyboard.add(button_create,button_edit,button_view,button_story,button_delete)


# start keyboard
start_keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True)
start_keyboard.add(button_create)

# action keyboard
action_keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True)
action_keyboard.add(button_stop)


# currencykeyboard
currency_keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True)
currency_keyboard.add(button_UAH,button_USD,button_EUR)


# edit keyboard
def Generate_edit_keyboard(groups,task):
    edit_keyboard = types.InlineKeyboardMarkup(row_width=2)
    for saving in groups:
        button=types.InlineKeyboardButton(f"{saving.name}|\n{saving.description}",callback_data=f"{task}|{saving.id}")
        edit_keyboard.add(button)

    return edit_keyboard