from loader import dp
from loader import bot
from data.config import rate, support_id, channel_username

from aiogram import types
from handlers.users.start import anti_flood

from static.text import users
from utils.inline_btn import create_markup


@dp.message_handler(chat_type='private', commands=['about'])
@dp.throttled(anti_flood, rate=rate)
async def about_command(message: types.Message):
    await about_message(message)


@dp.message_handler(chat_type='private', regexp='☃ О нас')
@dp.throttled(anti_flood, rate=rate)
async def about_message(message: types.Message):
    markup = create_markup('inline', 2, ['🚀 Наш канал', f'u3l*https://t.me/{channel_username}'],
                           *list(map(lambda x: ['💤 Поддержка', f'u3l*tg://user?id={x}'], support_id)))
    await bot.send_message(message.chat.id, users.text_about.format(message.chat.full_name), reply_markup=markup)
