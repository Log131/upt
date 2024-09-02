from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton





def starts_():
    s = InlineKeyboardBuilder()
    s0 = InlineKeyboardButton(text='🌐 Подключить VPN', callback_data='vpn')
    s5 = InlineKeyboardButton(text='🔥 Подписка', callback_data='prems')  
    
    
    s7 = InlineKeyboardButton(text='❗️ Как установить ?', callback_data='howto')
    s6 = InlineKeyboardButton(text='🤵🏽‍♀️ Поддержка', url='https://t.me/kaif_work')
    s9 = InlineKeyboardButton(text='👥 Реффералы', callback_data='reffs')
    
    s.add(s0,s5,s9,s7,s6)

    return s.adjust(1,1,1,2).as_markup()





def admins_key():
    s = InlineKeyboardBuilder()
    s5 = InlineKeyboardButton(text='Добавить Ссылку впн', callback_data='add_vpn')
    s6 = InlineKeyboardButton(text='Отмена', callback_data='cansel')
    s7 = InlineKeyboardButton(text='Разбанить', callback_data='unban')
    s9 = InlineKeyboardButton(text='Рассылка', callback_data='sender')




    s.add(s5,s7,s9,s6)

    return s.adjust(1,1,1,1).as_markup()


def cancel_():
    s = InlineKeyboardBuilder()
    s5 = InlineKeyboardButton(text='Отмена', callback_data='cansel')

    return s.add(s5).as_markup()

def oplata_infos():
    s = InlineKeyboardBuilder()
    s5 = InlineKeyboardButton(text='Перейти к оплате ❗️',callback_data='infos')

    return s.add(s5).as_markup()



def accept(userid,rands):
    s = InlineKeyboardBuilder()
    s5 = InlineKeyboardButton(text='Принять', callback_data=f'accept_{userid}_{rands}')
    s6 = InlineKeyboardButton(text='Отменить', callback_data=f'otmenit_{userid}_{rands}')
    s7 = InlineKeyboardButton(text='Забанить', callback_data=f'ban_{userid}_{rands}')

    s.add(s5,s6,s7)
    
    return s.adjust(2,1).as_markup()



def get_pay(userid, rands):
    s = InlineKeyboardBuilder()
    s5 = InlineKeyboardButton(text='Оплатил ☑️', callback_data=f'pay_{userid}_{rands}')

    s6 = InlineKeyboardButton(text='Отмена', callback_data='nazad')

    s.add(s5,s6)
    
    return s.adjust(1,1).as_markup()



def send_url():
    s = InlineKeyboardBuilder()
    s5 = InlineKeyboardButton(text='Инструкция для Андроид', url='https://telegra.ph/Kaif-VPN-dlya-Android-Bezopasnost-na-vysshem-urovne-08-30')
    s6 = InlineKeyboardButton(text='Инструкция для IOS', url='https://telegra.ph/Kaif-VPN-dlya-iPhone-Nastrojka-v-paru-klikov-08-30')

    return s.add(s5,s6).as_markup()
