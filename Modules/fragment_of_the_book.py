# -*- coding: utf8 -*-
import codecs
import sys
sys.path.append("..")
import kirptestbot as b

def fragment_of_book(message):
    try:
        if message.text == 'Бесы':
            with codecs.open('Бесы.txt', encoding='utf-8') as demons:
                read_demons = demons.read()
            b.bot.send_message(message.chat.id, text=read_demons, reply_markup=b.mark_up_6)
        elif message.text == 'Заповедник':
            with codecs.open('Заповедник.txt', encoding='utf-8') as reserve:
                read_reserve = reserve.read()
            b.bot.send_message(message.chat.id, text=read_reserve, reply_markup=b.mark_up_6)
        else:
            b.bot.send_message(message.chat.id, 'Название книги неверное. Попробуйте снова', reply_markup=b.mark_up_6)
    except:
        b.bot.send_message(message.chat.id, 'Произошла ошибка. Попробуйте снова', reply_markup=b.mark_up_6)
