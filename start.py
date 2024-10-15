import asyncio

from aiogram import F

from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart, Command, StateFilter, CommandObject
import aiosqlite
from keyboards import *
from vpn import *
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import random

import datetime
from payments import create_payment
from datas import *
import re
from aiogram.utils.markdown import hlink





from aiogram.types import InputFile




async def datas():
    async with aiosqlite.connect('tet.db') as tc:
        await tc.execute('CREATE TABLE IF NOT EXISTS users(user_id PRIMARY KEY,status DEFAULT 0, vpn DEFAULT 0, date)')
        await tc.execute('CREATE TABLE IF NOT EXISTS vpn(names PRIMARY KEY, lists)')
        await tc.execute('CREATE TABLE IF NOT EXISTS server(log,passw,names,sip,sinbound)')
        await tc.execute('CREATE TABLE IF NOT EXISTS ref(refid PRIMARY KEY, userid, balance DEFAULT 0)')
        await tc.execute('CREATE TABLE IF NOT EXISTS reff(refid PRIMARY KEY, userid, balance DEFAULT 0, status DEFAULT 0)')
        await tc.execute('CREATE TABLE IF NOT EXISTS payments(user_id PRIMARY KEY, status DEFAULT 0, url DEFAULT 0, days DEFAULT 0)')
        await tc.commit()
    async with aiosqlite.connect('teg.db') as tc:
        await tc.execute('CREATE TABLE IF NOT EXISTS usersw(user_id PRIMARY KEY, sip, sinbound, log, passw)')
        await tc.commit()







dp = Dispatcher()
router = Router()

bot = Bot(token='7420265405:AAEojcS8CRjT5sRqlgrqTsSdsWToUptnNzc')

dp.include_router(router=router) 

#5162602636:AAHtUb-m25lZ18_fGdomamEo9XZekfASi8c
#7420265405:AAEojcS8CRjT5sRqlgrqTsSdsWToUptnNzc



@dp.message(CommandStart())
async def start_(msg: types.Message):
    invited_ref_id = msg.text.replace('/start', '').replace(' ', '')
    if invited_ref_id and int(invited_ref_id) != msg.from_user.id:
        await insert_reffs(refid=msg.from_user.id, userid=int(invited_ref_id))
        async with aiosqlite.connect('tet.db') as tc:
            await tc.execute('INSERT OR IGNORE INTO users(user_id) VALUES(?)', (msg.from_user.id,))
            await tc.execute('INSERT OR IGNORE INTO payments(user_id) VALUES(?)', (msg.from_user.id,))
            await tc.commit()
        async with aiosqlite.connect('teg.db') as tc:
            await tc.execute('INSERT OR IGNORE INTO usersw(user_id) VALUES(?)', (msg.from_user.id,))
            await tc.commit()
        await msg.answer('Добро пожаловать', reply_markup=starts_())
    else:
        async with aiosqlite.connect('tet.db') as tc:
            await tc.execute('INSERT OR IGNORE INTO users(user_id) VALUES(?)', (msg.from_user.id,))
            await tc.execute('INSERT OR IGNORE INTO payments(user_id) VALUES(?)', (msg.from_user.id,))
            await tc.commit()
        async with aiosqlite.connect('teg.db') as tc:
            await tc.execute('INSERT OR IGNORE INTO usersw(user_id) VALUES(?)', (msg.from_user.id,))
            await tc.commit()

        await msg.answer('Добро пожаловать', reply_markup=starts_())



@router.callback_query(F.data ==('reffs'))
async def reffs_555(css: types.CallbackQuery):
    await css.answer()
    try:
        count_reffs = await get_reffs_count(css.from_user.id)
        balance_ = await get_ref_balance(css.from_user.id)
        await css.message.answer(f'💰 Ваш баланс : {balance_} \n\n 👥 Всего рефералов : {count_reffs[0]} \n\n 🔗 Ваша ссылка : https://t.me/OfficialKaifVpn_Bot?start={css.from_user.id} \n \n Чтобы вывести деньги, напишите @kaif_work')
    except:
        await css.message.answer(f'У вас еще нет бонусов за приведённого друга. Начните\n приглашать друзей и зарабатывайте! \n\n 🔗 Ваша ссылка :  https://t.me/OfficialKaifVpn_Bot?start={css.from_user.id}')




@router.callback_query(F.data == ('howto'))
async def hwtse(css: types.CallbackQuery):
    await css.answer()
    s = await get_user_stat(css.from_user.id)
    if s == 0 or s == 555:
        
        await css.message.answer('У вас нет подписки')

    else:

        await css.message.answer('Гайдик', reply_markup=send_url())



