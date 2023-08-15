import telebot
from keyboards import *
import db_operations
import tabulate
import os
from dotenv import load_dotenv


# Initialize the bot
load_dotenv()
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(bot_token)
user_states = {}


# Get the list of savings in a tabular format
def get_saving_list(user_id):
    saving_list = db_operations.Get_saving(user_id)
    formated_savings = [[saving.id, saving.name, saving.description,
                         f"{saving.balance} {saving.currency}"] for saving in saving_list]
    formated_savings.insert(0, ["ID", "NAME", "DESCRIPTION", "BALANCE"])
    table = tabulate.tabulate(formated_savings)
    return table



# Handle the /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привіт,я допоможу тобі вести облік твоїх заощаджень.\nЩоб дізнатись більш детально про мене скористайся командою /help ", reply_markup=start_keyboard)



# Handle the /help command
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(
        message.chat.id, "Список доступних команд:\n/start - почати дiалог\n")


# Handle the "🤚🏻 Stop Action" button
@bot.message_handler(func=lambda message: message.text == '🤚🏻 Припинит дію')
def create_savings(message):
    user_states.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "Дію припинено",
                     reply_markup=def_keyboard)


# Create saving
@bot.message_handler(func=lambda message: message.text == '🌱 Створити заощадження')
def create_savings(message):
    user_states[message.chat.id] = 'enter_name'
    bot.send_message(message.chat.id, "Введіть ім'я заощадження:",
                     reply_markup=action_keyboard)


# Create saving/getting name
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'enter_name')
def enter_description(message):
    if len(message.text) > 30:
        return bot.send_message(message.chat.id, "Обране ім'я занадто довге(більше 30 символів). Введіть коротше.")
    user_states[message.chat.id] = 'enter_description'
    user_states['name'] = message.text
    bot.send_message(
        message.chat.id, "Введіть опис до заощадження\nМожете описати ціль ")

# Create saving/getting description
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'enter_description')
def enter_balance(message):
    if len(message.text) > 150:
        return bot.send_message(message.chat.id, "Обраний опис занадто довгий(більше 150 символів). Введіть коротший.")
    user_states[message.chat.id] = 'enter_balance'
    user_states['description'] = message.text
    bot.send_message(
        message.chat.id, "Введіть початковий баланс до заощадження\nМожете просто написати 0")
    

# Create saving/getting balance
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'enter_balance')
def enter_curency(message):
    if len(message.text) > 12:
        return bot.send_message(message.chat.id, "Баланс не може бути довше ніж 12 символів завдовшки. Введіть коротше.")
    try:
        float(message.text.strip())
    except ValueError:
        return bot.send_message(message.chat.id, "Баланс має бути вказаний цифрами,при вказанні нецілого \
                                числа символ крапки '.' застосовується як роздільник.\nПриклад: 12.45")

    user_states[message.chat.id] = 'enter_currency'
    user_states['balance'] = message.text
    bot.send_message(message.chat.id, "Введіть валюту,в якім вестиме заощадження\nМожете обрати на клавіатурі або ввести самостійно",
                     reply_markup=currency_keyboard)



# Create saving/getting currency
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'enter_currency')
def save_savings(message):
    if len(message.text) > 10:
        return bot.send_message(message.chat.id, "Валюта не може бути довше ніж 10 символів завдовшки. Введіть коротше.")
    user_states.pop(message.chat.id, None)
    name = user_states['name']
    description = user_states['description']
    balance = user_states['balance']
    currency = message.text
    user_id = message.chat.id
    if message.chat.first_name:
        username = message.chat.first_name
    else:
        username = message.chat.username
    db_operations.Create_savings(
        user_id, username, name, description, balance, currency)
    bot.send_message(
        message.chat.id, f"Збереження {name} створено", reply_markup=def_keyboard)



# Edit saving
@bot.message_handler(func=lambda message: message.text == '✏️ Редагува заощадження')
def edit_save(message):
    saving_list = db_operations.Get_saving(message.chat.id)
    save_savings_kb = Generate_edit_keyboard(saving_list, "edit")

    bot.send_message(
        message.chat.id, "Виберіть заощадження для редагування:", reply_markup=save_savings_kb)


# Edit saving/getting_savingId
@bot.callback_query_handler(func=lambda call: call.data.count("edit") == 1)
def callback_handler(call):
    user_states[call.message.chat.id] = 'edit_saving'
    user_states["saving_id"] = call.data.split("|")[-1]
    bot.send_message(call.message.chat.id,
                     "Введіть суму, на яку бажаєте збільшити заощадження\nЯкщо ж бажаєте зменшити просто додайте '-' перед числом ")


# Edit saving/commit_editind
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'edit_saving')
def commit_edit_save(message):
    try:
        float(message.text.strip())
    except ValueError:
        return bot.send_message(message.chat.id, "Число має бути вказаний цифрами,при вказанні нецілого \
                                числа символ крапки '.' застосовується як роздільник.\nПриклад: 12.45")
    user_states.pop(message.chat.id, None)
    db_operations.Change_saving(user_states["saving_id"], message.text)
    bot.send_message(message.chat.id, f"Редагування успішне",
                     reply_markup=def_keyboard)


# Get savings
@bot.message_handler(func=lambda message: message.text == '👁️‍🗨️ Переглянути заощадження')
def get_view(message):
    user_states[message.chat.id] = 'get_view'
    saving_table = get_saving_list(message.chat.id)
    bot.send_message(
        message.chat.id, f"<pre>{saving_table}</pre>", parse_mode="HTML")



# Delete saving 
@bot.message_handler(func=lambda message: message.text == '❌ Видалити заощадження')
def delete_save(message):

    saving_list = db_operations.Get_saving(message.chat.id)
    save_savings_kb = Generate_edit_keyboard(saving_list, "delete")
    bot.send_message(
        message.chat.id, "Виберіть заощадження для видалення", reply_markup=save_savings_kb)

# Delete saving/get savingId
@bot.callback_query_handler(func=lambda call: call.data.count("delete") == 1)
def callback_handler(call):
    data = call.data.split("|")[-1]
    db_operations.Delete_saving(int(data))
    bot.send_message(
            call.message.chat.id, "Видалення успішне")

# View savings history
@bot.message_handler(func=lambda message: message.text == '📖 Переглянути історію')
def history_view(message):

    saving_list = db_operations.Get_saving(message.chat.id)
    save_savings_kb = Generate_edit_keyboard(saving_list, "history")
    bot.send_message(
        message.chat.id, "Виберіть заощадження для перегляду його історії", reply_markup=save_savings_kb)


# View savings history/get history_id
@bot.callback_query_handler(func=lambda call: call.data.count("history") != 0)
def history_callback(call):
    save_story = db_operations.get_saving_history(call.data.split("|")[-1])
    formated_story = [[story.id, story.action, story.date]
                      for story in save_story]
    formated_story.insert(0, ["ID", "ACTION", "DATE"])
    table = tabulate.tabulate(formated_story)
    bot.send_message(call.message.chat.id,
                     f"<pre>{table}</pre>", parse_mode="HTML")



# Handle text messages
@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(
        message.chat.id, f"Ви написали: {message.text},скористайтесь клавіатурою або командою /start")


# Start polling the bot
bot.polling()
