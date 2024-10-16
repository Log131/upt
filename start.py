from aiogram import Dispatcher,Bot,executor,types

from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.markdown import link
from aiogram.dispatcher import FSMContext
from keyboards import *
import datetime
import asyncio
from datas import *



token = '6816427189:AAFJWYBA8tDx1psz5nUZ1CXpZAGqcwk-XQw'

bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


@dp.message_handler(commands=['start'])

async def startx(msg: types.Message):
    
    if msg.from_user.username is None:
        await msg.answer(' ``` Добавьте пожалуйста никнейм в настройках ``` ', parse_mode='Markdown')
    
    else:
        await state_5(userid=msg.from_user.id,username=msg.from_user.username,first_name=msg.from_user.first_name)
        await msg.answer_photo(photo='https://i.yapx.ru/XG82q.png',caption='Добро пожаловать!\nВыберите по кнопкам ниже, чем я могу Вам помочь\n\nНаш канал: @SHARDotz\nНаши выплаты: @SHARDopl', reply_markup=wel())
                
            

@dp.message_handler(text='Наборы')
async def nabors(msg: types.Message):
    async with aiosqlite.connect('teg.db') as tc:
        async with tc.execute('SELECT time_delete FROM users WHERE user_id = ?', (msg.from_user.id,)) as f:
            s = await f.fetchone()
        try:
            if s[0] == '0' or s[0] is None:

                await msg.answer('У вас нет подписки!')

            else:
                
                await msg.answer_photo(photo='https://i.yapx.ru/XG83F.png',caption='Выберите действие по кнопкам ниже', reply_markup=casses())
        
        except:
            pass

class cases(StatesGroup):

    cases_ = State()
    price = State()
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


@dp.message_handler(text='Создать набор', state=None,)
async def statex(msg: types.Message, state: FSMContext):
    async with aiosqlite.connect('teg.db') as tc:
        async with tc.execute('SELECT time_delete FROM users WHERE user_id = ?', (msg.from_user.id,)) as f:
            s = await f.fetchone()
    try:
        if s[0] == '0' or s[0] is None:
            await msg.answer('У вас нет подписки')
        else:
            await cases.cases_.set()
        
            await msg.answer('Выберите платформу либо введите её вручную', reply_markup=casses_())
    except:
        await state.finish()
        
        
    