@router.callback_query(F.data.startswith('vpn'))
async def vpn_state(css: types.CallbackQuery):
    await css.answer()
    try:
        send_vpn = await get_user_vpn(css.from_user.id)
        pay_days = await get_payments_days(css.from_user.id)
        get_stat = await get_user_stat(css.from_user.id)
        get_vpn = await get_user_vpn(css.from_user.id)
        if get_stat == 1 and get_vpn == 0:   
            try:
                get_server = await set_client(userid=css.from_user.id,days=pay_days)
                if get_server[1]:
                    updated_text = re.sub(r'vless://.*?@', f'vless://{css.from_user.id}@', get_server[0])
                    updated_text = re.sub(r'spx=[^&]+', f'spx=%2F#{css.from_user.id}', updated_text)
                    await upt_user_vpn(userid=css.from_user.id,vpn=updated_text)
                    await css.message.answer(f'Ваша ссылка : \n `{updated_text}` ', parse_mode='Markdown')
            except Exception as e:
                print(e)
                await css.message.answer('Произошла ошибка свяжитесь с поддержкой')
        elif get_vpn != 0:
            await css.message.answer(text=f'Ваша ссылка : \n `{send_vpn}`', parse_mode='Markdown')
        elif get_stat == 555:
            await css.message.answer('Вы забанены')
        else:
            await css.message.answer('У вас нет подписки', reply_markup=oplata_infos())
    except Exception as e:
        print(e)
        await css.message.answer('Список VPN пуст пожалуйста обратитесь в поддержку')



@dp.callback_query(F.data == ('prems'))
async def guide(css: types.CallbackQuery):
    await css.answer()
    s = await get_user_stat(css.from_user.id)
    if s == 0:
        await css.message.answer(text=f'У вас еще нет подписки!', reply_markup=oplata_infos())
        
    else:
        datas_ = await get_user_date(userid=css.from_user.id)
        await css.message.answer(text=f'Ваша подписка : {datas_}')



@router.callback_query(F.data == ('infos'))
async def s555666(css: types.CallbackQuery):
    await css.answer()
    await css.message.answer('🌐Выберите кол-во месяцев, на которое вы хотите приобрести\n KAIF VPN:',reply_markup=payment_key())



@router.callback_query(F.data.startswith('payment_'))
async def payments_____(css: types.CallbackQuery):
    s = css.data.split('_')
    await css.answer()
    await css.message.delete()
    r_url = await get_payments_url(css.from_user.id)
    if r_url == 0:
        if str(s[1]) == '150':
            payms = await create_payment('150')
            await css.message.answer(f'Ваша ссылка для оплаты \n {payms[1]}')
            await upt_pay_infos(userid=css.from_user.id,status=payms[0],url=payms[1],days=30)
        elif str(s[1]) == '400':
            payms = await create_payment('400')
            await css.message.answer(f'Ваша ссылка для оплаты \n {payms[1]}')
            await upt_pay_infos(userid=css.from_user.id,status=payms[0],url=payms[1],days=90)
        elif str(s[1]) == '750':
            payms = await create_payment('750')
            await css.message.answer(f'Ваша ссылка для оплаты \n {payms[1]}')
            await upt_pay_infos(userid=css.from_user.id,status=payms[0],url=payms[1],days=180)
        elif str(s[1]) == '1400':
            payms = await create_payment('1400')
            await css.message.answer(f'Ваша ссылка для оплаты \n {payms[1]}')
            await upt_pay_infos(userid=css.from_user.id,status=payms[0],url=payms[1],days=360)
    else:
        await css.message.answer(f'У вас есть незаконченная оплата Хотите отменить? \n [Тык]({r_url})',parse_mode='Markdown', reply_markup=payment_cancel())



@router.callback_query(F.data == ('paycancel'))
async def payments______5555(css: types.CallbackQuery):
    await css.answer()
    await css.message.delete()
    await upt_pay_infos(userid=css.from_user.id,status=0,url=0,days=0)
    await css.message.answer('Отменено', reply_markup=payment_key())







@router.callback_query(F.data.startswith('otmenit_'))
async def ttttt(css: types.CallbackQuery):
    await css.answer()
    s = css.data.split('_')
    await css.message.answer(text=f'Отменен {s[1]}')

class addSer(StatesGroup):
    nickname_ = State()
    vpn_ = State()

class spam_(StatesGroup):
    spams = State()

class unbans(StatesGroup):
    nicknames_ = State()

class perevods(StatesGroup):
    infos_ = State()


