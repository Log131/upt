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









async def datas():
    async with aiosqlite.connect('tet.db') as tc:
        await tc.execute('CREATE TABLE IF NOT EXISTS users(user_id PRIMARY KEY,status DEFAULT 0, vpn DEFAULT 0, date)')
        await tc.execute('CREATE TABLE IF NOT EXISTS vpn(names PRIMARY KEY, lists)')
        await tc.execute('CREATE TABLE IF NOT EXISTS ref(refid PRIMARY KEY, userid, balance DEFAULT 0)')
        await tc.commit()




async def upt_user_date(userid):
    time_delete = (datetime.datetime.now() + datetime.timedelta(days=int(30))).strftime('%Y-%m-%d %H:%M')
    async with aiosqlite.connect('tet.db') as tc:
        await tc.execute('UPDATE users SET date = ? WHERE user_id = ?', (time_delete,userid,))
        await tc.commit()

async def get_user_stat(userid):
    async with aiosqlite.connect('tet.db') as tc:
       async with tc.execute('SELECT status FROM users WHERE user_id = ?',(userid,)) as f:
           s = await f.fetchone()
    return s[0]



async def get_user_vpn(userid):
    async with aiosqlite.connect('tet.db') as tc:
       async with tc.execute('SELECT vpn FROM users WHERE user_id = ?',(userid,)) as f:
           s = await f.fetchone()
    return s[0]

async def upt_user_vpn(userid, vpn):
    async with aiosqlite.connect('tet.db') as tc:
        
        await tc.execute('UPDATE users SET vpn = ? WHERE user_id = ?', (vpn, userid,))

        
        await tc.commit()

async def upt_user_ban(userid):
    async with aiosqlite.connect('tet.db') as tc:
        await tc.execute('UPDATE users SET status = 555 WHERE user_id = ?', (userid,))
        await tc.commit()

async def upt_user_unban(userid):
    async with aiosqlite.connect('tet.db') as tc:
        await tc.execute('UPDATE users SET status = 0 WHERE user_id = ?', (userid,))
        await tc.commit()

async def upt_user_stat(userid):
    async with aiosqlite.connect('tet.db') as tc:
        await tc.execute('UPDATE users SET status = 1 WHERE user_id = ?', (userid,))
        await tc.commit()

async def upt_ref_balance(userid):
    async with aiosqlite.connect('tet.db') as tc:
        await tc.execute('UPDATE ref SET balance = balance + 15 WHERE userid = ?', (userid,))
        await tc.commit()

async def get_user_date(userid):
    async with aiosqlite.connect('tet.db') as tc:
        async with tc.execute('SELECT date FROM users WHERE user_id = ?', (userid,)) as f:
            s = await f.fetchone()

    return s[0]

async def insert_vpn(url, names):
    async with aiosqlite.connect('tet.db') as tc:
        await tc.execute('INSERT OR IGNORE INTO vpn(names,lists) VALUES(?,?)', (names,url,))
        await tc.commit()

async def choose_vpn():
    async with aiosqlite.connect('tet.db') as tc:
        async with tc.execute('SELECT * FROM vpn') as f:
            s = await f.fetchall()
    
    return s

async def delete_vpn(clientid):
    async with aiosqlite.connect('tet.db') as tc:
        await tc.execute('DELETE FROM vpn WHERE names = ?', (clientid,))
        await tc.commit()


async def insert_reffs(refid,userid):
    async with aiosqlite.connect('tet.db') as tc:
        await tc.execute('INSERT OR IGNORE INTO ref(refid,userid) VALUES(?,?)', (refid,userid,))
        await tc.commit()



async def get_reffs_count(userid):
    async with aiosqlite.connect('tet.db') as tc:
        async with tc.execute('SELECT COUNT(refid) FROM ref WHERE userid = ?', (userid,)) as f:
            s = await f.fetchall()  
    
    
    
    
    
    
    return s[0]


async def get_reffs(userid):
    async with aiosqlite.connect('tet.db') as tc:
        async with tc.execute('SELECT userid FROM ref WHERE refid = ?', (userid,)) as f:
            s = await f.fetchone()
    
    return s[0]


async def get_ref_balance(userid):
    async with aiosqlite.connect('tet.db') as tc:
        async with tc.execute('SELECT balance FROM ref WHERE userid = ?', (userid,)) as f:
            s = await f.fetchone()
    
    return s[0]


dp = Dispatcher()
router = Router()

bot = Bot(token='7420265405:AAEojcS8CRjT5sRqlgrqTsSdsWToUptnNzc')
dp.include_router(router=router) 










