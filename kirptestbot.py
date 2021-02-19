'''
Это тестовый бот, выполняющий 3 функции:
1. Простой калькулятор
2. Узнать погоду в городе
3. Парсинг последних новостей с сайта kino.tricolor.tv
4. Прочитать фрагменты из двух книг: "Бесы" и "Заповедник"

'''
import telebot
from telebot import types
from Modules import tokens as tk
from Modules import owmapi as owm
from Modules import parsing_news as n
from Modules import fragment_of_the_book as book


BOT_TOKEN = tk.BOT_TOKEN
bot = telebot.TeleBot(BOT_TOKEN)

user_num_1 = ''
user_num_2 = ''
calc_op = ''
user_result = None
zero_degree = 0
mark_up = types.InlineKeyboardMarkup(row_width=1)
mark_up_2 = types.ReplyKeyboardMarkup(row_width=2)
mark_up_3 = types.InlineKeyboardMarkup()
mark_up_4 = types.InlineKeyboardMarkup()
mark_up_5 = types.InlineKeyboardMarkup()
mark_up_6 = types.InlineKeyboardMarkup(row_width=1)
answer_btn_1 = types.InlineKeyboardButton('Вернуться в меню', callback_data="Меню")
answer_btn_2 = types.InlineKeyboardButton('Узнать еще новость', callback_data="Еще новость")
answer_btn_3 = types.InlineKeyboardButton('Узнать погоду', callback_data="Узнать погоду")
answer_btn_4 = types.InlineKeyboardButton('Ввести название книги еще раз', callback_data="фрагмент")
item_btn_1 = types.InlineKeyboardButton('Калькулятор', callback_data="Калькулятор")
item_btn_2 = types.InlineKeyboardButton('Узнать погоду', callback_data="Узнать погоду")
item_btn_3 = types.InlineKeyboardButton('Узнать новость про кино и тв', callback_data="новости кино")
item_btn_4 = types.InlineKeyboardButton('Прочитать фрагмент из книги', callback_data="фрагмент")
calc_btn_1 = types.KeyboardButton('+')
calc_btn_2 = types.KeyboardButton('-')
calc_btn_3 = types.KeyboardButton('*')
calc_btn_4 = types.KeyboardButton('/')
calc_btn_5 = types.KeyboardButton('^')
calc_btn_6 = types.KeyboardButton('Результат')
calc_btn_7 = types.KeyboardButton('Продолжить вычисление')
mark_up.add(item_btn_1, item_btn_2, item_btn_3, item_btn_4)
mark_up_2.add(calc_btn_1, calc_btn_2, calc_btn_3, calc_btn_4, calc_btn_5)    
mark_up_4.add(answer_btn_1, answer_btn_3)   
mark_up_3.add(answer_btn_1, answer_btn_2)
mark_up_5.add(answer_btn_1)
mark_up_6.add(answer_btn_4, answer_btn_1)


# Функция приветствия.
@bot.message_handler(content_types=['text', 'document', 'audio'])

def greeting(message):
    global mess, mark_up
    mess = message
    
    
    if message.text == '/start':
        greeting_1 = 'Здравствуйте, ' + message.from_user.first_name + ', что бы вы хотели узнать?'
        bot.send_message(message.chat.id, text=greeting_1, reply_markup=mark_up)
    elif message.text == '/proceed' or message.text == 'Меню':
        greeting_1 = message.from_user.first_name + ', что бы вы еще хотели узнать?'
        bot.send_message(message.chat.id, text=greeting_1, reply_markup=mark_up)
    elif user_result != None:
        bot.load_next_step_handlers()
    else:
        bot.send_message(message.chat.id, 'Напишите /start')
    

# Обработка кнопок inline Keyboard
@bot.callback_query_handler(func=lambda call: True)

def callback_inline(call):
    global mark_up_3, mark_up_4, mark_up_5
    
    mess.text = call.data
    try:
        if call.message:
            if call.data == "Калькулятор":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выбран калькулятор.", reply_markup=None)
                bot.send_message(mess.chat.id, ('Введите число'))
                bot.register_next_step_handler(mess, calc_num1)
            elif call.data == "фрагмент":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выбрана опция получения фрагмента книги.", reply_markup=None)
                bot.send_message(mess.chat.id, ('Введите название книги'))
                bot.register_next_step_handler(mess, book.fragment_of_book)
            elif call.data == "Узнать погоду":
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выбрана погода.", reply_markup=None)
                bot.send_message(mess.chat.id, 'Укажите город')
                bot.register_next_step_handler(mess, owm.get_weather)
            elif call.data == "новости кино" or call.data == "Еще новость":
                n.news_kino_tv()
                if n.news_result == "К сожалению, актуальных новостей пока больше нет :(":
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Загрузка новости...", reply_markup=None)
                    bot.send_message(mess.chat.id, n.news_result,parse_mode='HTML', reply_markup=mark_up_5)
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Новость загружена", reply_markup=None)
                    bot.send_message(mess.chat.id, n.news_result,parse_mode='HTML', reply_markup=mark_up_3)
            elif call.data == "Меню":
                greeting_3 = mess.from_user.first_name + ', что бы вы еще хотели узнать?'
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выбрано меню", reply_markup=None)
                bot.send_message(mess.chat.id, text=greeting_3, reply_markup=mark_up) 
            else:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Выбрано другое значение")
    except Exception as e:
        print(repr(e))



