from aiogram import Dispatcher,Bot,executor,types

from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.dispatcher import FSMContext
from keyboards import *
import datetime
import asyncio
from datas import *



token = '6021836757:AAFu1PVkjrjcG1R4sfQTBv79A8pYQQb-08Q'

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


@dp.message_handler(commands=['start'])

async def startx(msg: types.Message):
    
    if msg.from_user.username is None:
        await msg.answer(' ``` Добавьте пожалуйста никнейм в настройках ``` ', parse_mode='Markdown')
    
    else:
        await state_5(userid=msg.from_user.id,username=msg.from_user.username,first_name=msg.from_user.first_name)
        await msg.answer('Добро пожаловать', reply_markup=wel())
                
            

@dp.message_handler(text='🗂 Наборы')
async def nabors(msg: types.Message):
    async with aiosqlite.connect('teg.db') as tc:
        async with tc.execute('SELECT time_delete FROM users WHERE user_id = ?', (msg.from_user.id,)) as f:
            s = await f.fetchone()
        try:
            if s[0] == '0' or s[0] is None:

                await msg.answer('У вас нет подписки!')

            else:
                
                await msg.answer('Выберите Действие с наборами!', reply_markup=casses())
        
        except:
            pass

class cases(StatesGroup):

    cases_ = State()
    price = State()
    zametka = State()
    usersc = State()

class adminadd(StatesGroup):
    add_xdx = State()
    
    timex_ = State()

class get_spam(StatesGroup):
    spam_start = State()
class del_admins(StatesGroup):
    del_ads = State()

class searches_(StatesGroup):
    search_start = State()




def datetime_end():
    date_ = datetime.datetime.now()
    start_ = datetime.datetime.strptime('8:00', '%H:%M').time()
    end_ = datetime.datetime.strptime('22:00', '%H:%M').time()

    return start_ <= date_.time() <= end_

@dp.message_handler(text='Открыть Набор', state=None,)
async def statex(msg: types.Message, state: FSMContext):
    if datetime_end():
        async with aiosqlite.connect('teg.db') as tc:
            async with tc.execute('SELECT time_delete FROM users WHERE user_id = ?', (msg.from_user.id,)) as f:
                s = await f.fetchone()
        try:
            if s[0] == '0' or s[0] is None:
                await msg.answer('У вас нет подписки')
            else:
                await cases.cases_.set()
        
                await msg.answer('Для Открытия набора выберите следующие данные:\n 1. Выберите тип', reply_markup=casses_())
        except:
            await state.finish()
    else:
        await msg.answer('Время наборов с 8:00 до 22:00 по МСК, не забывай 😊')
        
        
    



