from loader import dp
from loader import bot
from data.config import rate

from aiogram import types
from handlers.users.start import anti_flood

from static.text import users
from utils.db_api import db_users
from utils.top_rating import check


@dp.message_handler(chat_type='private', commands=['profile'])
@dp.throttled(anti_flood, rate=rate)
async def profile_command(message: types.Message):
    await profile_message(message)


@dp.message_handler(chat_type='private', regexp='⭐ Мой профиль')
@dp.throttled(anti_flood, rate=rate)
async def profile_message(message: types.Message):
    data = db_users.deanon(message.chat.id)

    teht = check(data)

    await bot.send_message(message.chat.id,
                           users.text_profile.format(data.id, data.username,
                                                     round((data.win_count / data.all_count) * 100, 2)
                                                     if data.all_count else 0, data.date,
                                                     data.all_count, data.win_count, teht))
