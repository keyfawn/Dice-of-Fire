from loader import dp
from loader import bot
from data.config import rate

from aiogram import types
from handlers.users.start import anti_flood

from static.text import users
from utils.inline_btn import create_markup
from utils.db_api import db_users


@dp.message_handler(commands=['rating'])
@dp.throttled(anti_flood, rate=rate)
async def rating_command(message: types.Message):
    await rating_message(message)


@dp.message_handler(regexp='⚡ Топ рейтинг')
@dp.throttled(anti_flood, rate=rate)
async def rating_message(message: types.Message, target=None):
    top = db_users.return_win()
    markup = create_markup('inline', 2, *list(map(lambda x: [f'🌟 {x[0]}', f'id{x[1]}'], top))[:10])
    if target:
        await bot.edit_message_media(types.InputMediaPhoto(open('static/img/top_rating.png', 'rb'),
                                                           caption=users.text_top), message.chat.id, message.message_id,
                                     reply_markup=markup)
    else:
        await bot.send_photo(message.chat.id, open('static/img/top_rating.png', 'rb'), caption=users.text_top,
                             reply_markup=markup)


@dp.callback_query_handler()
@dp.throttled(anti_flood, rate=rate)
async def rating_callback(call: types.CallbackQuery):
    if call.data[:2] == 'id':
        data = db_users.deanon(call.data[2:])

        games = {'⚽': data.football,
                 '🎯': data.darts,
                 '🎲': data.dice,
                 '🏀': data.basketball,
                 '🎳': data.bowling,
                 '🎰': data.slot}
        maxi = max(games.values())
        teht = ''
        for game in games.keys():
            if games[game] == maxi:
                teht = teht + game

        ava = await bot.get_user_profile_photos(data.id)
        markup = create_markup('inline', 2, ['⚔ Посмотреть', f'u3l*tg://user?id={data.id}'], ['❌ Назад', 'cancel'])

        photo = ava.photos[0][-1].file_id if ava.photos else open('static/img/no_ava.png', 'rb')
        await bot.edit_message_media(types.InputMediaPhoto(photo, caption=users.text_top_info.format(
            data.first_name, round((data.win_count / data.all_count) * 100, 2) if data.all_count else 0,
            data.date, data.all_count, data.win_count, teht)), call.from_user.id, call.message.message_id,
                                     reply_markup=markup)
    elif call.data == 'cancel':
        await call.answer(users.cancel_top)
        await rating_message(call.message, 'yes')
