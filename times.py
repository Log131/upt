import schedule

import datetime

from start import bot
import aiosqlite
import asyncio

import time





async def check_s():
    async with aiosqlite.connect('tet.db') as tc:
        async with tc.execute('SELECT user_id,date FROM users') as t:
            
            s = await t.fetchall()    
        for xdx in s:
            try:
                if xdx[1] is None or xdx[1] == 0:
                    pass
                else:
                    if datetime.datetime.now() >= datetime.datetime.strptime(xdx[1], '%Y-%m-%d %H:%M'):
                        try:
                            await bot.send_message(chat_id=xdx[0], text='У вас закончилась подписка')
                        except Exception as e:
                            print(e)
                        
                        
                        async with aiosqlite.connect('tet.db') as tc:
                            await tc.execute('UPDATE users SET vpn = 0, status = 0 WHERE user_id = ?', (xdx[0],))
                            await tc.commit()
            except Exception as e:
                print(e)













def funcs_5():
    s = asyncio.get_event_loop()
    s.run_until_complete(check_s())

schedule.every(600).seconds.do(funcs_5)



while True:
    schedule.run_pending()
    time.sleep(5)