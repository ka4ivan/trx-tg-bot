from asyncio import sleep
from aiogram.dispatcher import FSMContext

from db_api import db_quick_commands
from db_api.schemas.users import Users_model as users
from config import dp, bot, _
from aiogram import types
from handlers.states import say_hi
import keyboards as kb


#######################################################################################################################################
from settings import session

price_text = 50
price_photo = 60
price_audio = 60
price_all = 80


@dp.message_handler(state=say_hi.text)
async def say_hi_text(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(text=answer)
    markup_say_hi_add_photo, markup_say_hi_add_audio, markup_say_hi_add_audio_mod = await kb.markup_say(message)
    await message.answer(text=answer, reply_markup=markup_say_hi_add_photo)
    await say_hi.state.set()


@dp.callback_query_handler(text='next', state=say_hi.state)
async def say_hi_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    markup_say_hi_add_photo, markup_say_hi_add_audio, markup_say_hi_add_audio_mod = await kb.markup_say(message)
    await bot.send_message(message.from_user.id, text=text, reply_markup=markup_say_hi_add_audio_mod)


@dp.callback_query_handler(text='send_text_msg', state=say_hi.state)
async def say_hi_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    await bot.send_message(message.from_user.id, text=text)
    markup_succes_say_hi = await kb.markup_succes_say_hi(message)
    await bot.send_message(message.from_user.id, _("Ви дійсно хочете надіслати на перевірку повідомлення зверху?"), reply_markup=markup_succes_say_hi, parse_mode='html')


@dp.callback_query_handler(text='succes_say_hi', state=say_hi.state)
async def start(call: types.callback_query, state: FSMContext):
    user = await users.query.where(users.user_id == call.message.chat.id).gino.first()
    user_balance = user.bal_trx
    if user_balance >= price_text:
        data = await state.get_data()
        text = data.get('text')
        try:
            await dp.bot.send_message(chat_id=5143177713, text=f'__________________________________________________________________'
                                                               f'\nРозсилка Текст\n\n<b><i>User_id</i> = {call.message.chat.id}</b>\n<b><i>LANGUAGE</i> = {user.user_language}</b>', parse_mode='html')
            await dp.bot.send_message(chat_id=5143177713, text=text, parse_mode='html')
            await dp.bot.send_message(chat_id=5143177713, text=f'<b><i>User_id</i> = {call.message.chat.id}</b>\n\nРозсилка Текст\n\n'
                                                               f'__________________________________________________________________', parse_mode='html')
            await db_quick_commands.register_say_hi(call.message.chat.id, text, False, False)
            session.commit()
            await sleep(0.33)
        except Exception:
            pass
        await state.finish()
        await users.update.values(bal_trx=users.bal_trx - price_text).where(users.user_id == call.message.chat.id).gino.status()
        session.commit()
        markup_start = await kb.markup_start(call.message)
        await call.message.answer(_("✅ <b><i>Повідомлення надіслано в <u>модерацію</u></i></b>"), reply_markup=markup_start, parse_mode='html')
        await call.message.answer(_("ℹ З балансу знято <b><i>{}</i></b> TRX".format(price_text)), parse_mode='html')
    else:
        markup_start = await kb.markup_start(call.message)
        await bot.send_message(call.message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html', reply_markup=markup_start)
        await state.finish()


@dp.callback_query_handler(text='add_photo', state=say_hi.state)
async def add_photo(call: types.callback_query):
    await call.message.answer(_("📸 Надішліть фото"))
    await say_hi.photo.set()


@dp.message_handler(state=say_hi.photo, content_types=types.ContentType.PHOTO)
async def say_hi_text(message: types.Message, state: FSMContext):
    photo_file_id = message.photo[-1].file_id
    await state.update_data(photo=photo_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    markup_say_hi_add_photo, markup_say_hi_add_audio, markup_say_hi_add_audio_mod = await kb.markup_say(message)
    await message.answer_photo(photo=photo, caption=text, reply_markup=markup_say_hi_add_audio)


@dp.callback_query_handler(text='next', state=say_hi.photo)
async def say_hi_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    await bot.send_photo(message.from_user.id, photo=photo, caption=text)
    markup_succes_say_hi = await kb.markup_succes_say_hi(message)
    await bot.send_message(message.from_user.id, _("Ви дійсно хочете надіслати на перевірку повідомлення зверху?"), reply_markup=markup_succes_say_hi, parse_mode='html')


@dp.callback_query_handler(text='succes_say_hi', state=say_hi.photo)
async def start(call: types.callback_query, state: FSMContext):
    user = await users.query.where(users.user_id == call.message.chat.id).gino.first()
    user_balance = user.bal_trx
    if user_balance >= price_photo:
        data = await state.get_data()
        text = data.get('text')
        photo = data.get('photo')
        try:
            await dp.bot.send_message(chat_id=5143177713, text=f'__________________________________________________________________'
                                                               f'\nРозсилка Фото\n\n<b><i>User_id</i> = {call.message.chat.id}</b>\n<b><i>LANGUAGE</i> = {user.user_language}</b>', parse_mode='html')
            await dp.bot.send_photo(chat_id=5143177713, photo=photo, caption=text, parse_mode='html')
            await dp.bot.send_message(chat_id=5143177713, text=f'<b><i>User_id</i> = {call.message.chat.id}</b>\n\nРозсилка Музика\n\n'
                                                               f'__________________________________________________________________', parse_mode='html')
            await db_quick_commands.register_say_hi(call.message.chat.id, text, True, False)
            session.commit()
            await sleep(0.33)
        except Exception:
            pass
        await state.finish()
        await users.update.values(bal_trx=users.bal_trx - price_photo).where(users.user_id == call.message.chat.id).gino.status()
        session.commit()
        markup_start = await kb.markup_start(call.message)
        await call.message.answer(_("✅ <b><i>Повідомлення надіслано в <u>модерацію</u></i></b>"), reply_markup=markup_start, parse_mode='html')
        await call.message.answer(_("ℹ З балансу знято <b><i>{}</i></b> TRX").format(price_photo), parse_mode='html')
    else:
        markup_start = await kb.markup_start(call.message)
        await bot.send_message(call.message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html', reply_markup=markup_start)
        await state.finish()


@dp.callback_query_handler(text='add_song', state=say_hi.state)
async def add_song(call: types.callback_query):
    await call.message.answer(_("🎤 Надішліть пісню"))
    await say_hi.song.set()


@dp.message_handler(state=say_hi.song, content_types=types.ContentType.AUDIO)
async def say_hi_text(message: types.Message, state: FSMContext):
    audio_file_id = message.audio.file_id
    await state.update_data(audio=audio_file_id)
    data = await state.get_data()
    text = data.get('text')
    audio = data.get('audio')
    markup = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[[types.InlineKeyboardButton(text=_('📩 Надіслати повідомлення'), callback_data='next'), types.InlineKeyboardButton(text=_('❌ Відмінити'), callback_data='quit')]])
    await message.answer_audio(audio=audio, caption=text, reply_markup=markup)


@dp.callback_query_handler(text= 'next', state=say_hi.song)
async def say_hi_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    audio = data.get('audio')
    await bot.send_audio(message.from_user.id, audio=audio, caption=text)
    markup_succes_say_hi = await kb.markup_succes_say_hi(message)
    await bot.send_message(message.from_user.id, _("Ви дійсно хочете надіслати на перевірку повідомлення зверху?"), reply_markup=markup_succes_say_hi, parse_mode='html')


@dp.callback_query_handler(text='succes_say_hi', state=say_hi.song)
async def start(call: types.callback_query, state: FSMContext):
    user = await users.query.where(users.user_id == call.message.chat.id).gino.first()
    user_balance = user.bal_trx
    if user_balance >= price_audio:
        data = await state.get_data()
        text = data.get('text')
        audio = data.get('audio')
        try:
            await dp.bot.send_message(chat_id=5143177713, text=f'__________________________________________________________________'
                                                               f'\nРозсилка Музика\n\n<b><i>User_id</i> = {call.message.chat.id}</b>\n<b><i>LANGUAGE</i> = {user.user_language}</b>', parse_mode='html')
            await dp.bot.send_audio(chat_id=5143177713, audio=audio, caption=text, parse_mode='html')
            await dp.bot.send_message(chat_id=5143177713, text=f'<b><i>User_id</i> = {call.message.chat.id}</b>\n\nРозсилка Музика\n'
                                                               f'__________________________________________________________________', parse_mode='html')
            await db_quick_commands.register_say_hi(call.message.chat.id, text, False, True)
            session.commit()
            await sleep(0.33)
        except Exception:
            pass
        await state.finish()
        await users.update.values(bal_trx=users.bal_trx - price_audio).where(users.user_id == call.message.chat.id).gino.status()
        session.commit()
        markup_start = await kb.markup_start(call.message)
        await call.message.answer(_("✅ <b><i>Повідомлення надіслано в <u>модерацію</u></i></b>"), reply_markup=markup_start, parse_mode='html')
        await call.message.answer(_("ℹ З балансу знято <b><i>{}</i></b> TRX".format(price_audio)), parse_mode='html')
    else:
        markup_start = await kb.markup_start(call.message)
        await bot.send_message(call.message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html', reply_markup=markup_start)
        await state.finish()

@dp.callback_query_handler(text='add_song', state=say_hi.photo)
async def add_song(call: types.callback_query):
    await call.message.answer(_("🎤 Надішліть пісню"))
    await say_hi.song_plus_photo.set()


@dp.message_handler(state=say_hi.song_plus_photo, content_types=types.ContentType.AUDIO)
async def say_hi_photo(message: types.Message, state: FSMContext):
    audio_file_id = message.audio.file_id
    await state.update_data(audio=audio_file_id)
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    audio = data.get('audio')
    markup = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[[types.InlineKeyboardButton(text=_('📩 Надіслати повідомлення'), callback_data='next'), types.InlineKeyboardButton(text=_('❌ Відмінити'), callback_data='quit')]])
    await message.answer_photo(photo=photo, caption=text)
    await message.answer_audio(audio=audio, reply_markup=markup)


@dp.callback_query_handler(text= 'next', state=say_hi.song_plus_photo)
async def say_hi_text(message: types.Message, state: FSMContext):
    data = await state.get_data()
    text = data.get('text')
    photo = data.get('photo')
    audio = data.get('audio')
    await bot.send_photo(message.from_user.id, photo=photo, caption=text)
    await bot.send_audio(message.from_user.id, audio=audio)
    markup_succes_say_hi = await kb.markup_succes_say_hi(message)
    await bot.send_message(message.from_user.id, _("Ви дійсно хочете надіслати на перевірку повідомлення зверху?"), reply_markup=markup_succes_say_hi, parse_mode='html')


@dp.callback_query_handler(text='succes_say_hi', state=say_hi.song_plus_photo)
async def start(call: types.callback_query, state: FSMContext):
    user = await users.query.where(users.user_id == call.message.chat.id).gino.first()
    user_balance = user.bal_trx
    if user_balance >= price_all:
        data = await state.get_data()
        text = data.get('text')
        photo = data.get('photo')
        audio = data.get('audio')
        try:
            await dp.bot.send_message(chat_id=5143177713, text=f'__________________________________________________________________'
                                                               f'\nРозсилка Фото і Музика\n\n<b><i>User_id</i> = {call.message.chat.id}</b>\n<b><i>LANGUAGE</i> = {user.user_language}</b>', parse_mode='html')
            await dp.bot.send_photo(chat_id=5143177713, photo=photo, caption=text, parse_mode='html')
            await dp.bot.send_audio(chat_id=5143177713, audio=audio)
            await dp.bot.send_message(chat_id=5143177713, text=f'<b><i>User_id</i> = {call.message.chat.id}</b>\n\nРозсилка Фото і Музика\n'
                                                               f'__________________________________________________________________', parse_mode='html')
            await db_quick_commands.register_say_hi(call.message.chat.id, text, True, True)
            session.commit()
            await sleep(0.33)
        except Exception:
            pass
        await state.finish()
        await users.update.values(bal_trx=users.bal_trx - price_all).where(users.user_id == call.message.chat.id).gino.status()
        session.commit()
        markup_start = await kb.markup_start(call.message)
        await call.message.answer(_("✅ <b><i>Повідомлення надіслано в <u>модерацію</u></i></b>"), reply_markup=markup_start, parse_mode='html')
        await call.message.answer(_("ℹ З балансу знято <b><i>{}</i></b> TRX".format(price_all)), parse_mode='html')
    else:
        markup_start = await kb.markup_start(call.message)
        await bot.send_message(call.message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html', reply_markup=markup_start)
        await state.finish()


@dp.message_handler(state=say_hi.photo)
async def no_photo(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[[types.InlineKeyboardButton(text=_('❌ Відмінити'), callback_data='quit')]])
    await message.answer(_("📸 Надішліть фото"), reply_markup=markup)


@dp.message_handler(state=say_hi.song)
async def no_song(message: types.Message):
    markup = types.InlineKeyboardMarkup(row_width=2, inline_keyboard=[[types.InlineKeyboardButton(text=_('❌ Відмінити'), callback_data='quit')]])
    await message.answer(_("🎤 Надішліть пісню"), reply_markup=markup)


@dp.callback_query_handler(text='quit', state=[say_hi.text, say_hi.photo, say_hi.state, say_hi.song, say_hi.state_second, say_hi.song_plus_photo])
async def quit(call: types.callback_query, state: FSMContext):
    await state.finish()
    markup_start = await kb.markup_start(call.message)
    await call.message.answer(_("❌ Повідомлення відмінено"), reply_markup=markup_start)


#######################################################################################################################################
