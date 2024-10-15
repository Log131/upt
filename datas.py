import aiosqlite

import datetime

import asyncio


async def upt_user_date(userid,days):
    time_delete = (datetime.datetime.now() + datetime.timedelta(days=int(days))).strftime('%Y-%m-%d %H:%M')
    async with aiosqlite.connect('tet.db') as tc:
        await tc.execute('UPDATE users SET date = ? WHERE user_id = ?', (time_delete,userid,))
        await tc.commit()

async def get_user_stat(userid):
    async with aiosqlite.connect('tet.db') as tc:
       async with tc.execute('SELECT status FROM users WHERE user_id = ?',(userid,)) as f:
           s = await f.fetchone()
    return s[0]

async def insert_server_info(log,passw,names,sip,sinbound):
    async with aiosqlite.connect('tet.db') as tc:
        await tc.execute('INSERT OR IGNORE INTO server(log,passw,names,sip,sinbound) VALUES (?,?,?,?,?)', (log,passw,names,sip,sinbound,))
        await tc.commit()


async def update_server_info(log,passw):
    async with aiosqlite.connect('tet.db') as tc:
        await tc.execute('UPDATE server SET log = ?, passw = ? WHERE country = ?', (log,passw,))
        await tc.commit()

async def get_server_info():
    async with aiosqlite.connect('tet.db') as tc:
       async with tc.execute('SELECT * FROM server') as f:
           s = await f.fetchall()
    
    return s

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
        await tc.execute('UPDATE reff SET balance = balance + 15 WHERE userid = ?', (userid,))
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
        await tc.execute('INSERT OR IGNORE INTO reff(refid,userid) VALUES(?,?)', (refid,userid,))
        await tc.commit()



async def get_reffs_count(userid):
    async with aiosqlite.connect('tet.db') as tc:
        async with tc.execute('SELECT COUNT(refid) FROM reff WHERE userid = ?', (userid,)) as f:
            s = await f.fetchall()  
    
    
    
    
    
    
    return s[0]


async def get_reffs(userid):
    async with aiosqlite.connect('tet.db') as tc:
        async with tc.execute('SELECT userid,status FROM reff WHERE refid = ?', (userid,)) as f:
            s = await f.fetchone()
    
    return s


async def get_ref_balance(userid):
    async with aiosqlite.connect('tet.db') as tc:
        async with tc.execute('SELECT balance FROM reff WHERE userid = ?', (userid,)) as f:
            s = await f.fetchone()
    
    return s[0]


async def get_payments_info(userid):
    async with aiosqlite.connect('tet.db') as tc:
        async with tc.execute('SELECT status FROM payments WHERE user_id = ?', (userid,)) as f:
            s = await f.fetchone()
    
    return s[0]


async def get_payments_days(userid):
    async with aiosqlite.connect('tet.db') as tc:
        async with tc.execute('SELECT days FROM payments WHERE user_id = ?', (userid,)) as f:
            s = await f.fetchone()
    
    return s[0]

async def upt_pay_infos(userid,status,url,days):
    async with aiosqlite.connect('tet.db') as tc:
        await tc.execute('UPDATE payments SET status = ?, url = ?, days = ? WHERE user_id = ?', (status,url,days,userid,))
        await tc.commit()

async def get_payments_url(userid):
    async with aiosqlite.connect('tet.db') as tc:
        async with tc.execute('SELECT url FROM payments WHERE user_id = ?', (userid,)) as f:
            s = await f.fetchone()
    
    return s[0]

async def update_reff5(userid):
    async with aiosqlite.connect('teg.db') as tc:
        await tc.execute('UPDATE reff SET balance = 0 WHERE user_id = ?', (userid,))
        await tc.commit()

async def update_usersw(userid,sip,log,passw,inbound):
    async with aiosqlite.connect('teg.db') as tc:
        await tc.execute('UPDATE usersw SET sip = ?, sinbound = ?,log = ?, passw = ? WHERE user_id = ?', (sip,inbound,log,passw,userid,))
        await tc.commit()

async def get_usersw_infos(userid):
    async with aiosqlite.connect('teg.db') as tc:
        async with tc.execute('SELECT sip,log,passw,sinbound FROM usersw WHERE user_id = ?', (userid,)) as f:
            s = await f.fetchone()
    
    return s[0]

async def delete_servers(sip):
    async with aiosqlite.connect('tet.db') as tc:
        await tc.execute('DELETE FROM server WHERE sip = ?', (sip,))
        await tc.commit()