class servInfo(StatesGroup):
    country_ = State()
    log_ = State()
    passw_ = State()
    sip_ = State()
    sinbound = State()

class reff5(StatesGroup):
    reff6 = State()


@router.callback_query(StateFilter(None), F.data == ('reff0'))
async def add_reff5(css: types.CallbackQuery, state: FSMContext):
    if css.from_user.id == 1624519308 or css.from_user.id == 6203509782:
        await css.answer()
        await css.message.answer('Введите ID Пользователя', reply_markup=cancel_())
        await state.set_state(reff5.reff6)


@router.message(reff5.reff6)
async def add_reff6(msg: types.Message, state: FSMContext): 
    try:
        await update_reff5(userid=int(msg.from_user.id))
        await msg.answer('Готово')
        await state.clear()
    except:
        await msg.answer(text='Чтото пошло не так')
        await state.clear()

@router.callback_query(StateFilter(None), F.data == ('add_server'))
async def add_server(css: types.CallbackQuery, state: FSMContext):
    if css.from_user.id == 1624519308 or css.from_user.id == 6203509782:
        await css.answer()
        await css.message.answer('Введите login от сервера', reply_markup=cancel_())
        await state.set_state(servInfo.country_)




@router.message(servInfo.country_)
async def add_server_6(msg: types.Message, state: FSMContext): 
    await state.update_data(country_=msg.text)
    await msg.answer('Введите Пароль от сервера', reply_markup=cancel_())


    await state.set_state(servInfo.log_)

@router.message(servInfo.log_)
async def vpn___(msg: types.Message, state: FSMContext):
    await state.update_data(passw_=msg.text)
    await msg.answer('Введите ссылку от VPN из панели', reply_markup=cancel_())
    await state.set_state(servInfo.passw_)


@router.message(servInfo.passw_)
async def add_server_8(msg: types.Message, state: FSMContext):
    await state.update_data(sip_=msg.text)
    if 'vless' in msg.text:
        await msg.answer('Введите IP PORT сервера пример 0.0.0.0:65000', reply_markup=cancel_())
        await state.set_state(servInfo.sip_)
    else:
        await msg.answer('Вы неправильно ввели ссылку', reply_markup=cancel_())


@router.message(servInfo.sip_)
async def add_server_7(msg: types.Message, state: FSMContext):
    await state.update_data(sinbound_=msg.text)
    try:
        if ':' in msg.text:
            await msg.answer('Введите ID панели клиентов пример (от 1 - 9)', reply_markup=cancel_())
            await state.set_state(servInfo.sinbound)
        else:
            await msg.answer('Вы неправильно ввели ссылку', reply_markup=cancel_())
    except Exception as e:
        await state.clear()
        await bot.send_message(chat_id=1624519308, text=str(e))
        await msg.answer('Чтото пошло не так')

