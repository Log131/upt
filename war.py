from aiogram import Dispatcher,Bot,executor,types

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

import asyncio
from datetime import datetime, time
import sqlite3







token = '5984947658:AAFEJNgy0rXV8FxfVRsV7uvcgS8Co1Mi24w'
#token = '6093970106:AAFugNzYa1SL0WTgReF4gHznIwqAF6tSRSY'
bot_5 = Bot(token=token)
dp = Dispatcher(bot=bot_5)

tbase = sqlite3.connect('tes.db')
tc = tbase.cursor()



with tbase:
    tc.execute('CREATE TABLE IF NOT EXISTS wars_(username, user_id PRIMARY KEY, war DEFAULT 0)')



@dp.message_handler(commands=['start'])
async def strsx(msg: types.Message):
    
    with tbase:
        tc.execute('INSERT OR IGNORE INTO wars_(username, user_id) VALUES(?, ?)', (msg.from_user.username, msg.from_user.id,))


    


@dp.message_handler(commands=['war'])
async def warxd_(msg: types.Message):
    try:
        
        chat_admins = await bot_5.get_chat_member(chat_id='@OwnerOtziv', user_id=msg.from_user.id)
        
        
        
        
        
        
        
        if chat_admins.status == 'creator' or chat_admins.status == 'administrator':
            with tbase:
                tc.execute('INSERT OR IGNORE INTO wars_(user_id) VALUES(?)',(msg.reply_to_message.from_user.id,))
            with tbase:
                tc.execute('UPDATE wars_ SET war = war + 1 WHERE user_id = ?',(msg.reply_to_message.from_user.id,))
            with tbase:
               s = tc.execute('SELECT war FROM wars_ WHERE user_id = ?', (msg.reply_to_message.from_user.id,)).fetchone()
            await bot_5.send_message(msg.reply_to_message.from_user.id, text=f'Вы получили предупреждение ‼️ ‼️ ‼️ {s[0]}/3')
            await bot_5.send_message(msg.chat.id, text=f'@{msg.reply_to_message.from_user.username}        Вы получили предупреждение ‼️ ‼️ ‼️{s[0]}/3')
            if s[0] >= 3:
                with tbase:
                    tc.execute('UPDATE wars_ SET war = 1 WHERE user_id = ?', (msg.reply_to_message.from_user.id,))
                await bot_5.send_photo(msg.chat.id, photo='https://i.yapx.ru/V9rL7.png',caption=f'@{msg.reply_to_message.from_user.username} Был отправлен в ЧВК Шелби 🫡')
                await bot_5.ban_chat_member(msg.chat.id, user_id=msg.reply_to_message.from_user.id)
        else:

            pass
    
    except Exception as e:
        print(e)








@dp.message_handler(commands=['card'])
async def cardxd_(msg: types.Message):
    await msg.answer('_Реквизиты Кайфа_ : \n 🏦 АльфаБанк\n💳 2200150236389786 \n \n 🏦 Сбербанк \n💳 2202206884471868 \n \n 📲 +79106265792 (Для переводов по номеру, актуальны только те банки, которые указаны выше ☝️ \n \n🤖 💳Савушкин С.В.', parse_mode='Markdown')



@dp.message_handler(commands=['del'])
async def delxd_(msg: types.Message):
    
    
    
    try:
        chat_admins = await bot_5.get_chat_member(chat_id='@OwnerOtziv', user_id=msg.from_user.id)
        if chat_admins.status == 'creator' or chat_admins.status == 'administrator':
            s = msg.reply_to_message.from_user.username
            with tbase:
                tc.execute('UPDATE wars_ SET war = war - 1 WHERE user_id = ?', (msg.reply_to_message.from_user.id,))
            with tbase:
                s_ = tc.execute('SELECT war FROM wars_ WHERE user_id = ? ',(msg.reply_to_message.from_user.id,)).fetchone()
            

            
            
            
            await bot_5.send_message(msg.chat.id, text=f'@{s} Предупреждения сняты {s_[0]}/3')
    except:
        pass




















if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