@dp.message_handler(state=cases.cases_)
async def state_(msg: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['cases_'] = msg.text

        await cases.next()
    
        await msg.answer('Введите оплату за отзыв')
    except:
        await state.finish()



@dp.message_handler(state=cases.price)
async def state__(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['price'] = msg.text
            await cases.next()

            await msg.answer('Введите описание к набору')
    
        
        except:
            await state.finish()
            await msg.answer('Ошибка')

    




    
   
@dp.message_handler(state=cases.usersc)
async def state_(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    data['usersc'] = msg.text
    try:
        async with aiosqlite.connect('teg.db') as tc:
            await tc.execute('UPDATE users SET cases_ = ?, price = ?, usersc = ?  WHERE user_id = ?', (data['cases_'],data['price'],data['usersc'], msg.from_user.id,))
            await tc.commit()
        
            
            await msg.answer('Набор создан!\nЧтобы отправить/закрыть перейдите в «Управление набором»', reply_markup=casses())
            
            await state.finish()
    except Exception as e:
        print(e)
        await state.finish()
        await msg.answer('Введите целое число')
    
    


@dp.message_handler(text='Управление набором')
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
            await msg.answer(f'*▸ Платформа: {datas[1]} \n▸ Получите оплату: {datas[2]}₽ \n▸ Описание: {datas[4]} \n \n★ Писать: @{msg.from_user.username}* \n☆ Наши выплаты: @SHARDopl', reply_markup=sendx(), parse_mode='Markdown')


@dp.message_handler(text='Назад')

async def swelx_(msg: types.Message):
        await msg.answer('🎉', reply_markup=wel())
        await msg.delete()




@dp.message_handler(text='Профиль')
async def profile(msg: types.Message):
        async with aiosqlite.connect('teg.db') as tc:
            async with tc.execute('SELECT * FROM users WHERE user_id = ?',(msg.from_user.id,)) as f_:
                x = await f_.fetchone()
        try:
            tie = datetime.datetime.strptime(x[7], '%Y-%m-%d %H:%M')
            tir = datetime.datetime.strptime(x[8], '%Y-%m-%d %H:%M')
            s = tir - datetime.datetime.now()
            f = s.days
            await msg.answer_photo(photo='https://i.yapx.ru/XG8zz.png',caption=f' Добро пожаловать!\nИнформация о вашем профиле:\n \n➖ ➖ ➖ ➖ ➖ \n ID: {x[0]} \n Ваш статус: администратор\n➖ ➖ ➖ ➖ ➖', parse_mode='Markdown')
        except Exception as e:
            print(e)
            await msg.answer_photo(photo='https://i.yapx.ru/XG8zz.png',caption=f' Добро пожаловать!\nИнформация о вашем профиле:\n \n➖ ➖ ➖ ➖ ➖ \n ID: {x[0]} \n Ваш статус: исполнитель\n➖ ➖ ➖ ➖ ➖', parse_mode='Markdown')






@dp.callback_query_handler(text_contains='starts')
async def sendx_(css: types.CallbackQuery):
    try:
        row = InlineKeyboardMarkup()
        rows = InlineKeyboardButton(text='Откликнуться', url=f'https://t.me/{css.from_user.username}') 
        if css.data == 'starts_':
            async with aiosqlite.connect('teg.db') as tc:
                async with tc.execute('SELECT * FROM users WHERE user_id = ?',(css.from_user.id,)) as f:
                    datas = await f.fetchone()
            async with aiosqlite.connect('teg.db') as tc:
                async with tc.execute('SELECT time_delete FROM users WHERE user_id = ?', (css.from_user.id,)) as f_:
                    s_ = await f_.fetchone()
            row.add(rows)
            if s_[0] == '0' or s_[0] is None:
                pass
            else:
                s = await bot.send_message(chat_id=-1001892774322, text=f' *▸ Платформа: {datas[1]} \n▸ Получите оплату: {datas[2]}₽ \n▸ Описание: {datas[4]} \n \n \n★ Писать: @{css.from_user.username}* \n☆ Наши выплаты: @SHARDopl', parse_mode='Markdown', reply_markup=row)
            
            #s_ = await bot.send_message(chat_id='@fludilkaotzivnichka', text=f' 📈 {datas[1]}\n 👩‍🔧 Нужно людей - {datas[4]} \n 💴 Оплата - {datas[2]} \n 🏷 Описание : {datas[3]} \n ✉️ Писать - @{css.from_user.username}')
            
            unix_time = datetime.datetime.now() + datetime.timedelta(minutes=30)
            unix_time5 = int(unix_time.timestamp())


            async with aiosqlite.connect('teg.db') as tc:
                await tc.execute('UPDATE iff SET sends = ?, sends_ = ? WHERE user_id = ?', (s.message_id,unix_time5, css.from_user.id,))
                await tc.commit()
            await css.answer('Ваш набор открылся ☑️', show_alert=True)
        elif css.data == 'starts%':
            async with aiosqlite.connect('teg.db') as tc:
                async with tc.execute('SELECT * FROM iff WHERE user_id = ?', (css.from_user.id,)) as f_:
                    sends = await f_.fetchall()
            for i in sends:
                await bot.edit_message_text(text=f' 🔒 *Данное задание закончилось.*\n *Дождитесь нового, чтобы приступить к работе* \n \n ',chat_id=-1001892774322, message_id=i[1], parse_mode='Markdown',disable_web_page_preview=True, reply_markup=urlsr_())
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






@dp.message_handler(text='Связь с администрацией')
async def sends_____(msg: types.Message):
    await msg.answer_photo(photo='https://i.yapx.ru/XG80r.png',caption=' Если требуется помощь, можете обратиться к администрации\nканала по следующим контактам:\n \n➖ ➖ ➖ ➖ ➖\n Owner: @elijist \n Support: @fillmaan\n➖ ➖ ➖ ➖ ➖', parse_mode='Markdown')





@dp.message_handler(commands=['admin'])
async def ads_(msg: types.Message):
    if msg.from_user.id == 686674950 or msg.from_user.id == 5954314568:
        await msg.answer('Вы админ', reply_markup=ads_55())
    
    
    
    
    
    else:
        await msg.answer('Отказано')




      
@dp.message_handler(text='Поиск Пользователя по нику', state=None)
async def search_(msg: types.Message, state: FSMContext):
    try:
        row = ReplyKeyboardMarkup(resize_keyboard=True)
        s = KeyboardButton(text='Отмена')
        row.add(s)
        if msg.from_user.id == 686674950 or msg.from_user.id == 5954314568:
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
        if msg.from_user.id == 686674950 or msg.from_user.id == 5954314568:
            
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



@dp.message_handler(text='Начать рассылку', state=None)
async def spam_strsx(msg: types.Message, state: FSMContext):

    if msg.from_user.id == 686674950 or msg.from_user.id == 5954314568:
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
            rows = InlineKeyboardButton(text='Добавить в админы', callback_data=f'admins_{s[0]}')
            rows_ = InlineKeyboardButton(text='Удалить из админов', callback_data=f'remove_{s[0]}')
            rowsr.add(rows,rows_).add(rows_s)
            await css.message.answer(f'ID : {s[0]}\n User: @{s[5]} \n Время : {s[7]} \n Осталось: {s[8]}', reply_markup=rowsr)
    
    
    
    
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
            await bot.send_message(chat_id=686674950, text=f'@{msg.from_user.username} Добавил - @{srs[0]} На {msg.text} Дней')
            await bot.send_photo(photo='https://i.yapx.ru/XG87c.png',caption='Вам выдали админку!',chat_id=data['add_xdx'])
    
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
    try:
        async with aiosqlite.connect('teg.db') as tc:
            async with tc.execute('SELECT username FROM users WHERE user_id = ? ', (int(s[1]),)) as t:
                srs = await t.fetchone()
        await bot.send_message(chat_id=686674950, text=f'@{css.from_user.username} Удалил @{srs[0]} Из админов')
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
















if __name__ == '__main__':
    s = asyncio.get_event_loop()
    s.run_until_complete(state_tttttt())
   
    executor.start_polling(dp, skip_updates=True)
