from loader import dp
from loader import bot
from data.config import rate

from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup

from static.text import users
from utils.inline_btn import create_markup
from utils.db_api import db_users


class UserState(StatesGroup):
    games = State()


MAIN_MARKUP = create_markup('reply', 2, ['🎲 Играть'], ['⭐ Мой профиль'], ['⚡ Топ рейтинг'], ['☃ О нас'])


async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.answer(users.text_flood)


@dp.message_handler(chat_type='private', commands=['start'])
@dp.throttled(anti_flood, rate=rate)
async def start_message(message: types.Message):
    if not db_users.check_user(message.chat.id):
        db_users.add_user(message.chat.id, message.chat.username, message.chat.full_name)
    await bot.send_message(message.chat.id, users.text_start.format(message.from_user.first_name),
                           reply_markup=MAIN_MARKUP)