# Калькулятор: функция для первого числа
def calc_num1(message, user_result=None):
    try:
        global user_num_1
        
        if user_result == None:
            user_num_1 = int(message.text)
            bot.send_message(message.from_user.id, text='Выберите операцию', reply_markup=mark_up_2)
            bot.register_next_step_handler(message, calc_operation)
           
        else:
            user_num_1 = int(user_result)
            bot.send_message(message.from_user.id, text='Выберите операцию', reply_markup=mark_up_2)
            bot.register_next_step_handler(message, calc_operation)
        
    except Exception as e:
        bot.reply_to(message, 'Возникла ошибка. Попробуйте снова.')
        bot.send_message(message.chat.id, 'Введите число')
        bot.register_next_step_handler(message, calc_num1)

# Калькулятор: функция для выбора операции и второго числа
def calc_operation(message):
    try:
        global calc_op
        
        if message.text == '^':
            calc_op = '**'
        else:
            calc_op = message.text
        mark_up_2 = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, "Введите еще число", reply_markup=mark_up_2)
        bot.register_next_step_handler(message, calc_num2)
    except Exception as e:
        bot.reply_to(message, 'Возникла ошибка. Попробуйте снова.')


# Калькулятор: функция для выбора варианта показа результата или продолжения вычислений
def calc_num2(message):
    try:
        global user_num_2, user_num_1
        user_num_2 = int(message.text)
        user_num_2_length = len(message.text)
        user_num_1_length = len(str(user_num_1))
        user_num_1_length_three = 3
        user_num_1_length_four = 4
        user_num_2_length_max = 1
        negative_first_degree =-1
        mark_up_2 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        mark_up_2.add(calc_btn_6, calc_btn_7)
        if calc_op == '**' and (((user_num_1_length >= user_num_1_length_three and user_num_1_length < user_num_1_length_four) and user_num_2_length > user_num_2_length_max) or (user_num_1_length >= user_num_1_length_four and user_num_2_length >= user_num_2_length_max and (negative_first_degree != user_num_2 and user_num_2 != user_num_2_length_max and user_num_2 != zero_degree))):
            bot.reply_to(message, 'При возведении в степень получилось слишком большое число.')
            bot.send_message(message.chat.id, 'Введите снова первое число')
            bot.register_next_step_handler(message, calc_num1)
        else:
            bot.send_message(message.chat.id, "Показать результат или продолжить операцию?", reply_markup=mark_up_2)
            bot.register_next_step_handler(message, computing_process)

    except Exception as e:
        bot.reply_to(message, 'Возникла ошибка. Попробуйте снова.')
        bot.send_message(message.chat.id, 'Введите число')
        bot.register_next_step_handler(message, calc_num2)


# Калькулятор: функция для показа результата или продолжения вычислений
def computing_process(message):
    try:
        computing()
        mark_up_2 = types.ReplyKeyboardRemove(selective=False)
        if message.text.lower() == 'результат':
            bot.send_message(message.chat.id, calc_result_print(), reply_markup=mark_up_2)
            bot.register_next_step_handler(message, greeting)
        elif message.text.lower() == 'продолжить вычисление':
            calc_num1(message, user_result)
    except Exception as e:
        bot.reply_to(message, 'Возникла ошибка. Попробуйте снова.')


# Калькулятор: функция для вычислений
def computing():
    global user_num_1, user_num_2, calc_op, user_result
    user_result = eval(str(user_num_1) + calc_op + str(user_num_2))


# Калькулятор: функция для строки результата
def calc_result_print():
    global user_num_1, user_num_2, calc_op, user_result, zero_degree
    user_result_string = str(user_result)
    user_num_1_string = str(user_num_1)
    user_num_1_string_len = len(user_num_1_string)
    user_result_string_len = len(user_result_string)
    user_result_string_len_max = 15
    user_num_1_string_len_max = 10
    print(user_num_1)
    if user_result_string_len >= user_result_string_len_max and user_num_1_string_len < user_num_1_string_len_max:
        return "Результат: " + user_num_1_string + ' ' + calc_op + ' ' + str(user_num_2) + ' = ' + "{:.0e}".format(user_result) + '\nВведите /proceed'
    
    elif user_result_string_len >= user_result_string_len_max and user_num_1_string_len >= user_num_1_string_len_max:
        return "Результат: " + '(' + "{:.0e}".format(user_num_1) +')' + ' ' + calc_op + ' ' + str(user_num_2) + ' = ' + "{:.0e}".format(user_result) + '\nВведите /proceed'
    
    elif user_num_1_string_len >= user_num_1_string_len_max and calc_op == '**' and user_num_2 == zero_degree:
        return "Результат: " + '(' + "{:.0e}".format(user_num_1) +')' + ' ' + calc_op + ' ' + str(user_num_2) + ' = ' + str(user_result) + '\nВведите /proceed'

    else:
        return "Результат: " + str(user_num_1) + ' ' + calc_op + ' ' + str(user_num_2) + ' = ' + str(user_result) + '\nВведите /proceed'

bot.enable_save_next_step_handlers(delay=2)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