@dp.message(CommandStart())
async def start_(msg: types.Message):
    invited_ref_id = msg.text.replace('/start', '').replace(' ', '')
    if invited_ref_id and int(invited_ref_id) != msg.from_user.id:
        await insert_reffs(refid=msg.from_user.id, userid=int(invited_ref_id))
        async with aiosqlite.connect('tet.db') as tc:
            await tc.execute('INSERT OR IGNORE INTO users(user_id) VALUES(?)', (msg.from_user.id,))
            await tc.commit()
        await msg.answer('Добро пожаловать', reply_markup=starts_())
    else:
        async with aiosqlite.connect('tet.db') as tc:
            await tc.execute('INSERT OR IGNORE INTO users(user_id) VALUES(?)', (msg.from_user.id,))
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
        rands = random.choice(await choose_vpn())
        vpn_clintid = rands[0]
        vpn_url = rands[1]
        get_stat = await get_user_stat(css.from_user.id)
        get_vpn = await get_user_vpn(css.from_user.id)
        if get_stat == 1 and get_vpn == 0:   
            await css.message.answer(f'Ваша ссылка : \n `{vpn_url}`', parse_mode='Markdown')
            await upt_user_vpn(userid=css.from_user.id, vpn=vpn_url)
            await delete_vpn(clientid=vpn_clintid)
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
    rands = random.randrange(00000,99999)
    s = await get_user_stat(css.from_user.id)
    if s == 0:
        await css.message.answer(text=f'У вас еще нет подписки!\n\nПереведи деньги по реквизитам и нажми оплатил!\n\nСейчас акция в честь открытия ВПН, цена подписки всего 100 \n рублей на месяц!\n\nПри переводе  обязательно укажите комментарий\n`{css.from_user.id}`    (Нажми на циферки и они скопируют сами)\n\nЕсли комментария не будет, подписка не засчитается',parse_mode='Markdown')
        await css.message.answer(text='Реквизиты для перевода:\n\n🏦 Русский Стандарт Банк\n💳 5100472474930137\n\n📲 +79106265792\n\n🤖 💳 Станислав С. \n\nОПЛАТА МОЖЕТ ОСУЩЕСТВЛЯТЬСЯ НА БАНК, ЧТО Я УКАЗАЛ,\nРУССКИЙ СТАНДРТ БАНК, ЕСЛИ ВЫ ОТПРАВИЛИ ПЛАТЁЖ НЕ НА\nТОТ БАНК, ОПЛАТА БУДЕТ НЕ ДЕЙСТВИТЕЛЬНА',reply_markup=get_pay(userid=css.from_user.id,rands=rands))
    
    
    
    else:
        datas_ = await get_user_date(userid=css.from_user.id)
        await css.message.answer(text=f'Ваша подписка : {datas_}')



@router.callback_query(F.data == ('infos'))
async def s555666(css: types.CallbackQuery):
    await css.answer()
    s = await get_user_stat(css.from_user.id)
    rands = random.randrange(00000,99999)
    await css.message.answer(text=f'У вас еще нет подписки!\n\nПереведи деньги по реквизитам и нажми оплатил!\n\nСейчас акция в честь открытия ВПН, цена подписки всего 100 \n рублей на месяц!\n\nПри переводе  обязательно укажите комментарий\n`{css.from_user.id}`    (Нажми на циферки и они скопируют сами)\n\nЕсли комментария не будет, подписка не засчитается',parse_mode='Markdown')
    await css.message.answer(text='Реквизиты для перевода:\n\n🏦 Русский Стандарт Банк\n💳 5100472474930137\n\n📲 +79106265792\n\n🤖 💳 Станислав С. \n\nОПЛАТА МОЖЕТ ОСУЩЕСТВЛЯТЬСЯ НА БАНК, ЧТО Я УКАЗАЛ,\nРУССКИЙ СТАНДРТ БАНК, ЕСЛИ ВЫ ОТПРАВИЛИ ПЛАТЁЖ НЕ НА\nТОТ БАНК, ОПЛАТА БУДЕТ НЕ ДЕЙСТВИТЕЛЬНА',reply_markup=get_pay(userid=css.from_user.id,rands=rands))

#@router.callback_query(F.data.startswith('pay_'))
#async def s666555(css: types.CallbackQuery):
   # s = css.data.split('_')
    #await css.answer()
    #await css.message.delete()
    #await css.message.answer('Спасибо подождите')
    #await bot.send_message(chat_id=-1002214194022,text=f'Пользователь `{s[1]}`, Оптлатил заказ {s[2]}', reply_markup=accept(userid=s[1],rands=s[2],), parse_mode='Markdown')


@router.callback_query(F.data.startswith('accept_'))
async def acc(css: types.CallbackQuery):
    await css.answer()
    s = css.data.split('_')
    try:
        reffs = await get_reffs(userid=int(s[1]))

        await upt_ref_balance(userid=int(reffs))
        await css.message.answer(text=f'Завершено {s[1]}')
        await upt_user_stat(userid=int(s[1]))
        await upt_user_date(userid=int(s[1]))
        await bot.send_message(chat_id=s[1],text='Спасибо можете пользоваться VPN\n\n Нажмите на Подключить VPN и получите ссылку /start')
    
        try:
            await bot.send_message(chat_id=int(reffs), text='На ваш баланс зачислено 15 рублей за приведённого друга')
        except:
            pass
    except:
        await upt_user_stat(userid=int(s[1]))
        await upt_user_date(userid=int(s[1]))
        await bot.send_message(chat_id=s[1],text='Спасибо можете пользоваться VPN\n\n Нажмите на Подключить VPN и получите ссылку /start')





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


@dp.message(Command('admin'))
async def admins(msg: types.Message):
    if msg.from_user.id == 1624519308 or msg.from_user.id == 6203509782:
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


async def main():
    await datas()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())





if __name__ == "__main__":
    try:
        asyncio.run(main())  
    except Exception as e:
        print(e)