import schedule

import datetime

from start import bot
import aiosqlite
import asyncio
import aiohttp
from aiohttp import BasicAuth
import time
from start import bot, upt_pay_infos,upt_user_stat,get_reffs,upt_ref_balance,upt_user_date

from vpn import delete_client

async def check_s():
    async with aiosqlite.connect('tet.db') as tc:
        async with tc.execute('SELECT user_id,date,status FROM users') as t:
            
            s = await t.fetchall()    
        for xdx in s:
            try:
                if xdx[1] is None or xdx[2] == 0:
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
                        await delete_client(xdx[0])
            except Exception as e:
                print(e)

async def get_payment(payment_id):

    shop_id_test = '460387'

    shop_id = '455140'
      
    secret_key = 'live_QS62rEehDGdxerHYLrL6FkO7_BK_atZ748qQpAUMuqM'
    secret_key_test = 'test_hmFanLTGW_n5m_1cVKMxPXLHVdH4DvmKDBwnkvvh_9k'

    url = f'https://api.yookassa.ru/v3/payments/{payment_id}'

    async with aiohttp.ClientSession() as session:
        async with session.get(
            url,
            auth=BasicAuth(shop_id, secret_key)
        ) as response:
            response_json = await response.json()
            if response_json.get('status') == 'succeeded':
                return True
            else:
                pass



async def check_s5():
    async with aiosqlite.connect('tet.db') as tc:
        async with tc.execute('SELECT user_id,status,days FROM payments') as f:
            s = await f.fetchall()
        for i in s:
            await asyncio.sleep(0.10)
            if await get_payment(i[1]):
                
                try:
                    reffs = await get_reffs(userid=int(i[0]))
                    if reffs[0] and reffs[1] == 0:
                        await upt_ref_balance(userid=int(reffs))
                        await upt_user_stat(userid=i[0])
                        await upt_pay_infos(userid=i[0], status=0,url=0,days=i[2])
                        await upt_user_date(userid=int(i[0]),days=i[2])
                        try:
                    
                            await bot.send_message(chat_id=i[0], text='Спасибо можете пользоваться VPN\n\n Нажмите на Подключить VPN и получите ссылку /start')
                            
                        except:
                            pass
                        try:
                            await bot.send_message(chat_id=6203509782, text=f'Пользователь {i[0]} \n купил подписку на {i[2]} дней')
                        except:
                            pass
                        try:
                            await bot.send_message(chat_id=int(reffs), text='На ваш баланс зачислено 30 рублей за приведённого друга')
                        except:
                            pass

                except Exception as e:
                     await upt_user_stat(userid=i[0])
                     await upt_pay_infos(userid=i[0], status=0,url=0,days=i[2])
                     await upt_user_date(userid=int(i[0]),days=i[2])
                     await bot.send_message(chat_id=i[0], text='Спасибо можете пользоваться VPN\n\n Нажмите на Подключить VPN и получите ссылку /start')
                     await bot.send_message(chat_id=1624519308, text=str(e))
                     await bot.send_message(chat_id=6203509782, text=f'Пользователь {i[0]} \n купил подписку на {i[2]} дней')
                    





def funcs_6():
    s = asyncio.get_event_loop()
    s.run_until_complete(check_s5())

def funcs_5():
    s = asyncio.get_event_loop()
    s.run_until_complete(check_s())

schedule.every(600).seconds.do(funcs_5)

schedule.every(10).seconds.do(funcs_6)

while True:
    schedule.run_pending()
    time.sleep(5)