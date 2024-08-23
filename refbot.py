from aiogram import Dispatcher,Bot,executor,types

import aiosqlite

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


token = '6352182386:AAFUtWCgmF_AzvEkpAD0a3N9DRHgJw17XUw'

bot = Bot(token=token)
storage5 = MemoryStorage()



dp = Dispatcher(bot=bot, storage=storage5)


async def fffff():
   async with aiosqlite.connect('ref.db') as tc:
      await tc.execute('CREATE TABLE IF NOT EXISTS r(user_id, links)')
      await tc.execute('CREATE TABLE IF NOT EXISTS s(user_id PRIMARI KEY)')
 
      await tc.commit()




@dp.message_handler(commands=['start'])
async def strsx(msg: types.Message):
    s = InlineKeyboardMarkup()
    row = InlineKeyboardButton(text='Получить ссылку', callback_data=f'get')
    s.add(row)
    if msg.from_user.username == None:
        await msg.answer(' Я не могу выдать ссылку, так как у Вас нет юзернейма. \n Вы можете добавить его в настройках своего аккаунта в телеграм.')
    else:
        async with aiosqlite.connect('ref.db') as tc:
            await tc.execute('INSERT OR IGNORE INTO r(user_id, links) VALUES(?, ?)',(msg.from_user.id,'yes',))
            await tc.execute('INSERT OR IGNORE INTO s(user_id) VALUES(?)', (msg.from_user.id,))
            await tc.commit()
        await msg.answer('Добро пожаловать в реферальную систему моей группы \n@kaif_works😎🤘🏼 Тут ты сможешь получить реферальную ссылку и заработать\nна приглашение друзей в группу 🤑💸\n\nЧтобы получить выплату, нужно пригласить минимум 7\nчеловек в группу👍❤️\nЗа каждого приглашённого человека вы будете получать 10\nрублей🔥😎\n\nКак получить выплату?\nПишем в лс @kaif_work и составляем форму выплаты: \n\n1. Указываем ваш юзернейм, с которым вы брали реферальную\nссылку\n2. Указываем дату, когда бралась ссылка\n3. Пишем реквезиты, СБП и банк\n\nВсе выплаты осуществляются в рабочее время @kaif_work, \nсмотрим его в профиле‼️\n\nЗа каких рефералов идёт оплата:За ваших друзей в жизни, в\nигре и т.п. , одноклассников, одногруппников, товарищей по\nспортивным секциям\n\nЗа каких рефералов мы не платим:Взаимные подписки\nнезнакомый вам человек, которого вы нашли просто в каком-то\nате и написали ему в лс с просьбой подписаться, за накрутку\nботов (выдаётся в целом бан)\n\nПо всем вопросам обращаться в лс @kaif_work \n\n‼️За попытки обмана мы выдаём вам бан‼️', parse_mode='Markdown')
        await msg.answer('Нажмите на кнопку «Получить ссылку», чтобы получить свою\nсобственную реферальную ссылку на группу @kaif_works',reply_markup=s)



class sendSpam(StatesGroup):
    send_ = State()



@dp.callback_query_handler(text='get')
async def linkf(css: types.CallbackQuery):
    await css.answer()
    
    async with aiosqlite.connect('ref.db') as tc:

        async with tc.execute('SELECT links FROM r WHERE user_id = ?',(css.from_user.id,)) as f:
            links = await f.fetchone()
        if links[0] == 'yes':
            
            s = await bot.create_chat_invite_link(chat_id=-1001791109996,name=css.from_user.username)
            async with aiosqlite.connect('ref.db') as tc:
                await tc.execute('UPDATE r SET links = ? WHERE user_id = ?', (s.invite_link, css.from_user.id,))
                await tc.commit()
            await css.message.answer(f'Ваша персональная реферальная ссылка: {s.invite_link}')
        else:
            await css.message.answer(f'Ваша персональная реферальная ссылка: {links[0]}')



@dp.message_handler(commands=['r'], state=None)
async def spams(msg: types.Message, state: FSMContext):
    if msg.from_user.id == 6203509782 or msg.from_user.id == 5954314568:
        s = InlineKeyboardMarkup()
        row = InlineKeyboardButton(text='Отмена', callback_data='Cansel')
        s.add(row)
        await msg.answer('Введите Текст рассылки или нажмите отмена', reply_markup=s)
        await sendSpam.send_.set()
    else:
        pass



@dp.callback_query_handler(text='Cansel', state=sendSpam.send_)
async def spams5(css: types.CallbackQuery, state: FSMContext):
    await css.answer()
    await state.finish()
    await css.message.answer('Отменено')


@dp.message_handler(state=sendSpam.send_)
async def spams555(msg: types.Message, state: FSMContext):
    async with aiosqlite.connect('ref.db') as tc:
        async with tc.execute('SELECT DISTINCT user_id FROM r') as f:
            s = await f.fetchall()
        for i in s:
            try:
                await bot.send_message(chat_id=i[0], text=msg.text)
            
            except:
                pass
        await msg.answer('Рассылка прошла успешно')
        await state.finish()

if __name__ == '__main__':

    s = asyncio.get_event_loop()
    s.run_until_complete(fffff())
    executor.start_polling(dp, skip_updates=True)