@router.message(servInfo.sinbound)
async def add_server_555(msg: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        await insert_server_info(log=data['country_'], passw=data['passw_'],names=data['sip_'],sip=data['sinbound_'],sinbound=msg.text)
        await msg.answer('Готово', reply_markup=admins_key())
        await state.clear()
    except Exception as e:
        await state.clear()
        await bot.send_message(chat_id=1624519308, text=str(e))
        await msg.answer('Чтото пошло не так')



@dp.message(Command('admin'))
async def admins(msg: types.Message):
    if msg.from_user.id == 1624519308 or msg.from_user.id == 6203509782:
        async with aiosqlite.connect('tet.db') as tc:
            await tc.execute('UPDATE users SET status = 1 WHERE user_id = ?', (msg.from_user.id,))
            await tc.commit()
        await msg.answer('Админка', reply_markup=admins_key())








@router.callback_query(StateFilter(None), F.data.startswith('pay_'))
async def add_5(css: types.CallbackQuery, state: FSMContext):
    await css.answer()
    s = await get_user_stat(css.from_user.id)
    if s == 555:
        await css.message.answer('Вы были забанены обратитесь в службу поддержки')
    else:
        
        await css.message.answer('Напишите пожалуйста от кого перевод ?', reply_markup=cancel_())




    
    
    await state.set_state(perevods.infos_)


@router.message(perevods.infos_)
async def add_6(msg: types.Message, state: FSMContext):
    await bot.send_message(chat_id=-1002214194022,text=f'Пользователь `{msg.from_user.id}`, Оптлатил заказ \n \n от кого : {msg.text}', reply_markup=accept(userid=msg.from_user.id,rands='0',), parse_mode='Markdown')
    await msg.answer('Спасибо подождите')
    await state.clear()



@router.callback_query(StateFilter(None), F.data == ('add_vpn'))
async def add_uder(css: types.CallbackQuery, state: FSMContext):
    if css.from_user.id == 1624519308 or css.from_user.id == 6203509782:
        await css.answer()
        
        await css.message.answer('Введите ID из панели VPN', reply_markup=cancel_())

        await state.set_state(addSer.nickname_)

@router.message(addSer.nickname_)
async def nickname___(msg: types.Message, state: FSMContext):
    
    await state.update_data(nickname_=msg.text)
    await msg.answer('Введите ссылку от впн', reply_markup=cancel_())


    await state.set_state(addSer.vpn_)

@router.message(addSer.vpn_)
async def vpn___(msg: types.Message, state: FSMContext):
    try:
        data = await state.get_data()
        if 'vless' in msg.text:
            await insert_vpn(url=msg.text,names=str(data['nickname_']))
            await msg.answer('Готово', reply_markup=admins_key())
            await state.clear()
        else:
            await msg.answer('Вы неправильно ввели ссылку', reply_markup=cancel_())
    except Exception as e:
        await state.clear()
        await bot.send_message(chat_id=1624519308, text=e)
        await msg.answer('Чтото пошло не так')

@router.callback_query(F.data.startswith ('ban_'))
async def states_5(css: types.CallbackQuery):
    s = css.data.split('_')
    await css.answer()
    await upt_user_ban(userid=int(s[1]))
    await css.message.answer(text=f'Пользователь - {s[1]} забанен')



@router.callback_query(StateFilter(None), F.data == ('unban'))
async def sends_5(css: types.CallbackQuery, state: FSMContext):
    await css.answer()
        
    await css.message.answer('Введите ID :', reply_markup=cancel_())

    await state.set_state(unbans.nicknames_)



@router.message(unbans.nicknames_)
async def nickname___5(msg: types.Message, state: FSMContext):
    try:
        await upt_user_unban(userid=int(msg.text))
        await msg.answer('Готово')
        await state.clear()
    except Exception as e:
        print(e)
        await state.clear()


@router.callback_query(StateFilter(None), F.data == ('sender'))
async def sends(css: types.CallbackQuery, state: FSMContext):
    if css.from_user.id == 1624519308 or css.from_user.id == 6203509782:
        await css.answer()
        
        await css.message.answer('Введите текст рассылки', reply_markup=cancel_())

        await state.set_state(spam_.spams)



@router.message(spam_.spams)
async def nickname___(msg: types.Message, state: FSMContext):
    try:
        async with aiosqlite.connect('tet.db') as tc:
            async with tc.execute('SELECT user_id FROM users') as f:
                s = await f.fetchall()
        for i in s:
            try:
                await bot.send_message(chat_id=i[0],text=msg.text)
            except:
                pass
        await msg.answer('Рассылено')
        await state.clear()

    except Exception as e:
        print(e)
        await state.clear()
        await msg.answer('Чтото пошло не так')



@router.callback_query(StateFilter('*'), F.data == ('cansel'))
async def canels(css: types.CallbackQuery, state: FSMContext):
        await css.answer()
        await state.clear() 
        await css.message.answer('Отмена', reply_markup=starts_())


@router.callback_query(F.data == ('nazad'))
async def s555(css: types.CallbackQuery):
    await css.answer()
    await css.message.answer('Назад', reply_markup=starts_())



@router.callback_query(F.data == ('delete_server'))
async def funcs5(css: types.CallbackQuery):
    await css.answer()
    s = await get_server_info()
    
    key = servers_key(s)
    await css.message.answer('Просто нажми на сервер что бы удалить', reply_markup=key)

@router.callback_query(F.data.startswith ('removeserver_'))
async def funcs6(css: types.CallbackQuery):
    s = css.data.split('_')
    await css.answer()
    try:
        await delete_servers(sip=s[1])
        s = await get_server_info()
    
        key = servers_key(s)
        await css.message.answer('Просто нажми на сервер что бы удалить', reply_markup=key)
    except Exception as e:
        print(e)


@router.callback_query(F.data == ('backup'))
async def funcs7(css: types.CallbackQuery):
    await css.answer()
    s = InputFile('tet.db')
    r = InputFile('teg.db')
    await bot.send_document(chat_id=css.from_user.id,document=s)
    await bot.send_document(chat_id=css.from_user.id,document=r)

async def main():
    await datas()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())





if __name__ == "__main__":
    try:
        asyncio.run(main())  
    except Exception as e:
        print(e)