@dp.message_handler(state=cases.cases_)
async def state_(msg: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['cases_'] = msg.text

        await cases.next()
    
        await msg.answer('Введите сумму оплаты за отзыв')
    except:
        await state.finish()



@dp.message_handler(state=cases.price)
async def state__(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['price'] = msg.text
            await cases.next()

            await msg.answer('Введите заметку для вашего набора. Она будет отображаться в комментарий к набору')
    
        
        except:
            await state.finish()
            await msg.answer('напишите целое число')

    
@dp.message_handler(state=cases.zametka)
async def stated(msg: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            
            data['zametka'] = msg.text
    
    
    
    
    
        await msg.answer('Сколько человек нужно')
        await cases.next()
    except:

        await state.finish()
        await msg.answer('Попробуйте заного')
    
   
@dp.message_handler(state=cases.usersc)
async def state_(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    data['usersc'] = msg.text
    try:
        async with aiosqlite.connect('teg.db') as tc:
            await tc.execute('UPDATE users SET cases_ = ?, price = ?, zametka = ?, usersc = ?  WHERE user_id = ?', (data['cases_'],data['price'],data['zametka'],data['usersc'], msg.from_user.id,))
            await tc.commit()
        
            
            await msg.answer('Готово нажмите мои наборы', reply_markup=casses())
            
            await state.finish()
    except:
        await state.finish()
        await msg.answer('Введите целое число')
    
    


@dp.message_handler(text='Мои Наборы')
async def check_cases(msg: types.Message):
    
    async with aiosqlite.connect('teg.db') as tc:
        async with tc.execute('SELECT * FROM users WHERE user_id = ?',(msg.from_user.id,)) as f:
            datas = await f.fetchone()
        async with tc.execute('SELECT time_delete FROM users WHERE user_id = ?', (msg.from_user.id,)) as f_:
            s = await f_.fetchone()
    if s[0] == '0' or s[0] is None:
        await msg.answer('У вас нет подписки')
    else:
        if datas[0] == '0':
            await msg.answer('У вас еще нет наборов что бы открыть набор нажмитe Открыть набор', reply_markup=casses())
        else:
            await msg.answer(f' 📈  {datas[1]}\n 👩‍🔧 Нужно людей - {datas[4]} \n 💴 Оплата - {datas[2]} \n 🏷 Описание : {datas[3]} \n ✉️ Писать - @{msg.from_user.username}', reply_markup=sendx())


@dp.message_handler(text='Главное Меню')

async def swelx_(msg: types.Message):
        await msg.answer('🎉', reply_markup=wel())
        await msg.delete()




@dp.message_handler(text='🆔 Профиль')
async def profile(msg: types.Message):
        async with aiosqlite.connect('teg.db') as tc:
            async with tc.execute('SELECT * FROM users WHERE user_id = ?',(msg.from_user.id,)) as f_:
                x = await f_.fetchone()
        try:
            tie = datetime.datetime.strptime(x[7], '%Y-%m-%d %H:%M')
            tir = datetime.datetime.strptime(x[8], '%Y-%m-%d %H:%M')
            s = tir - datetime.datetime.now()
            f = s.days
            await msg.answer(f' Ваш профиль: \n ➖ ➖ ➖ ➖ ➖ \n 🆔 : {x[0]} \n ➖ ➖ ➖ ➖ ➖ \n 🕰 Рецистрация Админки: {x[7]} \n ➖ ➖ ➖ ➖ ➖ \n ❗️ До конца Админки : ` {abs(f)} Дней ` ', parse_mode='Markdown')
        except Exception as e:
            print(e)
            await msg.answer(f' Ваш профиль: \n ➖ ➖ ➖ ➖ ➖ \n 🆔 : {x[0]} \n ➖ ➖ ➖ ➖ ➖ \n Админка : ` Недоступно ` ', parse_mode='Markdown')








@dp.callback_query_handler(text_contains='starts')
async def sendx_(css: types.CallbackQuery):
    if datetime_end():
        try:
            row = InlineKeyboardMarkup()
            rows = InlineKeyboardButton(text='📝 Откликнуться', url=f'https://t.me/{css.from_user.username}') 
            if css.data == 'starts_':
                async with aiosqlite.connect('teg.db') as tc:
                    async with tc.execute('SELECT * FROM users WHERE user_id = ?',(css.from_user.id,)) as f:
                        datas = await f.fetchone()
                row.add(rows)
                if datas[8] == '0' or datas[8] == None  or datas[8] is None:
            
                    await css.message.delete()
                else:
                    s = await bot.send_message(chat_id=-1001791109996, text=f' * 📈 {datas[1]}\n 👩‍🔧 Нужно людей - {datas[4]} \n 💴 Оплата - {datas[2]} \n 🏷 Описание : {datas[3]} \n ✉️ Писать - @{css.from_user.username}*', parse_mode='Markdown', reply_markup=row)
            
                
                #s_ = await bot.send_message(chat_id='@fludilkaotzivnichka', text=f' 📈 {datas[1]}\n 👩‍🔧 Нужно людей - {datas[4]} \n 💴 Оплата - {datas[2]} \n 🏷 Описание : {datas[3]} \n ✉️ Писать - @{css.from_user.username}')
            
                async with aiosqlite.connect('teg.db') as tc:
                    await tc.execute('UPDATE iff SET sends = ? WHERE user_id = ?', (s.message_id, css.from_user.id,))
                    await tc.commit()
                await css.answer('Ваш набор открылся ☑️', show_alert=True)
            elif css.data == 'starts%':
                async with aiosqlite.connect('teg.db') as tc:
                    async with tc.execute('SELECT * FROM iff WHERE user_id = ?', (css.from_user.id,)) as f_:
                        sends = await f_.fetchall()
                for i in sends:
                    await bot.edit_message_text(text=f'🔒 Набор закрыт, ожидайте следующие задания ❗️',chat_id=-1001791109996, message_id=i[1], reply_markup=urlsr_())
                    #await bot.delete_message(chat_id='@fludilkaotzivnichka', message_id=i[2])
                async with aiosqlite.connect('teg.db') as tc:
                    await tc.execute('UPDATE users SET cases_ = ?, price = ?, zametka = ?, usersc = ? WHERE user_id = ?',(None, None, None, None, css.from_user.id,))
                    await tc.commit()
                await css.answer('Удалено')
                    #await bot.send_message(chat_id=-1001791109996, text=f'🔒 Набор от @{css.from_user.username} Был закрыт!')
            elif css.data == 'starts-':
                await bot.send_message(css.from_user.id, text='Главное Меню', reply_markup=wel())
        except Exception as e:
            print(e)
            pass
    else:
        await css.message.answer('Время наборов с 8:00 до 22:00 по МСК, не забывай 😊')




@dp.message_handler(text='🗄 Дневник/Архив')
async def sends___(msg: types.Message):
    async with aiosqlite.connect('teg.db') as tc:
        async with tc.execute('SELECT time_delete FROM users WHERE user_id =?', (msg.from_user.id,)) as f:
            s = await f.fetchone()
    if s[0] == '0' or s[0] is None:
        await msg.answer('У вас нет подписки')
    else:
        await msg.answer('Тут Мануалы :',reply_markup=archives())


@dp.message_handler(text='📞 Связь с Гл.Админом')
async def sends_____(msg: types.Message):
    await msg.answer('📞 - @kaif_work')





@dp.message_handler(commands=['admin'])
async def ads_(msg: types.Message):
   
    chat_admins = await bot.get_chat_member(chat_id='@OwnerOtziv', user_id=msg.from_user.id)
    if chat_admins.status == 'creator' or chat_admins.status == 'administrator':
        await msg.answer('Вы админ Комманды для чата модераторов - /del обнулить счетчик предупреждений - /war выдать предупреждение', reply_markup=ads_55())
    
    
    
    
    
    else:
        await msg.answer('Отказано')




      
@dp.message_handler(text='Поиск Пользователя по нику', state=None)
async def search_(msg: types.Message, state: FSMContext):
    try:
        row = ReplyKeyboardMarkup(resize_keyboard=True)
        s = KeyboardButton(text='Отмена')
        row.add(s)
        chat_admins = await bot.get_chat_member(chat_id='@OwnerOtziv', user_id=msg.from_user.id)
        if chat_admins.status == 'creator' or chat_admins.status == 'administrator':
            await msg.answer('Введите ник Пользователя без @', reply_markup=row)
            await searches_.search_start.set()
    except Exception as e:
        pass

@dp.message_handler(state=searches_.search_start)
async def state_search(msg: types.Message, state: FSMContext):
    try:
        row = InlineKeyboardMarkup()
        if msg.text == 'Отмена':
            await msg.answer('Отменено!', reply_markup=ads_55())
            await state.finish()
        else:
            async with aiosqlite.connect('teg.db') as tc:
                async with tc.execute('SELECT username FROM users WHERE username = ?', (msg.text,)) as t:
                    x = await t.fetchone()
                async with tc.execute('SELECT * from users WHERE username = ?', (x[0],)) as t_:
                    s = await t_.fetchone()
            rows = InlineKeyboardButton(text='Добавить админа', callback_data=f'admins_{s[0]}')
            rows_ = InlineKeyboardButton(text='удалить из админов', callback_data=f'remove_{s[0]}')
            row.add(rows, rows_)
            await msg.answer(f'ID : {s[0]}\n nickname : @{s[5]} \n firstname: {s[6]} \n Время : {s[7]} \n Осталось: {s[8]}', reply_markup=row)
            await msg.answer('Главное меню', reply_markup=ads_55())
            await state.finish()
    except Exception as e:
        await msg.answer('Такого нет')
        await state.finish()
        print(e)




@dp.message_handler(text='Список Админов')
async def admins_(msg: types.Message):
    try:
        row = InlineKeyboardMarkup()
        chat_admins = await bot.get_chat_member(chat_id='@OwnerOtziv', user_id=msg.from_user.id)
        if chat_admins.status == 'creator' or chat_admins.status == 'administrator':
            async with aiosqlite.connect('teg.db') as tc:
                async with tc.execute('SELECT * FROM users') as t:
                    x = await t.fetchall()
            for s in x:
                rows = InlineKeyboardButton(text=f'@{s[5]} - {s[8]}', callback_data=f'add_@{s[0]}')
                    
                    
                row.add(rows)
            await msg.answer('Список админов', reply_markup=row)
        else:
            pass
    except:
        pass




@dp.callback_query_handler(text_contains='trr')
async def state_r_0(css: types.CallbackQuery):
    s = css.data.split('_')
    await css.answer()
    await css.message.delete()
    try:
        async with aiosqlite.connect('teg.db') as tc:
            async with tc.execute('SELECT time_delete FROM users WHERE user_id = ?', (int(s[1]),)) as f:
                s_ = await f.fetchone()
                time_now = (datetime.datetime.strptime(s_[0], '%Y-%m-%d %H:%M') - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M')
        async with aiosqlite.connect('teg.db') as tc:
            await tc.execute('UPDATE users SET time_delete = ? WHERE user_id = ?', (time_now, int(s[1])))
            await tc.commit()
        await css.message.answer('Успешно изменено')
    except Exception as e:
        print(e)
        await css.message.answer('Произошла ошибка')




@dp.callback_query_handler(text_contains='srr')
async def state_s_0(css: types.CallbackQuery):
    s = css.data.split('_')
    await css.answer()
    await css.message.delete()
    try:
        async with aiosqlite.connect('teg.db') as tc:
            async with tc.execute('SELECT time_delete FROM users WHERE user_id = ?', (int(s[1]),)) as f:
                s_ = await f.fetchone()
                time_now = (datetime.datetime.strptime(s_[0], '%Y-%m-%d %H:%M') + datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M')
        async with aiosqlite.connect('teg.db') as tc:
            await tc.execute('UPDATE users SET time_delete = ? WHERE user_id = ?', (time_now, int(s[1]),))
            await tc.commit()
        await css.message.answer('Успешно изменено')
    except Exception as e:
        print(e)
        await css.message.answer('Произошла ошибка')



@dp.message_handler(text='Начать рассылку', state=None)
async def spam_strsx(msg: types.Message, state: FSMContext):

    chat_admins = await bot.get_chat_member(chat_id='@OwnerOtziv', user_id=msg.from_user.id)
    if chat_admins.status == 'creator' or chat_admins.status == 'administrator':
        x = ReplyKeyboardMarkup(resize_keyboard=True)
        x_0 = KeyboardButton(text='Отмена')
        x.add(x_0)
        await msg.answer('Начинаем рассылку введите текст рассылки', reply_markup=x)
        await get_spam.spam_start.set()



@dp.message_handler(state=get_spam.spam_start)
async def stam_it(msg: types.Message, state: FSMContext):
    try:
        if msg.text == 'Отмена':
            await msg.answer('Отменено', reply_markup=ads_55())
            await state.finish()
        else:
            async with aiosqlite.connect('teg.db') as tc:
                async with tc.execute('SELECT user_id FROM users') as t:
                    s = await t.fetchall()
            for sends in s:
                try:
                    await bot.send_message(chat_id=sends[0], text=msg.text)
                except Exception as e:
                    print(e)
            await msg.answer('Рассылено', reply_markup=ads_55())
            await state.finish()
    except Exception as e:
        print(e)



@dp.callback_query_handler(text_contains='add_@')
async def add_ads_(css: types.CallbackQuery):

    
    rowsr = InlineKeyboardMarkup()
    rows_s = InlineKeyboardButton(text='Отмена', callback_data='otmena')
    try: 
        async with aiosqlite.connect('teg.db') as tc:
            async with tc.execute('SELECT * FROM users WHERE user_id = ?', (int(css.data[5:]),)) as t:
                v = await t.fetchall()
        for s in v:
            rows_0 = InlineKeyboardButton(text='- День админки', callback_data=f'trr_{s[0]}')
            rows_5 = InlineKeyboardButton(text='+ День админки', callback_data=f'srr_{s[0]}')
            rows = InlineKeyboardButton(text='Добавить в админы', callback_data=f'admins_{s[0]}')
            rows_ = InlineKeyboardButton(text='Удалить из админов', callback_data=f'remove_{s[0]}')
            rowsr.add(rows,rows_).add(rows_s).add(rows_0,rows_5)
            await css.message.answer(f'ID : {s[0]}\n nickname : @{s[5]} \n firstname: {s[6]} \n Время : {s[7]} \n Осталось: {s[8]}', reply_markup=rowsr)
    
    
    
    
    except:
        pass









@dp.callback_query_handler(text='otmena')
async def adsadsa(css: types.CallbackQuery):
    
    await css.message.delete()





@dp.callback_query_handler(text_contains='admins_', state=None)
async def state_ads_(css: types.CallbackQuery, state: FSMContext):
    
    try:
        async with state.proxy() as data:
            data['add_xdx'] = int(css.data[7:])
    
    
    
    
        s = InlineKeyboardMarkup()
        s_ = InlineKeyboardButton(text='Отмена', callback_data='stop')
        s.add(s_)
        await css.message.answer('Напишите время админки (Дни)', reply_markup=s) 


    
        await adminadd.add_xdx.set()
    except:

        await css.message.answer('Введите число или отмена')







@dp.message_handler(state=adminadd.add_xdx)
async def state_ads______(msg: types.Message, state: FSMContext):
    
    
    
    try:
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

        time_delete = (datetime.datetime.now() + datetime.timedelta(days=int(msg.text))).strftime('%Y-%m-%d %H:%M')
        
        async with state.proxy() as data:
            async with aiosqlite.connect('teg.db') as tc:
                async with tc.execute('SELECT * FROM users WHERE user_id = ?', (data['add_xdx'],)) as t:
                    s = await t.fetchall()
            for i in s:
                async with aiosqlite.connect('teg.db') as tc:
                    await tc.execute('UPDATE rat SET username = ?, username_admin = ?, time_now = ?, time_delete = ? WHERE user_id = ?', (i[5], msg.from_user.username,time_now, time_delete, data['add_xdx'],))
                    
                    await tc.execute('UPDATE users SET time_now = ?, time_delete = ? WHERE user_id = ?', (time_now, time_delete, data['add_xdx'],))
                    
                    await tc.commit()
                
                await msg.answer('Добавлено!')
                await state.finish()
            async with aiosqlite.connect('teg.db') as tc:
                async with tc.execute('SELECT username FROM users WHERE user_id = ?', (data['add_xdx'],)) as t:
                    srs = await t.fetchone()
            await bot.send_message(chat_id=6203509782, text=f'@{msg.from_user.username} Добавил - @{srs[0]} На {msg.text} Дней')
            await bot.send_photo(chat_id=data['add_xdx'], photo='https://i.yapx.ru/V8QOQ.png', caption='Вам выдали админку 🔥🔥🔥')
    
    except Exception as e:
        print(e)
        await state.finish()
        await msg.answer('Введите число')



@dp.callback_query_handler(state=adminadd.add_xdx)
async def state_adsrs(css: types.CallbackQuery, state: FSMContext):
    if css.data == 'stop':
        await state.finish()
        await css.message.answer('Отменено', reply_markup=ads_55())




@dp.callback_query_handler(text_contains='remove_')
async def remove_it(css: types.CallbackQuery):
    s = css.data.split('_')
    print(s)
    try:
        async with aiosqlite.connect('teg.db') as tc:
            async with tc.execute('SELECT username FROM users WHERE user_id = ? ', (int(s[1]),)) as t:
                srs = await t.fetchone()
        await bot.send_message(chat_id=6203509782, text=f'@{css.from_user.username} Удалил @{srs[0]} Из админов')
        async with aiosqlite.connect('teg.db') as tc:
                await tc.execute('DELETE FROM users WHERE user_id = ?', (int(s[1]),))
                await tc.commit()
        try:
            await bot.send_message(chat_id=int(s[1]), text='Ваша подписка закончилась /start перезапустите бота')
        except Exception as e:
            print(e)
    

        await css.message.answer('Удален')
        
    except Exception as e:
        print(e)
        await css.message.answer('Чтото пошло не так')







@dp.message_handler(commands=['rat'])
async def rat_(msg: types.Message):

    try:
        chat_member = await bot.get_chat_member(chat_id='@OwnerOtziv', user_id=msg.from_user.id)
        if chat_member.status == 'creator':
            async with aiosqlite.connect('teg.db') as tc:
                async with tc.execute('SELECT * FROM rat') as t:
                    s = await t.fetchall()
            for i in s:
                time_ = datetime.datetime.strptime(i[4], '%Y-%m-%d %H:%M')
                f = time_ - datetime.datetime.now()
                fffff = f.days
                await msg.answer(f'Админ - @{i[2]} добавил - @{i[1]} \n Добавил в - {i[3]} \n Выдал на - {abs(fffff) + 1} дней')
        else:
            await msg.answer('Отказано')

    except Exception as e:
        print(e)









if __name__ == '__main__':
    s = asyncio.get_event_loop()
    s.run_until_complete(state_tttttt())
   
    executor.start_polling(dp, skip_updates=True)
