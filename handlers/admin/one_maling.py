from aiogram.dispatcher import FSMContext
from handlers.admin.user import user_callback
from loader import dp
from loader import bot
from data.config import admins_id
from aiogram import types
from utils.inline_btn import create_markup
from static.text import admin
from handlers.admin.start import AdminState


@dp.message_handler(chat_type='private', state=AdminState.one_mailing, chat_id=admins_id, content_types=['photo', 'text'])
async def one_mailing_message(message: types.Message, state: FSMContext):
    if message.photo:
        await state.update_data(photo=message.photo[-1].file_id)
    await state.update_data(text=message.html_text)
    await AdminState.one_mailing_button.set()
    markup = create_markup('inline', 2, ['✅ Да', 'yes'], ['❌ Нет', 'no'], ['❌ Отмена', 'cancel'])
    await bot.send_photo(message.chat.id, open('static/img/saved_text_mailing.png', 'rb'),
                         caption=admin.text_saved_mailing, reply_markup=markup)


@dp.callback_query_handler(chat_type='private', state=AdminState.one_mailing, chat_id=admins_id)
async def one_mailing_callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'cancel':
        data = await state.get_data()
        await state.finish()
        call.data = f'id{data["id"]}'
        await call.answer(admin.cancel_user)
        await user_callback(call, state)


@dp.callback_query_handler(chat_type='private', state=AdminState.one_mailing_button, chat_id=admins_id)
async def one_mailing_button_callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        await AdminState.one_mailing_button_compilet.set()
        markup = create_markup('inline', 1, ['❌ Отмена', 'cancel'])
        await bot.edit_message_media(types.InputMediaPhoto(open('static/img/saved_button_mailing.png', 'rb'),
                                                           caption=admin.text_mailing_button),
                                     call.from_user.id, call.message.message_id, reply_markup=markup)
    elif call.data == 'no':
        await AdminState.one_mailing_button_compilet.set()
        await state.update_data(markup=None)
        call.message.text = 'None'
        await one_mailing_button_message(call.message, state)
    elif call.data == 'cancel':
        await one_mailing_callback(call, state)


@dp.message_handler(chat_type='private', state=AdminState.one_mailing_button_compilet, chat_id=admins_id)
async def one_mailing_button_message(message: types.Message, state: FSMContext):
    if message.text == 'None':
        data = await state.get_data()
        if 'photo' in data.keys():
            await bot.send_photo(message.chat.id, data['photo'], caption=data['text'], parse_mode='html')
        else:
            await bot.send_message(message.chat.id, data['text'], parse_mode='html')
    else:
        data = message.text.split('\n')
        markup = create_markup('inline', int(data[0]), *list(map(lambda x: [x.split(':::')[0], x.split(':::')[1].split(']')[0]], data[1].split('[')[1:])))
        await state.update_data(markup=markup)
        data = await state.get_data()
        if 'photo' in data.keys():
            await bot.send_photo(message.chat.id, data['photo'], caption=data['text'], reply_markup=markup,
                                 parse_mode='html')
        else:
            await bot.send_message(message.chat.id, data['text'], reply_markup=markup, parse_mode='html')
    markup = create_markup('inline', 2, ['✅ Да', 'yes'], ['❌ Нет', 'no'], ['❌ Отмена', 'cancel'])
    await bot.send_photo(message.chat.id, open('static/img/mailing.png', 'rb'), caption=admin.text_is_good_mailing, reply_markup=markup)
    await AdminState.is_good_mailing.set()


@dp.callback_query_handler(chat_type='private', state=AdminState.one_mailing_button_compilet, chat_id=admins_id)
async def one_mailing_button_compilet_callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'cancel':
        await one_mailing_callback(call, state)


@dp.callback_query_handler(chat_type='private', state=AdminState.is_good_mailing, chat_id=admins_id)
async def one_mailing_good_callback(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'yes':
        data = await state.get_data()
        await state.finish()
        try:
            if 'photo' in data.keys():
                await bot.send_photo(data['id'], data['photo'], caption=data['text'], reply_markup=data['markup'],
                                     parse_mode='html')
            else:
                await bot.send_message(data['id'], data['text'], reply_markup=data['markup'], parse_mode='html')
            await bot.edit_message_media(types.InputMediaPhoto(open('static/img/good_mailing.png', 'rb'),
                                                               caption=admin.text_good_mailing.format(
                                                                   call.from_user.first_name)),
                                         call.from_user.id, call.message.message_id)
        except Exception:
            await bot.edit_message_media(types.InputMediaPhoto(open('static/img/bad_mailing.png', 'rb'),
                                                               caption=admin.text_bad_mailing),
                                         call.from_user.id, call.message.message_id)
    elif call.data == 'no' or call.data == 'cancel':
        await one_mailing_callback(call, state)
