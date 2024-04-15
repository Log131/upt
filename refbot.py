from aiogram import Dispatcher,Bot,executor,types

import aiosqlite

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


token = '6706064870:AAEUUK9NXP4PZyi3_urMQfDnNqsVR-zcNAM'

bot = Bot(token=token)

dp = Dispatcher(bot=bot,storage=MemoryStorage())

class sendSpam(StatesGroup):
    send_ = State()




async def fffff():
   async with aiosqlite.connect('ref.db') as tc:
      await tc.execute('CREATE TABLE IF NOT EXISTS r(user_id, links)')
 
 
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
            await tc.commit()
        await msg.answer('Нажмите кнопку «Получить ссылку», чтобы принять участие \nв реферальной системе канала @SHARDotz', reply_markup=s)

@dp.callback_query_handler(text='get')
async def linkf(css: types.CallbackQuery):
    await css.answer()
    
    async with aiosqlite.connect('ref.db') as tc:

        async with tc.execute('SELECT links FROM r WHERE user_id = ?',(css.from_user.id,)) as f:
            links = await f.fetchone()
        if links[0] == 'yes':
            
            
            
            
            
            
            
            s = await bot.create_chat_invite_link(chat_id=-1001892774322,name=css.from_user.username)
            async with aiosqlite.connect('ref.db') as tc:
                await tc.execute('UPDATE r SET links = ? WHERE user_id = ?', (s.invite_link, css.from_user.id,))
                await tc.commit()
            await css.message.answer_photo(photo='https://i.yapx.ru/XIuH6.png',caption=f'Ваша персональная ссылка: {s.invite_link} \n \n \nКАК СДЕЛАТЬ ВЫВОД:\n1. Пригласить реальных людей, которые заинтересованы в заработке\nнакрутка и вз не оплачиваются\n2. Посмотреть, когда была создана ссылка\nдата и время по мск ПЕРВОГО запроса в боте\n3. Сообщить @elijist в ЛС дату и время создания\n \nВывод от 5-ти приглашенных, ссылка просматривается раз в сутки')
        else:
            await css.message.answer_photo(photo='https://i.yapx.ru/XIuH6.png',caption=f'Ваша персональная ссылка: {links[0]} \n \n \nКАК СДЕЛАТЬ ВЫВОД:\n1. Пригласить реальных людей, которые заинтересованы в заработке\nнакрутка и вз не оплачиваются\n2. Посмотреть, когда была создана ссылка\nдата и время по мск ПЕРВОГО запроса в боте\n3. Сообщить @elijist в ЛС дату и время создания\n \nВывод от 5-ти приглашенных, ссылка просматривается раз в сутки')


@dp.message_handler(commands=['r'], state=None)
async def spams(msg: types.Message, state: FSMContext):
    if msg.from_user.id == 686674950 or msg.from_user.id == 5954314568:
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