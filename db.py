import asyncio
from random import randint

import aiomysql
from aiomysql import Pool

import config

import datetime

pool: Pool
# conn: aiomysql.connection.Connection


async def if_user_exists(user_id) -> bool:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"SELECT * FROM users WHERE user_id='{user_id}';")
            return await cur.fetchone() is not None


async def update_user_data(user_id, user_name, check) -> bool:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            if check:
                await cur.execute(f"UPDATE users SET user_name='{user_name}' WHERE user_id='{user_id}';")
            else:
                await cur.execute(f"INSERT INTO users(user_id, sub_status, user_name) "
                                  f"VALUES ('{user_id}', '{0}', '{user_name}');")
            return await conn.commit() is None


async def check_cv(user_id) -> int:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"SELECT * FROM cvs WHERE user_id='{user_id}';")
            return await cur.fetchone() is not None


async def save_cv(user_id, name, email, phone, link, spec) -> bool:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            if await check_cv(user_id):
                await cur.execute(f"DELETE FROM skills WHERE user_id='{user_id}';")
            if await conn.commit() is None:
                await cur.execute(f"INSERT INTO cvs(user_id, name, email, phone, link, spec, inactive_status, status) "
                                  f"VALUES ('{user_id}', '{name}', '{email}', '{phone}', '{link}', '{spec}', {-1}, "
                                  f"{False});")
            return await conn.commit() is None


async def check_user_projects_count(user_id) -> int:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"SELECT * FROM projects WHERE user_id='{user_id}';")
            arr = await cur.fetchall()
            return len(arr)


async def if_user_can_create_project(user_id) -> int:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            count = await check_user_projects_count(user_id)
            await cur.execute(f"SELECT sub_status FROM users WHERE user_id='{user_id}';")
            status = (await cur.fetchone())[0]
            print(status)
            if status == 0 and count == 1:
                return 0
            elif status == 0:
                return -1
            elif status == 1 and count > config.basic_projects_count:
                return 1
            return 2


async def get_user_sub_state(user_id) -> int:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            count = await check_user_projects_count(user_id)
            await cur.execute(f"SELECT sub_status FROM users WHERE user_id='{user_id}';")
            return await cur.fetchone()


async def save_project(user_id, title, spec, descr, price, state) -> int:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            num = randint(1000, 9999)
            await cur.execute(f"""SELECT project_id FROM projects WHERE project_id='{num}'""")
            while await cur.fetchone() is not None:
                num = randint(1000, 9999)
                await cur.execute(f"""SELECT project_id FROM projects WHERE project_id='{num}'""")
            await cur.execute(f"INSERT INTO projects(user_id, project_id, title, spec, descr, price, state)"
                              f" VALUES ('{user_id}', '{num}', '{title}', '{spec}', '{descr}',"
                              f" '{price}', '{state}');")
            await conn.commit()
            return num


async def get_user_cv(user_id):
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"SELECT * FROM cvs WHERE user_id='{user_id}';")
            cv = await cur.fetchone()
            if cv is None:
                return None
            return cv


async def accept_cv(user_id) -> bool:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"UPDATE cvs SET inactive_status='1', status='1' WHERE user_id='{user_id}';")
            return await conn.commit() is None


async def delete_cv(user_id) -> bool:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"DELETE FROM cvs WHERE user_id='{user_id}';")
            return await conn.commit() is None


async def accept_project(order_id, user_id) -> bool:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            if await if_user_can_create_project(user_id) == 2:
                expiration = datetime.datetime.now() + datetime.timedelta(days=config.expiration)
                await cur.execute(
                    f"UPDATE projects SET expiration='{expiration}', state='1' WHERE project_id='{order_id}';")
                return await conn.commit() is None
            return False


async def delete_projects(order_id) -> bool:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"DELETE FROM projects WHERE project_id='{order_id}';")
            return await conn.commit() is None


async def get_user_projects(user_id):
    # async with pool.acquire() as conn:
    #     async with conn.cursor() as cur:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"SELECT * FROM projects WHERE user_id='{user_id}' AND state != 0;")
            arr = await cur.fetchall()
            print(arr)
            result = []
            for i in arr:
                if i[7] == 1:
                    result.append(i)
            return result


async def fetch_specialists(spec, client_id):
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"SELECT * FROM cvs WHERE spec='{spec}' AND inactive_status='{1}' AND user_id!='{client_id}';")
            return await cur.fetchall()


async def add_like(client_id, spec_id, project_id) -> bool:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"INSERT INTO likes(project_id, client_id, spec_id) VALUES ('{project_id}', '{client_id}',"
                f"'{spec_id}');")
            return await conn.commit() is None


async def reply_to_offer(project_id) -> int:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(f"SELECT client_id FROM likes WHERE project_id='{project_id}'")
            client = await cur.fetchone()
            if client is not None:
                await cur.execute(f"DELETE FROM likes WHERE project_id='{project_id}'")
                await conn.commit()
                return client[0]
            else:
                raise Exception('No likes for user')


async def get_specialist_info(user_id) -> list:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"SELECT * FROM users INNER JOIN cvs ON users.user_id = cvs.user_id WHERE users.user_id='{user_id}';")
            return await cur.fetchone()


async def buy_basic_subscription(user_id) -> list:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"UPDATE users SET sub_status='{1}' WHERE user_id='{user_id}';")
            return await conn.commit() is None


async def if_user_afk(user_id) -> int:
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"SELECT inactive_status FROM cvs WHERE user_id='{user_id}';")
            return (await cur.fetchone())[0]


async def switch_afk(user_id, b):
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"UPDATE cvs SET inactive_status='{b}' WHERE user_id='{user_id}';")
            return await conn.commit() is None


async def get_unsubscribed_projects(user_id):
    # async with pool.acquire() as conn:
    async with aiomysql.connect(host=config.db_host, port=config.db_port, user=config.db_login,
                                password=config.db_password, db=config.db_name, loop=asyncio.get_event_loop()) as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                f"SELECT * FROM projects WHERE user_id='{user_id}' AND state='{-1}';")
            return await cur.fetchone()
