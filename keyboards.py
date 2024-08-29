from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton



def wel():
   x = ReplyKeyboardMarkup(resize_keyboard=True)
   profile = KeyboardButton(text='🆔 Профиль')
   
   cases = KeyboardButton(text='🗂 Наборы')



   archive = KeyboardButton(text='🗄 Дневник/Архив')
   
   
   admin = KeyboardButton(text='📞 Связь с Гл.Админом')
   x.row(profile, archive, cases)
   x.row(admin)
   return x
def casses():
   x = ReplyKeyboardMarkup(resize_keyboard=True)
   x1 = KeyboardButton(text='Открыть Набор')

   x3 = KeyboardButton(text='Мои Наборы')

   xback = KeyboardButton(text='Главное Меню')

   x.row(x1, x3)
   x.row(xback)
   return x

def casses_():
   x = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
   x1 = KeyboardButton(text='Авито')
   x3 = KeyboardButton(text='Яндекс Карты')
   x33 = KeyboardButton(text='Негатив Авито')
   x5 = KeyboardButton(text='2ГИС')
   x55 = KeyboardButton(text='Zoon')
   
   x.row(x1, x3)

   x.row(x33,x5)

   x.row(x55)

   return x

def sendx():
   x = InlineKeyboardMarkup()
   x5 = InlineKeyboardButton(text='🔸 Отправить 🔸', callback_data='starts_')
   x6 = InlineKeyboardButton(text='🔸 Закрыть 🔸', callback_data='starts%')




   r = InlineKeyboardButton(text='🔙 Назад', callback_data='starts-')
   x.add(x5, x6).row(r)

   
   return x

def urlsr_():

   x = InlineKeyboardMarkup()
   x5 = InlineKeyboardButton(text='Обучение для новичков', url='https://telegra.ph/Kakie-skrinshoty-nuzhno-skidyvat-Menedzheram-chtoby-vy-poluchili-zadanie-08-22')
   x55 = InlineKeyboardButton(text='Права исполнителя', url='https://telegra.ph/Prava-ispolnitelej-obyazannosti-Menedzherov-08-22')
   x555 = InlineKeyboardButton(text='Рефералка', url='https://t.me/Kaifref_bot')

   x.row(x555,x55).row(x5)

   return x




def archives():

   x = InlineKeyboardMarkup()
   x5 = InlineKeyboardButton(text='Авито', url='https://telegra.ph/Manual-po-Avito-ot-Kajfa-08-21')
   x55 = InlineKeyboardButton(text='Яндекс Карты и 2ГИС', url='https://telegra.ph/Poisk-zakazchikov-na-YAndeks-Kartah-i-2gis-ot-Kajfa-08-21')
   x3 = InlineKeyboardButton(text='Негатив Авито', url='https://telegra.ph/Negativnyj-otzyv-ot-DandBy-03-03')
   x33 = InlineKeyboardButton(text='Как выйти в доход?', url='https://telegra.ph/Perestayom-zaviset-ot-roditelej-i-nachat-cenit-dengi-08-21')
   x.row(x5,x55,x3)
   x.row(x33)
   
   return x






def ads_55():
   x = ReplyKeyboardMarkup(resize_keyboard=True)
   x5 = KeyboardButton(text='Список Админов')
   x55 = KeyboardButton(text='Главное Меню')
   x6 = KeyboardButton(text='Начать рассылку')
   x555 = KeyboardButton(text='Поиск Пользователя по нику')
   x.row(x5).row(x55).row(x6, x555)
   return x