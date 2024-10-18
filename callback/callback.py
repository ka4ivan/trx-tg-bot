import random
from datetime import datetime, timedelta
import asyncio

from asyncio import sleep

from aiogram import types
from aiogram.dispatcher import FSMContext
from db_api.schemas.achievement import Achievement_model as achivement
from db_api.schemas.crush_game import Crush_model
from db_api.schemas.paymants import Paymants_model
from db_api.schemas.say_hi import Say_model
from db_api.schemas.users import Users_model as users
from db_api.schemas.bonus import Bonus_model as Bonus
from db_api.schemas.promo_code import Promo_model as Promo
from db_api.schemas.promo_code_count import Promo_count_model as Promo_count
from db_api import db_quick_commands as db_commands
from config import dp, bot, _, storage
import keyboards as kb
from handlers import states
from handlers.states import say_hi, pay_operation, mailing
from language_middleware import get_lang
from settings import session, CHANNELS


async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer('One mess per second, pls')


async def check_sub_channels(channels, user_id):
    for channel in channels:
        chat_member = await bot.get_chat_member(chat_id=channel[1], user_id=user_id)
        if chat_member['status'] == 'left':
            return False
    return True


@dp.callback_query_handler(lambda c: c.data == 'work_admin_patreon_list')
async def process_work_admin_patreon_list(callback_query: types.CallbackQuery):
    try:
        patron_list = await db_commands.get_patreon_list()
        page_size = 20  # Количество патронов на странице
        if patron_list:
            total_pages = (len(patron_list) + page_size - 1) // page_size  # Общее количество страниц
            try:
                page_num = int(callback_query.message.text.split()[-1])  # Номер текущей страницы
            except (ValueError, IndexError):
                page_num = 1
            start_idx = (page_num - 1) * page_size
            end_idx = start_idx + page_size
            patron_list_text = ''
            for bal_trx, bal_usd, user_id, name in patron_list[start_idx:end_idx]:
                patron_list_text += f"➖ {user_id}, user_id: <code><b>{name}</b></code> \n💰 balance:  <b>{bal_trx}</b> TRX | <b>{bal_usd}</b> USDT\n\n"
            text = _("🅿 Список патронів (сторінка {} из {}): \n\n{}").format(page_num, total_pages, patron_list_text)
            inline_kb = types.InlineKeyboardMarkup(row_width=5)
            if page_num == 1:
                prev_page_cb = f'work_admin_patreon_list_page_{total_pages}' if total_pages > 1 else '#'
            else:
                prev_page_cb = f'work_admin_patreon_list_page_{page_num - 1}'
            prev_page_btn = types.InlineKeyboardButton('<<', callback_data=prev_page_cb)
            if page_num == total_pages:
                next_page_cb = 'work_admin_patreon_list_page_1' if total_pages > 1 else '#'
            else:
                next_page_cb = f'work_admin_patreon_list_page_{page_num + 1}'
            next_page_btn = types.InlineKeyboardButton('>>', callback_data=next_page_cb)
            inline_kb.row(prev_page_btn, next_page_btn)
            await bot.send_message(callback_query.from_user.id, text + _("🅿 Список патронів (сторінка {} из {})").format(page_num, total_pages), reply_markup=inline_kb)
        else:
            await bot.send_message(callback_query.from_user.id, _('🅿 Список патронів пустий.'))
    except:
        pass

@dp.callback_query_handler(lambda c: c.data.startswith('work_admin_patreon_list_page_'))
async def process_work_admin_patreon_list_page(callback_query: types.CallbackQuery):
    try:
        patron_list = await db_commands.get_patreon_list()
        page_size = 20  # Количество патронов на странице
        if patron_list:
            total_pages = (len(patron_list) + page_size - 1) // page_size  # Общее количество страниц
            try:
                page_num = int(callback_query.data.split('_')[-1])  # Номер текущей страницы
            except (ValueError, IndexError):
                page_num = 1
            start_idx = (page_num - 1) * page_size
            end_idx = start_idx + page_size
            patron_list_text = ''
            for bal_trx, bal_usd, user_id, name in patron_list[start_idx:end_idx]:
                patron_list_text += f"➖ {user_id}, user_id: <code><b>{name}</b></code> \n💰 balance:  <b>{bal_trx}</b> TRX | <b>{bal_usd}</b> USDT\n\n"
            text = _("🅿 Список патронів (сторінка {} из {}): \n\n{}").format(page_num, total_pages, patron_list_text)
            inline_kb = types.InlineKeyboardMarkup(row_width=5)
            if page_num == 1:
                prev_page_cb = f'work_admin_patreon_list_page_{total_pages}' if total_pages > 1 else '#'
            else:
                prev_page_cb = f'work_admin_patreon_list_page_{page_num - 1}'
            prev_page_btn = types.InlineKeyboardButton('<<', callback_data=prev_page_cb)
            if page_num == total_pages:
                next_page_cb = 'work_admin_patreon_list_page_1' if total_pages > 1 else '#'
            else:
                next_page_cb = f'work_admin_patreon_list_page_{page_num + 1}'
            next_page_btn = types.InlineKeyboardButton('>>', callback_data=next_page_cb)
            inline_kb.row(prev_page_btn, next_page_btn)
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=text + _("🅿 Список патронів (сторінка {} из {})").format(page_num, total_pages), reply_markup=inline_kb)
        else:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=_('🅿 Список патронів пустий.'))
    except:
        pass

@dp.callback_query_handler(lambda c: c.data == 'work_admin_ban_list')
async def process_work_admin_ban_list(callback_query: types.CallbackQuery):
    try:
        ban_list = await db_commands.get_ban_list()
        page_size = 20  # Количество патронов на странице
        if ban_list:
            total_pages = (len(ban_list) + page_size - 1) // page_size  # Общее количество страниц
            try:
                page_num = int(callback_query.message.text.split()[-1])  # Номер текущей страницы
            except (ValueError, IndexError):
                page_num = 1
            start_idx = (page_num - 1) * page_size
            end_idx = start_idx + page_size
            ban_list_text = ''
            for bal_trx, bal_usd, user_id, name in ban_list[start_idx:end_idx]:
                ban_list_text += f"➖ {user_id}, user_id: <code><b>{name}</b></code> \n💰 balance:  <b>{bal_trx}</b> TRX | <b>{bal_usd}</b> USDT\n\n"
            text = _("💀 Список забанених (сторінка {} из {}): \n\n{}").format(page_num, total_pages, ban_list_text)
            inline_kb = types.InlineKeyboardMarkup(row_width=5)
            if page_num == 1:
                prev_page_cb = f'work_admin_ban_list_page_{total_pages}' if total_pages > 1 else '#'
            else:
                prev_page_cb = f'work_admin_ban_list_page_{page_num - 1}'
            prev_page_btn = types.InlineKeyboardButton('<<', callback_data=prev_page_cb)
            if page_num == total_pages:
                next_page_cb = 'work_admin_ban_list_page_1' if total_pages > 1 else '#'
            else:
                next_page_cb = f'work_admin_ban_list_page_{page_num + 1}'
            next_page_btn = types.InlineKeyboardButton('>>', callback_data=next_page_cb)
            inline_kb.row(prev_page_btn, next_page_btn)
            await bot.send_message(callback_query.from_user.id, text + _("💀 Список забанених (сторінка {} из {})").format(page_num, total_pages), reply_markup=inline_kb)
        else:
            await bot.send_message(callback_query.from_user.id, _('💀 Список забанених пустий.'))
    except:
        pass

@dp.callback_query_handler(lambda c: c.data.startswith('work_admin_ban_list_page_'))
async def process_work_admin_ban_list_page(callback_query: types.CallbackQuery):
    try:
        ban_list = await db_commands.get_ban_list()
        page_size = 20  # Количество патронов на странице
        if ban_list:
            total_pages = (len(ban_list) + page_size - 1) // page_size  # Общее количество страниц
            try:
                page_num = int(callback_query.data.split('_')[-1])  # Номер текущей страницы
            except (ValueError, IndexError):
                page_num = 1
            start_idx = (page_num - 1) * page_size
            end_idx = start_idx + page_size
            ban_list_text = ''
            for bal_trx, bal_usd, user_id, name in ban_list[start_idx:end_idx]:
                ban_list_text += f"➖ {user_id}, user_id: <code><b>{name}</b></code> \n💰 balance:  <b>{bal_trx}</b> TRX | <b>{bal_usd}</b> USDT\n\n"
            text = _("💀 Список забанених (сторінка {} из {}): \n\n{}").format(page_num, total_pages, ban_list_text)
            inline_kb = types.InlineKeyboardMarkup(row_width=5)
            if page_num == 1:
                prev_page_cb = f'work_admin_ban_list_page_{total_pages}' if total_pages > 1 else '#'
            else:
                prev_page_cb = f'work_admin_ban_list_page_{page_num - 1}'
            prev_page_btn = types.InlineKeyboardButton('<<', callback_data=prev_page_cb)
            if page_num == total_pages:
                next_page_cb = 'work_admin_ban_list_page_1' if total_pages > 1 else '#'
            else:
                next_page_cb = f'work_admin_ban_list_page_{page_num + 1}'
            next_page_btn = types.InlineKeyboardButton('>>', callback_data=next_page_cb)
            inline_kb.row(prev_page_btn, next_page_btn)
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=text + _("💀 Список забанених (сторінка {} из {})").format(page_num, total_pages), reply_markup=inline_kb)
        else:
            await bot.edit_message_text(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=_('💀 Список забанених пустий.'))
    except:
        pass

@dp.callback_query_handler()
@dp.throttled(anti_flood, rate=1)
async def callback_guess(call: types.callback_query):

    ban_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
    ban = ban_db.ban
    if ban == 0:

        if call.data == 'sub_channel_done':
            await bot.delete_message(call.message.chat.id, call.message.message_id)
            if await check_sub_channels(CHANNELS, call.message.chat.id):
                await bot.send_message(call.message.chat.id, _("✅ Виконано! Ви підписались на канал"))
            else:
                markup_channels = await kb.markup_channels(call.message)
                await bot.send_message(call.message.chat.id, _("ℹ Для отримання доступу до даної функції, потрібно підписатись на нашу групу в телеграм 💳\n\n👇 Силка тут 👇"), reply_markup=markup_channels)

        if call.data == 'change_language':
            await bot.send_message(call.message.chat.id, '🇺🇦 Оберіть мову інтерфейсу\n\n🇷🇺 Выберите язык интерфейса\n\n🇬🇧 Choose the interface language', reply_markup=kb.markup_change_language, parse_mode='html')

        if call.data == "ua_lang":
            await users.update.values(user_language='uk').where(users.user_id == call.message.chat.id).gino.status()
            session.commit()
            markup_start = await kb.markup_start(call.message)
            await bot.send_message(call.message.chat.id, _('🇺🇦 Вітаю\n\nВи обрали українську мову\n\nМову можна міняти в будь-який момент у розділі "🆘 Тех. Підтримка"'), reply_markup=markup_start, parse_mode='html')
            await call.message.answer(_('🔝 <b>Головне Меню</b>', locale='uk'), parse_mode='html')

        if call.data == "ru_lang":
            await users.update.values(user_language='ru').where(users.user_id == call.message.chat.id).gino.status()
            session.commit()
            markup_start = await kb.markup_start(call.message)
            await bot.send_message(call.message.chat.id, _('🇷🇺 Поздравляю\n\nУ вас русский язык интерфейса\n\nЯзык можно менять в любой момент в разделе "🆘 Тех. Поддержка"'), reply_markup=markup_start, parse_mode='html')
            await call.message.answer(_('🔝 <b>Головне Меню</b>', locale='ru'), parse_mode='html')

        if call.data == "en_lang":
            await users.update.values(user_language='en').where(users.user_id == call.message.chat.id).gino.status()
            session.commit()
            markup_start = await kb.markup_start(call.message)
            await bot.send_message(call.message.chat.id, _('🇬🇧 Congratulations\n\n You have chosen English\n\n You can change the language at any time in the section "🆘 Support"'), reply_markup=markup_start, parse_mode='html')
            await call.message.answer(_('🔝 <b>Головне Меню</b>', locale='en'), parse_mode='html')

        if call.data == 'day_bon_cab':
            if (not await db_commands.select_user_bonus(call.message.chat.id)):
                await bot.send_message(call.message.chat.id, _("ℹ В мережі було здійснено оновлення. Натисніть на кнопку: /start"))
            else:
                access = False
                curr_datetime = datetime.now()
                bonus = await Bonus.query.where(Bonus.user_id == call.message.chat.id).gino.first()
                bonus_daily_time = bonus.daily_date

                if (curr_datetime - bonus_daily_time).total_seconds() > 86400:  # 86400 секунд = 24 часа
                    access = True
                    photo = open('img/bonus_img.jpg', 'rb')
                    user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                    user_level = user_db.user_level
                    if (user_level == 1):
                        await call.answer(_("Вам нараховано 1 TRX"))
                        await bot.send_photo(call.message.chat.id, photo, caption=_("🤑 Вітаю! Тобі нараховано 1 TRX, отримати наступний бонус можеш через день!"), parse_mode='html')
                        await db_commands.give_bonus_daily_lvl_1(call.message.chat.id)
                        await db_commands.update_bonus_daily(call.message.chat.id)
                    elif (user_level == 2):
                        await call.answer(_("Вам нараховано 1.05 TRX"))
                        await bot.send_photo(call.message.chat.id, photo, caption=_("🤑 Вітаю! Тобі нараховано 1.05 TRX, отримати наступний бонус можеш через день!"), parse_mode='html')
                        await db_commands.give_bonus_daily_lvl_2(call.message.chat.id)
                        await db_commands.update_bonus_daily(call.message.chat.id)
                    elif (user_level == 3):
                        await call.answer(_("Вам нараховано 1.15 TRX"))
                        await bot.send_photo(call.message.chat.id, photo, caption=_("🤑 Вітаю! Тобі нараховано 1.15 TRX, отримати наступний бонус можеш через день!"), parse_mode='html')
                        await db_commands.give_bonus_daily_lvl_3(call.message.chat.id)
                        await db_commands.update_bonus_daily(call.message.chat.id)
                    else:
                        await call.message.answer(_("💢 Помилка! Зверніться у тех. підтримку"))
                else:
                    left_time = timedelta(hours=23, minutes=59, seconds=59) - (curr_datetime - bonus_daily_time)
                    photo = open('img/bonus_img.jpg', 'rb')
                    await call.answer(_("Стане доступним через {}").format(str(left_time)[:8]))
                    await bot.send_photo(call.message.chat.id, photo, caption=_("Ви зможете отримати денний бонус через {}").format(str(left_time)[:8]), parse_mode='html')
                return access

        if call.data == 'wek_bon_cab':
            if await check_sub_channels(CHANNELS, call.message.chat.id):
                if (not await db_commands.select_user_bonus(call.message.chat.id)):
                    await bot.send_message(call.message.chat.id, _("ℹ В мережі було здійснено оновлення. Натисніть на кнопку: /start"))
                else:
                    access = False
                    curr_datetime = datetime.now()
                    bonus = await Bonus.query.where(Bonus.user_id == call.message.chat.id).gino.first()
                    bonus_weekly_time = bonus.week_date
                    if (curr_datetime - bonus_weekly_time).total_seconds() > 604800:  # 86400 секунд = 24 часа
                        access = True
                        photo = open('img/bonus_img.jpg', 'rb')
                        user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                        user_level = user_db.user_level
                        if (user_level == 3):
                            await call.answer(_("Вам нараховано 2.5 TRX"))
                            await bot.send_photo(call.message.chat.id, photo, caption=_("🤑 Вітаю! Тобі нараховано 2.5 TRX, отримати наступний бонус можеш через тиждень!"), parse_mode='html')
                            await db_commands.give_bonus_week_lvl_3(call.message.chat.id)
                            await db_commands.update_bonus_week(call.message.chat.id)
                        else:
                            await call.answer(_("Вам нараховано 1.75 TRX"))
                            await bot.send_photo(call.message.chat.id, photo, caption=_("🤑 Вітаю! Тобі нараховано 1.75 TRX, отримати наступний бонус можеш через тиждень!"))
                            await db_commands.give_bonus_week(call.message.chat.id)
                            await db_commands.update_bonus_week(call.message.chat.id)
                    else:
                        left_time = timedelta(days=6, hours=23, minutes=59, seconds=59) - (curr_datetime - bonus_weekly_time)
                        photo = open('img/bonus_img.jpg', 'rb')
                        await call.answer(_("Стане доступним через {}").format(str(left_time)[:16]))
                        await bot.send_photo(call.message.chat.id, photo, caption=_("Ви зможете отримати тижневий бонус через {}").format(str(left_time)[:16]), parse_mode='html')
                        return access
            else:
                markup_channels = await kb.markup_channels(call.message)
                await bot.send_message(call.message.chat.id, _("ℹ Для отримання доступу до даної функції, потрібно підписатись на нашу групу в телеграм 💳\n\n👇 Силка тут 👇"), reply_markup=markup_channels)

        if call.data == 'promo_bon_cab':
            if await check_sub_channels(CHANNELS, call.message.chat.id):
                await states.promo_code.type_promo.set()
                markup_cancel_promo = await kb.markup_cancel_promo(call.message)
                await bot.send_message(call.message.chat.id, _("✍ Введіть промокод:"), reply_markup=markup_cancel_promo)

                @dp.message_handler(state=states.promo_code.type_promo)
                @dp.throttled(anti_flood, rate=1)
                async def promo_text(message: types.Message, state: FSMContext):
                    try:
                        first_promo = 'Ocgt3Ic21'
                        second_promo = 'msv7D2s4'
                        user_id = message.from_user.id
                        if not await db_commands.select_user_promo_code(first_promo, user_id):
                            db_commands.register_user_promo(message, first_promo)
                            session.commit()
                        if not await db_commands.select_user_promo_code(second_promo, user_id):
                            db_commands.register_user_promo(message, second_promo)
                            session.commit()
                        async with state.proxy() as data:
                            data['type_promo'] = message.text

                        if data['type_promo'] == first_promo or data['type_promo'] == second_promo:
                            if not await db_commands.select_user_promo_code_count(data['type_promo']):
                                db_commands.register_promo_count(data['type_promo'])
                            promo_code_db = await Promo.query.where((Promo.user_id == message.from_user.id) & (Promo.promo_code == data['type_promo'])).gino.first()
                            c_promo_code = promo_code_db.c_promo_code
                            if c_promo_code != 1:
                                promo_code_count_db = await Promo_count.query.where(Promo_count.promo_code == data['type_promo']).gino.first()
                                count_promo_code = promo_code_count_db.count_promo_code
                                if count_promo_code < 250:
                                    markup_start = await kb.markup_start(message)
                                    await bot.send_message(message.from_user.id, _('✅ Ви активували промокод - <b>"{}"</b>\n\nℹ Ще більше промокодів в нашому <b><i>патреоні</i></b>: patreon.com/TelegramTRXBot').format(data['type_promo']), reply_markup=markup_start)
                                    await bot.send_message(message.from_user.id, _("🤑 Вам нараховано 0.5 TRX"))
                                    await Promo.update.values(c_promo_code=1).where((Promo.user_id == message.from_user.id) & (Promo.promo_code == message.text)).gino.status()
                                    await users.update.values(bal_trx=users.bal_trx + 0.5).where(users.user_id == message.from_user.id).gino.status()
                                    await Promo_count.update.values(count_promo_code=count_promo_code + 1).where(Promo_count.promo_code == data['type_promo']).gino.status()
                                    session.commit()
                                    await state.finish()
                                else:
                                    markup_cancel_promo = await kb.markup_cancel_promo(message)
                                    await bot.send_message(message.from_user.id, _('❌ Промокоду " <u><b>{}</b></u> " не існує, або вся його кількість використана ❗\n\nℹ Ще більше промокодів в нашому <b><i>патреоні</i></b>: patreon.com/TelegramTRXBot\n\nВи можете вийти із введення промокоду: /cancel_promo_code').format(message.text),parse_mode='html', reply_markup=markup_cancel_promo)
                            else:
                                markup_start = await kb.markup_start(message)
                                await bot.send_message(message.from_user.id, _('⛔ Промокод можна використовувати тільки один раз ❗\n\nℹ Ще більше промокодів в нашому <b><i>патреоні</i></b>: patreon.com/TelegramTRXBot'), reply_markup=markup_start)
                                await state.finish()
                        elif message.text == '🚫 Повернутись назад 🚫' or message.text == '🚫 Вернуться назад 🚫' or message.text == '🚫 Go back 🚫':
                            await state.finish()
                            markup_start = await kb.markup_start(message)
                            await message.answer(_("🔝 <b>Головне меню</b>"), parse_mode='HTML', reply_markup=markup_start)
                        else:
                            markup_cancel_promo = await kb.markup_cancel_promo(message)
                            await bot.send_message(message.from_user.id, _('❌ Промокоду " <u><b>{}</b></u> " не існує, або вся його кількість використана ❗\n\nℹ Ще більше промокодів в нашому <b><i>патреоні</i></b>: patreon.com/TelegramTRXBot\n\nВи можете вийти із введення промокоду: /cancel_promo_code').format(message.text), parse_mode='html', reply_markup=markup_cancel_promo)
                    except:
                        markup_start = await kb.markup_start(message)
                        await bot.send_message(message.chat.id, _("❌ Промокод введено некоректно ❗"), parse_mode='html', reply_markup=markup_start)
                        await bot.send_message(message.chat.id, _("❌ Ви повернулись у головне меню ‼"), parse_mode='html')
                        await state.finish()
            else:
                markup_channels = await kb.markup_channels(call.message)
                await bot.send_message(call.message.chat.id, _("ℹ Для отримання доступу до даної функції, потрібно підписатись на нашу групу в телеграм 💳\n\n👇 Силка тут 👇"), reply_markup=markup_channels)

        if call.data == 'say_hi_inline':
            await call.message.answer(_("✍ Введіть текст повідомлення: \n\n(B дужках напишіть як хочете надіслати повідомлення, анонімно, або повністю відкрито, нд: <i>вкажіть моє ім'я та юзернейм, але не вказуйте мій айді</i>)"), reply_markup=types.ReplyKeyboardRemove(), parse_mode='html')
            await say_hi.text.set()

        if call.data == 'del_trx_cab':
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("📌 <b>Введіть суму яку хочете вивести</b>\n💳 Ваш баланс: {} trx \n\nЯкщо у вас виникли проблеми, або при будь-яких питаннях звертайтесь до нашого менеджера: @Christooo1").format(bal_trx), reply_markup=kb.markup_select_del_trx, parse_mode='html')
            await bot.send_message(call.message.chat.id, _("💶💵💴💷 Cума виводу: "), parse_mode='html')
            await pay_operation.del_trx.set()

        if call.data == 'add_trx_cab':
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("📌 <b>Введіть суму поповнення</b>\n💳 Ваш баланс: {} trx\n\n📌 Потрібно надіслати рівно ту суму, яку ви вказали, на дану адресу: <code>TCYB6trdKVeEk6SDdcpDHyNASgQudhpirT</code> \n\n\nЯкщо у вас виникли проблеми, або при будь-яких питаннях звертайтесь до нашого менеджера: @Christooo1").format(bal_trx), reply_markup=kb.markup_select_add_trx, parse_mode='html')
            await bot.send_message(call.message.chat.id, _("💶💵💴💷 Cума поповнення: "), parse_mode='html')
            await pay_operation.add_trx.set()

        if call.data == 'add_usd_cab':
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_usd = user_db.bal_usd
            await bot.send_message(call.message.chat.id, _("📌 <b>Введіть суму поповнення</b>\n💳 Ваш баланс: {} USDT\n\n📌 Потрібно надіслати рівно ту суму, яку ви вказали, на дану адресу: <code>TCYB6trdKVeEk6SDdcpDHyNASgQudhpirT</code>\n\n\nЯкщо у вас виникли проблеми, або при будь-яких питаннях звертайтесь до нашого менеджера: @Christooo1").format(bal_usd), reply_markup=kb.markup_select_add_usdt, parse_mode='html')
            await bot.send_message(call.message.chat.id, _("💶💵💴💷 Cума поповнення: "), parse_mode='html')
            await pay_operation.add_usd.set()

        if call.data == 'accept_cab':
            await call.answer(_("✅ Підтверджено"))

        if call.data == 'what_is_lvl':
            await bot.send_message(call.message.chat.id, _('📯 <b>Рівень аккаунту</b> - це показник ваших досягнень у боті. При вищому рівні, вашому аккаунту надаються більші привілегії.\n\nЩо дають рівні аккаунту:\n\n🥉 <b>1 Рівень</b>:\nЩоденний бонус становить - 1 TRX\n\n🥈 <b>2 Рівень</b>:\nЩоденний бонус становить - 1.05 TRX\n\n🥇 <b>3 Рівень</b>:\nЩоденний бонус становить - 1.15 TRX\nЩотижневий бонус становить - 2.5 TRX\n\n‼ Щоб аккаунт перевівся на слідуючий рівень, необхідно натиснути на кнопку "🖱 Перевірити виконання вимог" в особистому кабінеті\n\n\nЯк здобути рівні аккаунту?\n\n➖ 1 Рівень вимоги отримання:\nНадається після проходження реєстрації\n\n➖ 2 Рівень вимоги отримання:\n- Ігор у гру "50/50": 50 раз\n- Ігор у гру "Кейси": 150 раз\n- Кількість рефералів першої лінії має становити: 7\n- Загальна кількість рефералів: 10\n\n➖ 3 Рівень вимоги отримання:\n- Ігор у гру "Слоти": 185 раз\n- Ігор у гру "Вгадати число": 225 раз\n- Виграш в грі "Вгадати число" із 100 числами: 2 рази\n- Кількість рефералів першої лінії має становити: 22\n- Загальна кількість рефералів: 30\n- Поповнення балансу одним платежем на суму: 500 TRX (або отримання 100 щоденних і 4 тижневих бонусів)'), parse_mode='html')


        if call.data == 'check_lvl':
            f = int(await db_commands.count_first_ref(call.message.chat.id))
            a = int(await db_commands.count_first_ref(call.message.chat.id) + await db_commands.count_second_ref(call.message.chat.id) + await db_commands.count_third_ref(call.message.chat.id))

            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            user_level = user_db.user_level

            achievement = await achivement.query.where(achivement.user_id == call.message.chat.id).gino.first()
            game_fifty = achievement.game_fifty
            game_case = achievement.game_case
            game_slot = achievement.game_slot
            game_num = achievement.game_num
            pay_trx = achievement.pay_trx
            daily_bonus = achievement.daily_bonus
            week_bonus = achievement.week_bonus
            game_num_win_hun = achievement.game_num_win_hun
            try:
                if (user_level == 1):
                    fifty = _('➖ Ігор у гру "50/50"')
                    if game_fifty >= 50:
                        fifty = _('✅ Ігор у гру "50/50"')
                    case = _('➖ Ігор у гру "Кейси"')
                    if game_case >= 150:
                        case = _('✅ Ігор у гру "Кейси"')
                    f_ref = _('➖ Кількість рефералів першої лінії')
                    if await db_commands.count_first_ref(call.message.chat.id) >= 7:
                        f_ref = _('✅ Кількість рефералів першої лінії')
                    a_ref = _('➖ Загальна кількість рефералів')
                    if (await db_commands.count_first_ref(call.message.chat.id) + await db_commands.count_second_ref(call.message.chat.id) + await db_commands.count_third_ref(call.message.chat.id)) >= 10:
                        a_ref = _('✅ Загальна кількість рефералів')
                    await bot.send_message(call.message.chat.id, _('🪪 У вас <b><i>Перший рівень</i></b> аккаунту 🎫\n\n💢 Завдання для Другого рівня:\n\n{}: {}/50\n{}: {}/150\n{}: {}/7\n{}: {}/10\n\nЯкщо виникли питання, або ви впевнені що виконали вимоги, зверніться у тех. підтримку').format(fifty, game_fifty, case, game_case, f_ref, await db_commands.count_first_ref(call.message.chat.id), a_ref, await db_commands.count_first_ref(call.message.chat.id) + await db_commands.count_second_ref(call.message.chat.id) + await db_commands.count_third_ref(call.message.chat.id)), parse_mode='html')
                if (f >= 7 and a >= 10 and game_fifty >= 50 and game_case >= 150) and user_level == 1:
                    if user_level != 2:
                        await bot.send_message(call.message.chat.id, _('🪅 Вітаю!! Ви перейшли на <b><i>Другий рівень</i></b> аккаунту ⚔'), parse_mode='html')
                        await db_commands.give_level_2(call.message.chat.id)
                    else:
                        pass
                if user_level == 2:
                    spin = _('➖ Ігор у гру "Слоти"')
                    if game_slot >= 185:
                        spin = _('✅ Ігор у гру "Слоти"')
                    num = _('➖ Ігор у гру "Вгадати число"')
                    if game_num >= 225:
                        num = _('✅ Ігор у гру "Вгадати число"')
                    num_hun = _('➖ Виграш в грі "Вгадати число" із 100 числами')
                    if game_num_win_hun >= 2:
                        num_hun = _('✅ Виграш в грі "Вгадати число" із 100 числами')
                    f_ref = _('➖ Кількість рефералів першої лінії')
                    if await db_commands.count_first_ref(call.message.chat.id) >= 22:
                        f_ref = _('✅ Кількість рефералів першої лінії')
                    a_ref = _('➖ Загальна кількість рефералів')
                    if (await db_commands.count_first_ref(call.message.chat.id) + await db_commands.count_second_ref(call.message.chat.id) + await db_commands.count_third_ref(call.message.chat.id)) >= 30:
                        a_ref = _('✅ Загальна кількість рефералів')
                    pay_trx_to_lvl = _('➖ Поповнення балансу одним платежем на суму')
                    if pay_trx >= 500 or daily_bonus >= 150 and week_bonus >= 6:
                        pay_trx_to_lvl = _('✅ Поповнення балансу одним платежем на суму')
                    await bot.send_message(call.message.chat.id, _('🪪 У вас <b><i>Другий рівень</i></b> аккаунту 🎫\n\n💢 Завдання для Третього рівня:\n\n{}: {}/185\n{}: {}/225\n{}: {}/2\n{}: {}/22\n{}: {}/30\n{}: {}/500 \nабо отримання 150 щоденних і 6 тижневих бонусів: \n{}/150 і {}/6\n\nЯкщо виникли питання, або ви впевнені що виконали вимоги, зверніться у тех. підтримку').format(spin, game_slot, num, game_num, num_hun, game_num_win_hun, f_ref, await db_commands.count_first_ref(call.message.chat.id), a_ref, await db_commands.count_first_ref(call.message.chat.id) + await db_commands.count_second_ref(call.message.chat.id) + await db_commands.count_third_ref(call.message.chat.id), pay_trx_to_lvl, pay_trx, daily_bonus, week_bonus), parse_mode='html')
                if (f >= 22 and a >= 30 and game_slot >= 185 and game_num >= 225 and game_num_win_hun >= 2 and user_level == 2):
                    if pay_trx >= 500 or daily_bonus >= 150 and week_bonus >= 6:
                        if user_level != 3:
                            await bot.send_message(call.message.chat.id, _('🪅 Вітаю!! Ви перейшли на <b><i>Третій рівень</i></b> аккаунту ⚔'), parse_mode='html')
                            await db_commands.give_level_3(call.message.chat.id)
                        else:
                            pass
                if user_level == 3:
                    await bot.send_message(call.message.chat.id, _('🪪 У вас <b><i>Третій рівень</i></b> аккаунту 🎫\n\n💫 На даний момент у вас МАКСИМАЛЬНИЙ рівень аккаунту\n\nЯкщо виникли питання, зверніться у тех. підтримку'), parse_mode='html')
            except:
                await bot.send_message(call.message.chat.id, _('💢 Помилка! Зверніться у тех. підтримку'), parse_mode='html')



        if call.data == 'history_pay_cab':
            within_als = {
                "day": ('today', 'day', 'СЬОГОДНІ', _('ДЕНЬ')),
                "month": ('month', _("МІСЯЦЬ")),
                "year": ('year', _("РІК")),
            }
            within = 'month'
            await Paymants_model.delete.where(Paymants_model.adress == '/cancel').gino.status()
            session.commit()
            records = await db_commands.get_records(call.message.chat.id, within)
            if (len(records)):
                answer = (_("📖 Істория транзакцій за <b>{}</b>.\n\nТут будуть відображатись всі ваші операції, такі як поповнення USDT, поповнення TRX та вивід TRX за вибраний вами проміжок часу\n\n\n").format(within_als[within][-1]))
                for r in records:
                    answer += ("<b>" + ("➕ " if not r.del_trx else "➖ ") + "</b>")
                    if r.add_usd != 0:
                        answer += f"<b><u><i>{r.add_usd} USDT</i></u></b>"
                    if r.add_trx != 0:
                        answer += f"<b><u><i>{r.add_trx} TRX</i></u></b>"
                    if r.del_trx != 0:
                        answer += f"<b><u><i>{r.del_trx} TRX</i></u></b>"
                    answer += f"\n🕐 {r.date}  "
                    answer += ("<b>" + (
                        _("| Поповнення") if not r.del_trx else
                        _("|  Вивід")) + "</b>\n")
                    if r.acces == 0:
                        answer += _("<b>❌ Не виконано</b>\n\n")
                    elif r.acces == 1:
                        answer += _("<b>✅ Виконано</b>\n\n")
                    else:
                        answer += _("<b>💢 Помилка виконання</b>\n\n")
                markup_pay_history = await kb.markup_pay_history(call.message)
                await call.message.answer(answer, parse_mode='html', reply_markup=markup_pay_history)
            else:
                markup_pay_history = await kb.markup_pay_history(call.message)
                await call.message.answer(_("😯 Записів за {} не знайдено! 🔕").format(within_als[within][-1]), reply_markup=markup_pay_history)

        if call.data == 'pay_history_day_cab':
            within_als = {
                "day": ('today', 'day', 'СЬОГОДНІ', _('ДЕНЬ')),
                "month": ('month', _("МІСЯЦЬ")),
                "year": ('year', _("РІК")),
            }
            within = 'day'
            await Paymants_model.delete.where(Paymants_model.adress == '/cancel').gino.status()
            session.commit()
            records = await db_commands.get_records(call.message.chat.id, within)
            if (len(records)):
                answer = (_("📖 Істория транзакцій за <b>{}</b>.\n\nТут будуть відображатись всі ваші операції, такі як поповнення USDT, поповнення TRX та вивід TRX за вибраний вами проміжок часу\n\n\n").format(
                    within_als[within][-1]))
                for r in records:
                    answer += ("<b>" + ("➕ " if not r.del_trx else "➖ ") + "</b>")
                    if r.add_usd != 0:
                        answer += f"<b><u><i>{r.add_usd} USDT</i></u></b>"
                    if r.add_trx != 0:
                        answer += f"<b><u><i>{r.add_trx} TRX</i></u></b>"
                    if r.del_trx != 0:
                        answer += f"<b><u><i>{r.del_trx} TRX</i></u></b>"
                    answer += f"\n🕐 {r.date}  "
                    answer += ("<b>" + (
                        _("| Поповнення") if not r.del_trx else
                        _("|  Вивід")) + "</b>\n")
                    if r.acces == 0:
                        answer += _("<b>❌ Не виконано</b>\n\n")
                    elif r.acces == 1:
                        answer += _("<b>✅ Виконано</b>\n\n")
                    else:
                        answer += _("<b>💢 Помилка виконання</b>\n\n")
                markup_pay_history = await kb.markup_pay_history(call.message)
                try:
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=markup_pay_history)
                except:
                    pass
            else:
                markup_pay_history = await kb.markup_pay_history(call.message)
                try:
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=_("😯 Записів за {} не знайдено! 🔕").format(within_als[within][-1]), reply_markup=markup_pay_history)
                except:
                    pass

        if call.data == 'pay_history_month_cab':
            within_als = {
                "day": ('today', 'day', 'СЬОГОДНІ', _('ДЕНЬ')),
                "month": ('month', _("МІСЯЦЬ")),
                "year": ('year', _("РІК")),
            }
            within = 'month'
            await Paymants_model.delete.where(Paymants_model.adress == '/cancel').gino.status()
            session.commit()
            records = await db_commands.get_records(call.message.chat.id, within)
            if (len(records)):
                answer = (_("📖 Істория транзакцій за <b>{}</b>.\n\nТут будуть відображатись всі ваші операції, такі як поповнення USDT, поповнення TRX та вивід TRX за вибраний вами проміжок часу\n\n\n").format(
                    within_als[within][-1]))
                for r in records:
                    answer += ("<b>" + ("➕ " if not r.del_trx else "➖ ") + "</b>")
                    if r.add_usd != 0:
                        answer += f"<b><u><i>{r.add_usd} USDT</i></u></b>"
                    if r.add_trx != 0:
                        answer += f"<b><u><i>{r.add_trx} TRX</i></u></b>"
                    if r.del_trx != 0:
                        answer += f"<b><u><i>{r.del_trx} TRX</i></u></b>"
                    answer += f"\n🕐 {r.date}  "
                    answer += ("<b>" + (
                        _("| Поповнення") if not r.del_trx else
                        _("|  Вивід")) + "</b>\n")
                    if r.acces == 0:
                        answer += _("<b>❌ Не виконано</b>\n\n")
                    elif r.acces == 1:
                        answer += _("<b>✅ Виконано</b>\n\n")
                    else:
                        answer += _("<b>💢 Помилка виконання</b>\n\n")
                markup_pay_history = await kb.markup_pay_history(call.message)
                try:
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=markup_pay_history)
                except:
                    pass
            else:
                markup_pay_history = await kb.markup_pay_history(call.message)
                try:
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=_("😯 Записів за {} не знайдено! 🔕").format(within_als[within][-1]), reply_markup=markup_pay_history)
                except:
                    pass

        if call.data == 'pay_history_year_cab':
            within_als = {
                "day": ('today', 'day', 'СЬОГОДНІ', _('ДЕНЬ')),
                "month": ('month', _("МІСЯЦЬ")),
                "year": ('year', _("РІК")),
            }
            within = 'year'
            await Paymants_model.delete.where(Paymants_model.adress == '/cancel').gino.status()
            session.commit()
            records = await db_commands.get_records(call.message.chat.id, within)
            if (len(records)):
                answer = (_("📖 Істория транзакцій за <b>{}</b>.\n\nТут будуть відображатись всі ваші операції, такі як поповнення USDT, поповнення TRX та вивід TRX за вибраний вами проміжок часу\n\n\n").format(
                    within_als[within][-1]))
                for r in records:
                    answer += ("<b>" + ("➕ " if not r.del_trx else "➖ ") + "</b>")
                    if r.add_usd != 0:
                        answer += f"<b><u><i>{r.add_usd} USDT</i></u></b>"
                    if r.add_trx != 0:
                        answer += f"<b><u><i>{r.add_trx} TRX</i></u></b>"
                    if r.del_trx != 0:
                        answer += f"<b><u><i>{r.del_trx} TRX</i></u></b>"
                    answer += f"\n🕐 {r.date}  "
                    answer += ("<b>" + (
                        _("| Поповнення") if not r.del_trx else
                        _("|  Вивід")) + "</b>\n")
                    if r.acces == 0:
                        answer += _("<b>❌ Не виконано</b>\n\n")
                    elif r.acces == 1:
                        answer += _("<b>✅ Виконано</b>\n\n")
                    else:
                        answer += _("<b>💢 Помилка виконання</b>\n\n")
                markup_pay_history = await kb.markup_pay_history(call.message)
                try:
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=answer, reply_markup=markup_pay_history)
                except:
                    pass
            else:
                markup_pay_history = await kb.markup_pay_history(call.message)
                try:
                    await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=_("😯 Записів за {} не знайдено! 🔕").format(within_als[within][-1]), reply_markup=markup_pay_history)
                except:
                    pass

        if call.data == 'again_guess_five':
            await states.guess_number.bet_five.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

        if call.data == 'again_guess_same_bet_five':
            await states.guess_number.random_number_five.set()
            num_game = 5
            await bot.send_message(call.message.chat.id, _("Загадано число від 1 до {}. Спробуй вгадати").format(num_game), reply_markup=kb.markup_select_rand_num_five)

        if call.data == 'again_guess_ten':
            await states.guess_number.bet_ten.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

        if call.data == 'again_guess_same_bet_ten':
            await states.guess_number.random_number_ten.set()
            num_game = 10
            await bot.send_message(call.message.chat.id, _("Загадано число від 1 до {}. Спробуй вгадати").format(num_game), reply_markup=kb.markup_select_rand_num_ten)

        if call.data == 'again_guess_hun':
            await states.guess_number.bet_hun.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

        if call.data == 'again_guess_same_bet_hun':
            await states.guess_number.random_number_hun.set()
            num_game = 100
            await bot.send_message(call.message.chat.id, _("Загадано число від 1 до {}. Спробуй вгадати").format(num_game), reply_markup=kb.markup_select_rand_num_hun)

        if call.data == 'again_fifty_two':
            await states.fifty_fifty.bet_two.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

        if call.data == 'again_same_bet_fifty_two':
            await states.fifty_fifty.random_number_two.set()
            num_game = 2
            await bot.send_message(call.message.chat.id, _("Загадано число від 1 до {}. Спробуй вгадати").format(num_game), reply_markup=kb.markup_select_fifty_two)

        if call.data == 'again_fifty_four':
                await states.fifty_fifty.bet_four.set()
                user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                bal_trx = user_db.bal_trx
                await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

        if call.data == 'again_same_bet_fifty_four':
            await states.fifty_fifty.random_number_four.set()
            num_game = 4
            await bot.send_message(call.message.chat.id, _("Загадано число від 1 до {}. Спробуй вгадати").format(num_game), reply_markup=kb.markup_select_fifty_four)

        if call.data == 'again_dice_classic':
            await states.dice.bet_classic.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

        if call.data == 'again_same_bet_dice_classic':
            await states.dice.random_number_classic.set()
            await bot.send_message(call.message.chat.id, _("Кубик готовий до гри, оберіть ваше значення:"), reply_markup=kb.markup_select_dice_classic)

        if call.data == 'again_dice_under':
            await states.dice.bet_under.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

        if call.data == 'again_same_bet_dice_under':
            await states.dice.random_number_under.set()
            markup_select_dice_under = await kb.markup_select_dice_under(call.message)
            await bot.send_message(call.message.chat.id, _("Кубик готовий до гри, оберіть ваше значення:"), reply_markup=markup_select_dice_under)

        if call.data == 'again_br_case':
            await states.cases.case_br_buy.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            markup_accept_cases = await kb.markup_accept_cases(call.message)
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=markup_accept_cases, parse_mode='html')

        if call.data == 'again_si_case':
            await states.cases.case_si_buy.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            markup_accept_cases = await kb.markup_accept_cases(call.message)
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=markup_accept_cases, parse_mode='html')

        if call.data == 'again_go_case':
            await states.cases.case_go_buy.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            markup_accept_cases = await kb.markup_accept_cases(call.message)
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=markup_accept_cases, parse_mode='html')

        if call.data == 'again_miner_three':
            await states.miner.bet_three.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

        if call.data == 'again_same_bet_miner_three':
            await states.miner.random_number_three.set()
            random.shuffle(kb.list_buts)
            markup = types.InlineKeyboardMarkup()
            for text, data in kb.list_buts:
                markup.insert(types.InlineKeyboardButton(text=text, callback_data=data))
            await bot.send_message(call.message.chat.id, _("Де немає бомби?"), reply_markup=markup)

        if call.data == 'again_miner_five':
            await states.miner.bet_five.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

        if call.data == 'again_same_bet_miner_five':
            await states.miner.random_number_five.set()
            random.shuffle(kb.list_buts)
            markup = types.InlineKeyboardMarkup()
            for text, data in kb.list_buts:
                markup.insert(types.InlineKeyboardButton(text=text, callback_data=data))
            await bot.send_message(call.message.chat.id, _("Де немає бомби?"), reply_markup=markup)

        if call.data == 'again_miner_seven':
            await states.miner.bet_seven.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

        if call.data == 'again_same_bet_miner_seven':
            await states.miner.random_number_seven.set()
            random.shuffle(kb.list_buts)
            markup = types.InlineKeyboardMarkup()
            for text, data in kb.list_buts:
                markup.insert(types.InlineKeyboardButton(text=text, callback_data=data))
            await bot.send_message(call.message.chat.id, _("Де немає бомби?"), reply_markup=markup)

        if call.data == 'again_slot':
            await states.spin.bet_spin.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

        if call.data == 'again_same_bet_slot':
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            betting = user_db.bet
            bal_trx = user_db.bal_trx
            if betting <= bal_trx:
                await users.update.values(bet=betting).where(users.user_id == call.message.chat.id).gino.status()
                await bot.send_message(call.message.chat.id, _("Автомат готовий до гри"))
                markup_games = await kb.markup_games(call.message)
                data = await call.message.answer_dice(emoji="🎰", reply_markup=markup_games)
                data = data['dice']['value']
                try:
                    user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                    betting = user_db.bet
                    await asyncio.sleep(2)
                    await achivement.update.values(game_slot=achivement.game_slot + 1).where(achivement.user_id == call.message.chat.id).gino.status()
                    session.commit()
                    if data in (1, 22, 43):  # три в ряд без сімок
                        await users.update.values(bal_trx=users.bal_trx + betting * 3).where(users.user_id == call.message.chat.id).gino.status()
                        session.commit()
                        markup_games = await kb.markup_games(call.message)
                        await bot.send_message(call.message.chat.id, _("----------------------------------------------\n\n\n❤ Вітаю!\n\n💶 Ви виграли - {} TRX").format(betting * 3), reply_markup=markup_games)
                        user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                        bal_trx = user_db.bal_trx
                        markup_again_slot = await kb.markup_again_slot(call.message)
                        await bot.send_message(call.message.chat.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_slot, parse_mode='html')
                    elif data in (16, 32, 48):  # дві сімки на початку
                        await users.update.values(bal_trx=users.bal_trx + betting * 4).where(users.user_id == call.message.chat.id).gino.status()
                        session.commit()
                        markup_games = await kb.markup_games(call.message)
                        await bot.send_message(call.message.chat.id, _("----------------------------------------------\n\n\n❤ Вітаю!\n\n💶 Ви виграли - {} TRX").format(betting * 5), reply_markup=markup_games)
                        user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                        bal_trx = user_db.bal_trx
                        markup_again_slot = await kb.markup_again_slot(call.message)
                        await bot.send_message(call.message.chat.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_slot, parse_mode='html')
                    # два співпадіння
                    elif data in (2, 3, 4, 5, 6, 9, 13, 17, 33, 49, 18, 21, 23, 24, 26, 30, 38, 54, 11, 27, 35, 39, 41, 42, 44, 47, 59, 52, 56, 60, 61, 62, 63):
                        await users.update.values(bal_trx=users.bal_trx - betting * 0.7).where(users.user_id == call.message.chat.id).gino.status()
                        session.commit()
                        markup_games = await kb.markup_games(call.message)
                        await bot.send_message(call.message.chat.id, _("----------------------------------------------\n\n\n❤ Вітаю!\n\n💶 Ви виграли - {} TRX").format(betting * 0.3), reply_markup=markup_games)
                        user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                        bal_trx = user_db.bal_trx
                        markup_again_slot = await kb.markup_again_slot(call.message)
                        await bot.send_message(call.message.chat.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_slot, parse_mode='html')
                    elif data == 64:  # три сімки
                        await users.update.values(bal_trx=users.bal_trx + betting * 14).where(users.user_id == call.message.chat.id).gino.status()
                        session.commit()
                        await bot.send_message(call.message.chat.id, _("----------------------------------------------\n\n\n❤ Вітаю. Ви виграли ДЖЕКПОТ Х15!\n\n💶 Ви виграли - {} TRX").format(betting * 15))
                        await bot.send_message(call.message.chat.id, _("📯 Ви виграли ДЖЕКПОТ Х15! 📯"))
                        user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                        bal_trx = user_db.bal_trx
                        markup_again_slot = await kb.markup_again_slot(call.message)
                        await bot.send_message(call.message.chat.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_slot, parse_mode='html')
                    else:
                        await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == call.message.chat.id).gino.status()
                        session.commit()
                        markup_games = await kb.markup_games(call.message)
                        await bot.send_message(call.message.chat.id, _("----------------------------------------------\n\n\n💔 Ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
                        user_db = await users.query.where(
                            users.user_id == call.message.chat.id).gino.first()
                        bal_trx = user_db.bal_trx
                        markup_again_slot = await kb.markup_again_slot(call.message)
                        await bot.send_message(call.message.chat.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_slot, parse_mode='html')
                except:
                    await bot.send_message(call.message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
            else:
                await bot.send_message(call.message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                await bot.send_message(call.message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')


        if call.data == 'again_crush':
            await states.crush.bet_crush.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

        if call.data == 'again_same_bet_crush':
            async def stop_crush():
                try:
                    crush_db = await Crush_model.query.where(Crush_model.user_id == call.message.chat.id).gino.first()
                    stop = crush_db.stop
                    return stop
                except:
                    pass

            db_commands.register_user_crush(call.message.chat.id)
            crush_db = await Crush_model.query.where(Crush_model.user_id == call.message.chat.id).gino.first()
            coef = crush_db.coef
            num_game = crush_db.num_game
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            betting = user_db.bet
            data_coef = coef
            data_num_game = num_game
            bal_trx = user_db.bal_trx
            if betting <= bal_trx:
                await users.update.values(bet=betting).where(users.user_id == call.message.chat.id).gino.status()
                await states.crush.game_crush.set()
                await bot.send_message(call.message.chat.id, _("🛩 Літак готовий, встигни забрати свій виграш"), reply_markup=kb.markup_select_crush)
                if data_num_game == 1.0 or data_num_game == 1.1:
                    # await Crush_model.delete.where(Crush_model.user_id == call.message.chat.id).gino.status()
                    markup_games = await kb.markup_games(call.message)
                    await bot.send_message(call.message.chat.id, _("----------------------------------------------\n\n\n💥 Літак розбився\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), reply_markup=markup_games)
                    await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == call.message.chat.id).gino.status()
                    markup_again_crush_lose = await kb.markup_again_crush_lose(call.message)
                    user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                    bal_trx = user_db.bal_trx
                    await call.message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Множитель був</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, round(data_coef, 1)), reply_markup=markup_again_crush_lose, parse_mode='html')
                else:
                    while round(data_coef, 1) < data_num_game and await stop_crush() == False:
                        await Crush_model.update.values(coef=Crush_model.coef + 0.2).where(Crush_model.user_id == call.message.chat.id).gino.status()
                        crush_db = await Crush_model.query.where(Crush_model.user_id == call.message.chat.id).gino.first()
                        coef = crush_db.coef
                        data_coef = coef
                        await asyncio.sleep(1)
                        await bot.send_message(call.message.chat.id, _("🛫 Літак летить\n\n<b>Коефіцієнт: {}</b>").format(round(data_coef, 1)), reply_markup=kb.markup_again_crush_lose)
                        coef = data_coef
                        num_game = data_num_game
                        bet = betting
                        if data_coef >= data_num_game:
                            # await Crush_model.delete.where(Crush_model.user_id == call.message.chat.id).gino.status()
                            markup_games = await kb.markup_games(call.message)
                            await bot.send_message(call.message.chat.id, _("----------------------------------------------\n\n\n💥 Літак розбився\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), reply_markup=markup_games)
                            await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == call.message.chat.id).gino.status()
                            markup_again_crush_lose = await kb.markup_again_crush_lose(call.message)
                            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                            bal_trx = user_db.bal_trx
                            await call.message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Множитель був</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, round(data_coef, 1)), reply_markup=markup_again_crush_lose, parse_mode='html')
            else:
                await bot.send_message(call.message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                await bot.send_message(call.message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')


        if call.data == 'five_num_guess_game':
            num_game = 5
            await states.guess_number.bet_five.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

            @dp.message_handler(state=states.guess_number.bet_five)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_five(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['bet_five'] = float(message.text)
                    betting = data['bet_five']
                    if betting <= 1000:
                        if betting > 0:
                            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                            bal_trx_bet = user_db.bal_trx
                            if betting <= bal_trx_bet:
                                await users.update.values(bet=betting).where(users.user_id == message.chat.id).gino.status()
                                await states.guess_number.next()
                                await bot.send_message(message.chat.id, _("Загадано число від 1 до {}. Спробуй вгадати").format(num_game), reply_markup=kb.markup_select_rand_num_five)
                            else:
                                await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                                await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                        else:
                            await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
                            await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
                    else:
                        await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
                    await state.finish()

            @dp.message_handler(state=states.guess_number.random_number_five)
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    await states.guess_number.random_number_five.set()
                    data['random_number_five'] = random.randint(1, num_game)
                try:
                    user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                    betting = user_db.bet
                    await achivement.update.values(game_num=achivement.game_num + 1).where(achivement.user_id == message.chat.id).gino.status()
                    session.commit()
                    if int(message.text) >= 1 and int(message.text) <= num_game:
                        if int(message.text) == data['random_number_five']:
                            await users.update.values(bal_trx=users.bal_trx + betting * 3.95).where(users.user_id == message.chat.id).gino.status()
                            session.commit()
                            anim_num = random.sample(range(1, num_game), 3)
                            for rand_anim in anim_num:
                                await asyncio.sleep(0.5)
                                await message.answer(_("❓ Випадає число: ") + '<b>' + str(rand_anim) + '</b> ❓', parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(betting * 4.95), reply_markup=markup_games)
                            markup_again_guess_five = await kb.markup_again_guess_five(message)
                            user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
                            bal_trx = user_db.bal_trx
                            await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_five']), reply_markup=markup_again_guess_five, parse_mode='html')
                            await state.finish()
                        else:
                            await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == message.chat.id).gino.status()
                            session.commit()
                            anim_num = random.sample(range(1, num_game), 3)
                            for rand_anim in anim_num:
                                await asyncio.sleep(0.5)
                                await message.answer(_("❓ Випадає число: ") + '<b>' + str(rand_anim) + '</b> ❓', parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await message.answer(_("----------------------------------------------\n\n\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
                            markup_again_guess_five = await kb.markup_again_guess_five(message)
                            user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
                            bal_trx = user_db.bal_trx
                            await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_five']), reply_markup=markup_again_guess_five,parse_mode='html')
                            await state.finish()
                    else:
                        await bot.send_message(message.chat.id, _("❌ Діапазон чисел <b><i>від 1 до {} включно</i></b>‼").format(num_game), parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
                except:
                    await message.answer(_("❌ Число введене не коректно ❗\n\nВведіть цифру <b><i>від 1 до {} включно</i></b>!!").format(num_game), reply_markup=kb.markup_select_rand_num_five, parse_mode='html')

        if call.data == 'ten_num_guess_game':
            num_game = 10
            await states.guess_number.bet_ten.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format( bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

            @dp.message_handler(state=states.guess_number.bet_ten)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_ten(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['bet_ten'] = float(message.text)
                    betting = data['bet_ten']
                    if betting <= 1000:
                        if betting > 0:
                            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                            bal_trx_bet = user_db.bal_trx
                            if betting <= bal_trx_bet:
                                await users.update.values(bet=betting).where(users.user_id == message.chat.id).gino.status()
                                await states.guess_number.next()
                                await bot.send_message(message.chat.id, _("Загадано число від 1 до {}. Спробуй вгадати").format(num_game), reply_markup=kb.markup_select_rand_num_ten)
                            else:
                                await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                                await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                        else:
                            await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
                            await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
                    else:
                        await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
                    await state.finish()

            @dp.message_handler(state=states.guess_number.random_number_ten)
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    await states.guess_number.random_number_ten.set()
                    data['random_number_ten'] = random.randint(1, num_game)
                try:
                    user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                    betting = user_db.bet
                    await achivement.update.values(game_num=achivement.game_num + 1).where(achivement.user_id == message.chat.id).gino.status()
                    session.commit()
                    if int(message.text) >= 1 and int(message.text) <= num_game:
                        if int(message.text) == data['random_number_ten']:
                            await users.update.values(bal_trx=users.bal_trx + betting * 8.9).where(users.user_id == message.chat.id).gino.status()
                            session.commit()
                            anim_num = random.sample(range(1, num_game), 3)
                            for rand_anim in anim_num:
                                await asyncio.sleep(0.5)
                                await message.answer(_("❓ Випадає число: ") + '<b>' + str(rand_anim) + '</b> ❓', parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(betting * 9.9), reply_markup=markup_games)
                            markup_again_guess_ten = await kb.markup_again_guess_ten(message)
                            user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
                            bal_trx = user_db.bal_trx
                            await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_ten']), reply_markup=markup_again_guess_ten,parse_mode='html')
                            await state.finish()
                        else:
                            await users.update.values(bal_trx=users.bal_trx - betting).where(
                                users.user_id == message.chat.id).gino.status()
                            session.commit()
                            anim_num = random.sample(range(1, num_game), 3)
                            for rand_anim in anim_num:
                                await asyncio.sleep(0.5)
                                await message.answer(_("❓ Випадає число: ") + '<b>' + str(rand_anim) + '</b> ❓', parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await message.answer(_("----------------------------------------------\n\n\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
                            markup_again_guess_ten = await kb.markup_again_guess_ten(message)
                            user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
                            bal_trx = user_db.bal_trx
                            await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_ten']), reply_markup=markup_again_guess_ten, parse_mode='html')
                            await state.finish()
                    else:
                        await bot.send_message(message.chat.id, _("❌ Діапазон чисел <b><i>від 1 до {} включно</i></b>‼").format(num_game), parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
                except:
                    await message.answer(_("❌ Число введене не коректно ❗\n\nВведіть цифру <b><i>від 1 до {} включно</i></b>!!").format(num_game), reply_markup=kb.markup_select_rand_num_ten, parse_mode='html')

        if call.data == 'hun_num_guess_game':
            num_game = 100
            await states.guess_number.bet_hun.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format( bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

            @dp.message_handler(state=states.guess_number.bet_hun)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_hun(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['bet_hun'] = float(message.text)
                    betting = data['bet_hun']
                    if betting <= 1000:
                        if betting > 0:
                            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                            bal_trx_bet = user_db.bal_trx
                            if betting <= bal_trx_bet:
                                await users.update.values(bet=betting).where(users.user_id == message.chat.id).gino.status()
                                await states.guess_number.next()
                                await bot.send_message(message.chat.id, _("Загадано число від 1 до {}. Спробуй вгадати").format(num_game), reply_markup=kb.markup_select_rand_num_hun)
                            else:
                                await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                                await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                        else:
                            await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
                            await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
                    else:
                        await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
                    await state.finish()

            @dp.message_handler(state=states.guess_number.random_number_hun)
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    await states.guess_number.random_number_hun.set()
                    data['random_number_hun'] = random.randint(1, num_game)
                try:
                    user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                    betting = user_db.bet
                    await achivement.update.values(game_num=achivement.game_num + 1).where(achivement.user_id == message.chat.id).gino.status()
                    session.commit()
                    if int(message.text) >= 1 and int(message.text) <= num_game:
                        if int(message.text) == data['random_number_hun']:
                            await users.update.values(bal_trx=users.bal_trx + betting * 94).where(users.user_id == message.chat.id).gino.status()
                            session.commit()
                            anim_num = random.sample(range(1, num_game), 3)
                            for rand_anim in anim_num:
                                await asyncio.sleep(0.5)
                                await message.answer(_("❓ Випадає число: ") + '<b>' + str(rand_anim) + '</b> ❓', parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await achivement.update.values(game_num_win_hun=achivement.game_num_win_hun + 1).where(achivement.user_id == message.chat.id).gino.status()
                            await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(betting * 95), reply_markup=markup_games)
                            markup_again_guess_hun = await kb.markup_again_guess_hun(message)
                            user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
                            bal_trx = user_db.bal_trx
                            await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_hun']), reply_markup=markup_again_guess_hun,parse_mode='html')
                            await state.finish()
                        else:
                            await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == message.chat.id).gino.status()
                            session.commit()
                            anim_num = random.sample(range(1, num_game), 3)
                            for rand_anim in anim_num:
                                await asyncio.sleep(0.5)
                                await message.answer(_("❓ Випадає число: ") + '<b>' + str(rand_anim) + '</b> ❓', parse_mode='html')
                            markup_games = await kb.markup_games(message)
                            await message.answer(_("----------------------------------------------\n\n\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
                            markup_again_guess_hun = await kb.markup_again_guess_hun(message)
                            user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
                            bal_trx = user_db.bal_trx
                            await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_hun']), reply_markup=markup_again_guess_hun, parse_mode='html')
                            await state.finish()
                    else:
                        await bot.send_message(message.chat.id, _("❌ Діапазон чисел <b><i>від 1 до {} включно</i></b>‼").format(num_game), parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
                except:
                    await message.answer(_("❌ Число введене не коректно ❗\n\nВведіть цифру <b><i>від 1 до {} включно</i></b>!!").format(num_game), reply_markup=kb.markup_select_rand_num_hun, parse_mode='html')

        if call.data == 'two_num_fifty_game':
            num_game = 2
            await states.fifty_fifty.bet_two.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

            @dp.message_handler(state=states.fifty_fifty.bet_two)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_two(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['bet_two'] = float(message.text)
                    betting = data['bet_two']
                    if betting <= 1000:
                        if betting > 0:
                            user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                            bal_trx = user_db.bal_trx
                            if betting <= bal_trx:
                                await users.update.values(bet=betting).where(users.user_id == message.chat.id).gino.status()
                                await states.fifty_fifty.next()
                                await bot.send_message(message.chat.id, _("Загадано число від 1 до {}. Спробуй вгадати").format(num_game), reply_markup=kb.markup_select_fifty_two)
                            else:
                                await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                                await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                        else:
                            await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
                            await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                    else:
                        await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
                    await state.finish()

            @dp.message_handler(state=states.fifty_fifty.random_number_two)
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    await states.fifty_fifty.random_number_two.set()
                    data['random_number_two'] = random.randint(1, num_game)
                try:
                    user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                    betting = user_db.bet
                    if int(message.text) >= 1 and int(message.text) <= num_game:
                        anim_num_f = random.randint(1, num_game)
                        anim_num_s = random.randint(1, num_game)
                        anim_num_t = random.randint(1, num_game)
                        await asyncio.sleep(0.5)
                        await message.answer(_("❓ Випадає число: ") + '<b>' + str(
                            anim_num_f) + '</b> ❓', parse_mode='html')
                        await asyncio.sleep(0.5)
                        await message.answer(_("❓ Випадає число: ") + '<b>' + str(
                            anim_num_s) + '</b> ❓', parse_mode='html')
                        await asyncio.sleep(0.5)
                        await message.answer(_("❓ Випадає число: ") + '<b>' + str(
                            anim_num_t) + '</b> ❓', parse_mode='html')
                        if int(message.text) == data['random_number_two']:
                            await achivement.update.values(game_fifty=achivement.game_fifty + 1).where(achivement.user_id == message.chat.id).gino.status()
                            await users.update.values(bal_trx=users.bal_trx + betting * 0.95).where(users.user_id == message.chat.id).gino.status()
                            session.commit()
                            user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
                            bal_trx = user_db.bal_trx
                            markup_games = await kb.markup_games(message)
                            await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(betting * 1.95), reply_markup=markup_games)
                            markup_again_fifty_two = await kb.markup_again_fifty_two(message)
                            await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_two']), reply_markup=markup_again_fifty_two, parse_mode='html')
                            await state.finish()
                        else:
                            await achivement.update.values(game_fifty=achivement.game_fifty + 1).where(achivement.user_id == message.chat.id).gino.status()
                            await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == message.chat.id).gino.status()
                            session.commit()
                            user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
                            bal_trx = user_db.bal_trx
                            markup_games = await kb.markup_games(message)
                            await message.answer(_("----------------------------------------------\n\n\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
                            markup_again_fifty_two = await kb.markup_again_fifty_two(message)
                            await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_two']), reply_markup=markup_again_fifty_two, parse_mode='html')
                            await state.finish()
                    else:
                        await bot.send_message(message.chat.id, _("❌ Діапазон чисел <b><i>від 1 до {} включно</i></b>‼").format(num_game), parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
                except:
                    await message.answer(_("❌ Число введене некоректно ❗\n\nВведіть цифру <b><i>від 1 до {} включно</i></b>!!").format(num_game), reply_markup=kb.markup_select_fifty_two, parse_mode='html')

        if call.data == 'four_num_fifty_game':
            num_game = 4
            await states.fifty_fifty.bet_four.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format( bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

            @dp.message_handler(state=states.fifty_fifty.bet_four)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_four(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['bet_four'] = float(message.text)
                    betting = data['bet_four']
                    if betting <= 1000:
                        if betting > 0:
                            user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                            bal_trx = user_db.bal_trx
                            if betting <= bal_trx:
                                await users.update.values(bet=betting).where(users.user_id == message.chat.id).gino.status()
                                await states.fifty_fifty.next()
                                await bot.send_message(message.chat.id, _("Загадано число від 1 до {}. Спробуй вгадати").format(num_game), reply_markup=kb.markup_select_fifty_four)
                            else:
                                await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                                await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                        else:
                            await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
                            await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                    else:
                        await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
                    await state.finish()

            @dp.message_handler(state=states.fifty_fifty.random_number_four)
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    await states.fifty_fifty.random_number_four.set()
                    data['random_number_four_first'] = random.randint(1, num_game)
                    data['random_number_four_second'] = random.randint(1, num_game)
                    if data['random_number_four_first'] == data['random_number_four_second']:
                        data['random_number_four_second'] = random.randint(1, num_game)
                    if data['random_number_four_first'] == data['random_number_four_second']:
                        data['random_number_four_second'] = random.randint(1, num_game)
                    if data['random_number_four_first'] == data['random_number_four_second']:
                        data['random_number_four_second'] = random.randint(1, num_game)
                    try:
                        user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                        betting = user_db.bet
                        if int(message.text) >= 1 and int(message.text) <= num_game:
                            anim_num = random.sample(range(1, 5), 3)
                            for rand_anim in anim_num:
                                await asyncio.sleep(0.5)
                                await message.answer(_("❓ Випадає число: ") + '<b>' + str(rand_anim) + '</b> ❓', parse_mode='html')
                            if int(message.text) == data['random_number_four_first'] or int(message.text) == data['random_number_four_second']:
                                if int(message.text) == data['random_number_four_first'] and int(message.text) == data['random_number_four_second']:
                                    await achivement.update.values(game_fifty=achivement.game_fifty + 1).where(achivement.user_id == message.chat.id).gino.status()
                                    await users.update.values(bal_trx=users.bal_trx + betting * 2.9).where(users.user_id == message.chat.id).gino.status()
                                    session.commit()
                                    markup_games = await kb.markup_games(message)
                                    await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли із множителем х2!\n\n💶 Ви виграли - {} TRX").format(betting * 3.9), reply_markup=markup_games)
                                else:
                                    await achivement.update.values(game_fifty=achivement.game_fifty + 1).where(achivement.user_id == message.chat.id).gino.status()
                                    await users.update.values(bal_trx=users.bal_trx + betting * 0.95).where(users.user_id == message.chat.id).gino.status()
                                    session.commit()
                                    markup_games = await kb.markup_games(message)
                                    await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(betting * 1.95), reply_markup=markup_games)
                                user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                                bal_trx = user_db.bal_trx
                                markup_again_fifty_four = await kb.markup_again_fifty_four(message)
                                await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <u><b><i>{}</i></b></u>\n🔢 <i>Загадане число було</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_four_first'], data['random_number_four_second']), reply_markup=markup_again_fifty_four, parse_mode='html')
                                await state.finish()
                            else:
                                await achivement.update.values(game_fifty=achivement.game_fifty + 1).where(achivement.user_id == message.chat.id).gino.status()
                                await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == message.chat.id).gino.status()
                                session.commit()
                                user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                                bal_trx = user_db.bal_trx
                                markup_games = await kb.markup_games(message)
                                await message.answer(_("----------------------------------------------\n\n\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
                                markup_again_fifty_four = await kb.markup_again_fifty_four(message)
                                await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <u><b><i>{}</i></b></u>\n🔢 <i>Загадане число було</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_four_first'],data['random_number_four_second']), reply_markup=markup_again_fifty_four,parse_mode='html')
                                await state.finish()
                        else:
                            await bot.send_message(message.chat.id, _("❌ Діапазон чисел <b><i>від 1 до {} включно</i></b>‼").format(num_game), parse_mode='html')
                            await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
                    except:
                        await message.answer(_("❌ Число введене некоректно ❗\n\nВведіть цифру <b><i>від 1 до {} включно</i></b>!!").format(num_game), reply_markup=kb.markup_select_fifty_four, parse_mode='html')

        if call.data == 'classic_dice_game':
            await states.dice.bet_classic.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

            @dp.message_handler(state=states.dice.bet_classic)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_classic(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['bet_classic'] = float(message.text)
                    betting = data['bet_classic']
                    if betting <= 1000:
                        if betting > 0:
                            user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                            bal_trx = user_db.bal_trx
                            if betting <= bal_trx:
                                await users.update.values(bet=betting).where(users.user_id == message.chat.id).gino.status()
                                await states.dice.next()
                                await bot.send_message(message.chat.id, _("Кубик готовий до гри, оберіть ваше значення:"), reply_markup=kb.markup_select_dice_classic)
                            else:
                                await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                                await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                        else:
                            await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
                            await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                    else:
                        await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
                    await state.finish()

            @dp.message_handler(state=states.dice.random_number_classic)
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    await states.dice.random_number_classic.set()
                    data['random_number_classic'] = await bot.send_dice(message.chat.id)
                    data['random_number_classic'] = data['random_number_classic']['dice']['value']
                try:
                    user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                    betting = user_db.bet
                    await asyncio.sleep(4)
                    if int(message.text) >= 1 and int(message.text) <= 6:
                        if int(message.text) == data['random_number_classic']:
                            await achivement.update.values(game_dice=achivement.game_dice + 1).where(achivement.user_id == message.chat.id).gino.status()
                            await users.update.values(bal_trx=users.bal_trx + betting * 4.8).where(users.user_id == message.chat.id).gino.status()
                            session.commit()
                            user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
                            bal_trx = user_db.bal_trx
                            markup_games = await kb.markup_games(message)
                            await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(betting * 5.8), reply_markup=markup_games)
                            markup_again_dice_classic = await kb.markup_again_dice_classic(message)
                            await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Випало число</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_classic']), reply_markup=markup_again_dice_classic, parse_mode='html')
                            await state.finish()
                        else:
                            await achivement.update.values(game_dice=achivement.game_dice + 1).where(achivement.user_id == message.chat.id).gino.status()
                            await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == message.chat.id).gino.status()
                            session.commit()
                            user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
                            bal_trx = user_db.bal_trx
                            markup_games = await kb.markup_games(message)
                            await message.answer(_("----------------------------------------------\n\n\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
                            markup_again_dice_classic = await kb.markup_again_dice_classic(message)
                            await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Випало число</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_classic']), reply_markup=markup_again_dice_classic, parse_mode='html')
                            await state.finish()
                    else:
                        await bot.send_message(message.chat.id, _("❌ Діапазон чисел <b><i>від 1 до 6 включно</i></b>‼"), parse_mode='html', reply_markup=kb.markup_select_dice_classic)
                        await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
                except:
                    await message.answer(_("❌ Число введене не коректно ❗\n\nВведіть цифру <b><i>від 1 до 6 включно</i></b>!!"), reply_markup=kb.markup_select_dice_classic, parse_mode='html')

        if call.data == 'under_s_game':
            await states.dice.bet_under.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

            @dp.message_handler(state=states.dice.bet_under)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_under(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['bet_under'] = float(message.text)
                    betting = data['bet_under']
                    if betting <= 1000:
                        if betting > 0:
                            user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                            bal_trx = user_db.bal_trx
                            if betting <= bal_trx:
                                await users.update.values(bet=betting).where(users.user_id == message.chat.id).gino.status()
                                await states.dice.next()
                                markup_select_dice_under = await kb.markup_select_dice_under(message)
                                await bot.send_message(message.chat.id, _("Кубик готовий до гри, оберіть ваше значення:"), reply_markup=markup_select_dice_under)
                            else:
                                await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                                await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                        else:
                            await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
                            await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                    else:
                        await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.chat.id, "❌ Ви вийшли з гри ‼", reply_markup=markup_games, parse_mode='html')
                    await state.finish()

            @dp.message_handler(state=states.dice.random_number_under)
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    await states.dice.random_number_under.set()
                    data['random_number_under_first'] = await bot.send_dice(message.chat.id)
                    data['random_number_under_second'] = await bot.send_dice(message.chat.id)
                    if data['random_number_under_first']['dice']['value'] + data['random_number_under_second']['dice'][
                        'value'] < 7:
                        data['random_number_under'] = '(x2)\n🎲⬇7️⃣'
                    elif data['random_number_under_first']['dice']['value'] + \
                            data['random_number_under_second']['dice']['value'] == 7:
                        data['random_number_under'] = '(x5.8)\n🎲🟰7️⃣'
                    elif data['random_number_under_first']['dice']['value'] + \
                            data['random_number_under_second']['dice']['value'] > 7:
                        data['random_number_under'] = '(x2)\n🎲⬆7️⃣'
                    else:
                        markup_games = await kb.markup_games(message)
                        await message.answer(f'Error', reply_markup=markup_games)
                    try:
                        user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                        betting = user_db.bet
                        await asyncio.sleep(4)
                        if message.text == '(x2)\n🎲⬇7️⃣' or message.text == '(x5.8)\n🎲🟰7️⃣' or message.text == '(x2)\n🎲⬆7️⃣':
                            if message.text == data['random_number_under']:
                                if data['random_number_under_first']['dice']['value'] + data['random_number_under_second']['dice']['value'] == 7:
                                    await achivement.update.values(game_dice=achivement.game_dice + 1).where(achivement.user_id == message.chat.id).gino.status()
                                    await users.update.values(bal_trx=users.bal_trx + betting * 4.8).where(users.user_id == message.chat.id).gino.status()
                                    session.commit()
                                    markup_games = await kb.markup_games(message)
                                    await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(betting * 5.8), reply_markup=markup_games)
                                else:
                                    await achivement.update.values(game_dice=achivement.game_dice + 1).where(achivement.user_id == message.chat.id).gino.status()
                                    await users.update.values(bal_trx=users.bal_trx + betting).where(users.user_id == message.chat.id).gino.status()
                                    session.commit()
                                    markup_games = await kb.markup_games(message)
                                    await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(betting * 2), reply_markup=markup_games)
                                user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
                                bal_trx = user_db.bal_trx
                                markup_again_dice_under = await kb.markup_again_dice_under(message)
                                await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Випало число</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_under']), reply_markup=markup_again_dice_under, parse_mode='html')
                                await state.finish()
                            else:
                                await achivement.update.values(game_dice=achivement.game_dice + 1).where(achivement.user_id == message.chat.id).gino.status()
                                await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == message.chat.id).gino.status()
                                session.commit()
                                user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
                                bal_trx = user_db.bal_trx
                                markup_games = await kb.markup_games(message)
                                await message.answer(_("----------------------------------------------\n\n\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
                                markup_again_dice_under = await kb.markup_again_dice_under(message)
                                await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Випало число</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_under']), reply_markup=markup_again_dice_under, parse_mode='html')
                                await state.finish()
                        else:
                            markup_select_dice_under = await kb.markup_select_dice_under(message)
                            await bot.send_message(message.chat.id, _("❌ Відповідь введена не коректно‼"), parse_mode='html', reply_markup=markup_select_dice_under)
                            await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                    except:
                        markup_select_dice_under = await kb.markup_select_dice_under(message)
                        await message.answer(_("❌ Відповідь введена не коректно ❗\n\nНапишіть самі, або оберіть відповідь із клавіатури!!"), parse_mode='html', reply_markup=markup_select_dice_under)

        if call.data == 'miner_three_game':
            await states.miner.bet_three.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

            @dp.message_handler(state=states.miner.bet_three)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_three(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['bet_three'] = float(message.text)
                    betting = data['bet_three']
                    if betting <= 1000:
                        if betting > 0:
                            user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                            bal_trx = user_db.bal_trx
                            if betting <= bal_trx:
                                await users.update.values(bet=betting).where(users.user_id == message.chat.id).gino.status()
                                await states.miner.next()
                                random.shuffle(kb.list_buts)
                                markup = types.InlineKeyboardMarkup()
                                for text, data in kb.list_buts:
                                    markup.insert(types.InlineKeyboardButton(text=text, callback_data=data))
                                await bot.send_message(message.chat.id, _("Де немає бомби?"), reply_markup=markup)
                            else:
                                await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                                await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                        else:
                            await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
                            await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                    else:
                        await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
                    await state.finish()

            @dp.callback_query_handler(state=states.miner.random_number_three)
            @dp.throttled(anti_flood, rate=1)
            async def answer(call: types.CallbackQuery, state: FSMContext):
                async with state.proxy() as data:
                    user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                    betting = user_db.bet
                try:
                    await call.message.answer("_🟡_", parse_mode='html')
                    await asyncio.sleep(0.7)
                    await call.message.answer("_💣_", parse_mode='html')
                    await asyncio.sleep(0.7)
                    if call.data == 'field_1' or call.data == 'field_2' or call.data == 'field_3' or call.data == 'field_4' or call.data == 'field_5' or call.data == 'field_6':
                        await call.message.answer("👍", parse_mode='html')
                        await asyncio.sleep(0.7)
                        await achivement.update.values(game_mine=achivement.game_mine + 1).where(achivement.user_id == call.message.chat.id).gino.status()
                        await users.update.values(bal_trx=users.bal_trx + betting * 0.7).where(users.user_id == call.message.chat.id).gino.status()
                        markup_games = await kb.markup_games(call.message)
                        await call.message.answer(_("----------------------------------------------\n\n\n❤ Бомба знешкоджена. Вітаю!\n\n💶 Ви виграли - {} TRX").format(betting * 1.7), reply_markup=markup_games)
                        user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                        bal_trx = user_db.bal_trx
                        markup_again_miner_three = await kb.markup_again_miner_three(call.message)
                        await call.message.answer(_("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_miner_three, parse_mode='html')
                        await call.answer()
                        await state.finish()
                    else:
                        await call.message.answer("💥", parse_mode='html')
                        await asyncio.sleep(0.7)
                        await achivement.update.values(game_mine=achivement.game_mine + 1).where(achivement.user_id == call.message.chat.id).gino.status()
                        await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == call.message.chat.id).gino.status()
                        session.commit()
                        markup_games = await kb.markup_games(call.message)
                        await call.message.answer(_("----------------------------------------------\n\n\n💔 Бомба зірвалась. Ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
                        user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                        bal_trx = user_db.bal_trx
                        markup_again_miner_three = await kb.markup_again_miner_three(call.message)
                        await call.message.answer(_("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_miner_three, parse_mode='html')
                        await call.answer()
                        await state.finish()
                except:
                    await call.message.answer(_("❌ Значення введене не коректно ❗\n\nОберіть поле зі <b><i>списку</i></b>"), parse_mode='html')

        if call.data == 'miner_five_game':
            await states.miner.bet_five.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

            @dp.message_handler(state=states.miner.bet_five)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_five(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['bet_five'] = float(message.text)
                    betting = data['bet_five']
                    if betting <= 1000:
                        if betting > 0:
                            user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                            bal_trx = user_db.bal_trx
                            if betting <= bal_trx:
                                await users.update.values(bet=betting).where(users.user_id == message.chat.id).gino.status()
                                await states.miner.next()
                                random.shuffle(kb.list_buts)
                                markup = types.InlineKeyboardMarkup()
                                for text, data in kb.list_buts:
                                    markup.insert(types.InlineKeyboardButton(text=text, callback_data=data))
                                await bot.send_message(message.chat.id, _("Де немає бомби?"), reply_markup=markup)
                            else:
                                await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                                await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                        else:
                            await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
                            await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                    else:
                        await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
                    await state.finish()

            @dp.callback_query_handler(state=states.miner.random_number_five)
            @dp.throttled(anti_flood, rate=1)
            async def answer(call: types.CallbackQuery, state: FSMContext):
                async with state.proxy() as data:
                    user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                    betting = user_db.bet
                try:
                    await call.message.answer("_🟡_", parse_mode='html')
                    await asyncio.sleep(0.7)
                    await call.message.answer("_💣_", parse_mode='html')
                    await asyncio.sleep(0.7)
                    if call.data == 'field_1' or call.data == 'field_2' or call.data == 'field_3' or call.data == 'field_4':
                        await call.message.answer("👍", parse_mode='html')
                        await asyncio.sleep(0.7)
                        await achivement.update.values(game_mine=achivement.game_mine + 1).where(achivement.user_id == call.message.chat.id).gino.status()
                        await users.update.values(bal_trx=users.bal_trx + betting * 1).where(users.user_id == call.message.chat.id).gino.status()
                        markup_games = await kb.markup_games(call.message)
                        await call.message.answer(_("----------------------------------------------\n\n\n❤ Бомба знешкоджена. Вітаю!\n\n💶 Ви виграли - {} TRX").format(betting * 2), reply_markup=markup_games)
                        user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                        bal_trx = user_db.bal_trx
                        markup_again_miner_five = await kb.markup_again_miner_five(call.message)
                        await call.message.answer(_("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_miner_five, parse_mode='html')
                        await call.answer()
                        await state.finish()
                    else:
                        await call.message.answer("💥", parse_mode='html')
                        await asyncio.sleep(0.7)
                        await achivement.update.values(game_mine=achivement.game_mine + 1).where(achivement.user_id == call.message.chat.id).gino.status()
                        await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == call.message.chat.id).gino.status()
                        session.commit()
                        markup_games = await kb.markup_games(call.message)
                        await call.message.answer(_("----------------------------------------------\n\n\n💔 Бомба зірвалась. Ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
                        user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                        bal_trx = user_db.bal_trx
                        markup_again_miner_five = await kb.markup_again_miner_five(call.message)
                        await call.message.answer(_("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_miner_five, parse_mode='html')
                        await call.answer()
                        await state.finish()
                except:
                    await call.message.answer(_("❌ Значення введене не коректно ❗\n\nОберіть поле зі <b><i>списку</i></b>"), parse_mode='html')

        if call.data == 'miner_seven_game':
            await states.miner.bet_seven.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

            @dp.message_handler(state=states.miner.bet_seven)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_seven(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['bet_seven'] = float(message.text)
                    betting = data['bet_seven']
                    if betting <= 1000:
                        if betting > 0:
                            user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                            bal_trx = user_db.bal_trx
                            if betting <= bal_trx:
                                await users.update.values(bet=betting).where(users.user_id == message.chat.id).gino.status()
                                await states.miner.next()
                                random.shuffle(kb.list_buts)
                                markup = types.InlineKeyboardMarkup()
                                for text, data in kb.list_buts:
                                    markup.insert(types.InlineKeyboardButton(text=text, callback_data=data))
                                await bot.send_message(message.chat.id, _("Де немає бомби?"), reply_markup=markup)
                            else:
                                await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                                await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                        else:
                            await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
                            await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                    else:
                        await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
                    await state.finish()

            @dp.callback_query_handler(state=states.miner.random_number_seven)
            @dp.throttled(anti_flood, rate=1)
            async def answer(call: types.CallbackQuery, state: FSMContext):
                async with state.proxy() as data:
                    user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                    betting = user_db.bet
                try:
                    await call.message.answer("_🟡_", parse_mode='html')
                    await asyncio.sleep(0.7)
                    await call.message.answer("_💣_", parse_mode='html')
                    await asyncio.sleep(0.7)
                    if call.data == 'field_1' or call.data == 'field_2':
                        await call.message.answer("👍", parse_mode='html')
                        await asyncio.sleep(0.7)
                        await achivement.update.values(game_mine=achivement.game_mine + 1).where(achivement.user_id == call.message.chat.id).gino.status()
                        await users.update.values(bal_trx=users.bal_trx + betting * 3.5).where(users.user_id == call.message.chat.id).gino.status()
                        session.commit()
                        markup_games = await kb.markup_games(call.message)
                        await call.message.answer(_("----------------------------------------------\n\n\n❤ Бомба знешкоджена. Вітаю!\n\n💶 Ви виграли - {} TRX").format(betting * 4.5), reply_markup=markup_games)
                        user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                        bal_trx = user_db.bal_trx
                        markup_again_miner_seven = await kb.markup_again_miner_seven(call.message)
                        await call.message.answer(_("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_miner_seven, parse_mode='html')
                        await call.answer()
                        await state.finish()
                    else:
                        await call.message.answer("💥", parse_mode='html')
                        await asyncio.sleep(0.7)
                        await achivement.update.values(game_mine=achivement.game_mine + 1).where(achivement.user_id == call.message.chat.id).gino.status()
                        await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == call.message.chat.id).gino.status()
                        session.commit()
                        markup_games = await kb.markup_games(call.message)
                        await call.message.answer(_("----------------------------------------------\n\n\n💔 Бомба зірвалась. Ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
                        user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                        bal_trx = user_db.bal_trx
                        markup_again_miner_seven = await kb.markup_again_miner_seven(call.message)
                        await call.message.answer(_("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_miner_seven, parse_mode='html')
                        await call.answer()
                        await state.finish()
                except:
                    await call.message.answer(_("❌ Значення введене не коректно ❗\n\nОберіть поле зі <b><i>списку</i></b>"), parse_mode='html')

        if call.data == 'br_case_game':
            await states.cases.case_br_buy.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n.\n.\n.\n.\n.").format(bal_trx), parse_mode='html')
            markup_accept_cases = await kb.markup_accept_cases(call.message)
            await bot.send_message(call.message.chat.id, _("Ви дійсно хочете купити даний кейс за <b><i>10</i></b> TRX ?"), reply_markup=markup_accept_cases, parse_mode='html')

            @dp.callback_query_handler(state=states.cases.case_br_buy, text_contains='accept_case_game')
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                bal_trx = user_db.bal_trx
                if bal_trx >= 10:
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.from_user.id, _("Ви купили кейс 📦"), reply_markup=markup_games, parse_mode='html')
                    anim_num = random.sample(range(5, 15), 3)
                    for rand_anim in anim_num:
                        await asyncio.sleep(0.5)
                        await bot.send_message(message.from_user.id, _("❓ Ви виграли: ") + '<b>' + str(rand_anim) + ' TRX</b> ❓', parse_mode='html')
                    cash = random.randint(5, 15)
                    if cash >= 13:
                        cash = random.randint(5, 15)
                    await achivement.update.values(game_case=achivement.game_case + 1).where(achivement.user_id == message.from_user.id).gino.status()
                    await users.update.values(bal_trx=users.bal_trx + cash - 10).where(users.user_id == message.from_user.id).gino.status()
                    session.commit()
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.from_user.id, _("----------------------------------------------\n\n\n❤ Вітаю!\n💶 Ви виграли - {} TRX").format(cash), reply_markup=markup_games)
                    user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                    bal_trx = user_db.bal_trx
                    markup_again_br_case = await kb.markup_again_br_case(message)
                    await bot.send_message(message.from_user.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_br_case, parse_mode='html')
                    await state.finish()
                else:
                    await bot.send_message(message.from_user.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                    await state.finish()

        if call.data == 'si_case_game':
            await states.cases.case_si_buy.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n.\n.\n.\n.\n.").format(bal_trx), parse_mode='html')
            markup_accept_cases = await kb.markup_accept_cases(call.message)
            await bot.send_message(call.message.chat.id, _("Ви дійсно хочете купити даний кейс за <b><i>100</i></b> TRX ?"), reply_markup=markup_accept_cases, parse_mode='html')

            @dp.callback_query_handler(state=states.cases.case_si_buy, text_contains='accept_case_game')
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                bal_trx = user_db.bal_trx
                if bal_trx >= 100:
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.from_user.id, _("Ви купили кейс 🎒"), reply_markup=markup_games, parse_mode='html')
                    anim_num = random.sample(range(50, 150), 3)
                    for rand_anim in anim_num:
                        await asyncio.sleep(0.5)
                        await bot.send_message(message.from_user.id, _("❓ Ви виграли: ") + '<b>' + str(rand_anim) + ' TRX</b> ❓', parse_mode='html')
                    cash = random.randint(50, 150)
                    if cash >= 135:
                        cash = random.randint(50, 150)
                    await achivement.update.values(game_case=achivement.game_case + 1).where(achivement.user_id == message.from_user.id).gino.status()
                    await users.update.values(bal_trx=users.bal_trx + cash - 100).where(users.user_id == message.from_user.id).gino.status()
                    session.commit()
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.from_user.id, _("----------------------------------------------\n\n\n❤ Вітаю!\n💶 Ви виграли - {} TRX").format(cash), reply_markup=markup_games)
                    user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                    bal_trx = user_db.bal_trx
                    markup_again_si_case = await kb.markup_again_si_case(message)
                    await bot.send_message(message.from_user.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_si_case, parse_mode='html')
                    await state.finish()
                else:
                    await bot.send_message(message.from_user.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                    await state.finish()

        if call.data == 'go_case_game':
            await states.cases.case_go_buy.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n.\n.\n.\n.\n.").format(bal_trx), parse_mode='html')
            markup_accept_cases = await kb.markup_accept_cases(call.message)
            await bot.send_message(call.message.chat.id, _("Ви дійсно хочете купити даний кейс за <b><i>1000</i></b> TRX ?"), reply_markup=markup_accept_cases, parse_mode='html')

            @dp.callback_query_handler(state=states.cases.case_go_buy, text_contains='accept_case_game')
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                bal_trx = user_db.bal_trx
                if bal_trx >= 1000:
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.from_user.id, _("Ви купили кейс 💼"), reply_markup=markup_games, parse_mode='html')
                    anim_num = random.sample(range(0, 1500), 3)
                    for rand_anim in anim_num:
                        await asyncio.sleep(0.5)
                        await bot.send_message(message.from_user.id, _("❓ Ви виграли: ") + '<b>' + str(rand_anim) + ' TRX</b> ❓', parse_mode='html')
                    cash = random.randint(0, 1500)
                    if cash >= 1350:
                        cash = random.randint(0, 1500)
                    await achivement.update.values(game_case=achivement.game_case + 1).where(achivement.user_id == message.from_user.id).gino.status()
                    await users.update.values(bal_trx=users.bal_trx + cash - 1000).where(users.user_id == message.from_user.id).gino.status()
                    session.commit()
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.from_user.id, _("----------------------------------------------\n\n\n❤ Вітаю!\n💶 Ви виграли - {} TRX").format(cash), reply_markup=markup_games)
                    user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                    bal_trx = user_db.bal_trx
                    markup_again_go_case = await kb.markup_again_go_case(message)
                    await bot.send_message(message.from_user.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_go_case, parse_mode='html')
                    await state.finish()
                else:
                    await bot.send_message(message.from_user.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                    await state.finish()

        if call.data == 'accept_spin':
            await states.spin.bet_spin.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')

            @dp.message_handler(state=states.spin.bet_spin)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_spin(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['bet_spin'] = float(message.text)
                    betting = data['bet_spin']
                    if betting <= 1000:
                        if betting > 0:
                            user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                            bal_trx = user_db.bal_trx
                            if betting <= bal_trx:
                                await users.update.values(bet=betting).where(users.user_id == message.chat.id).gino.status()
                                await bot.send_message(message.chat.id, _("Автомат готовий до гри"))
                                async with state.proxy() as data:
                                    markup_games = await kb.markup_games(message)
                                    data['random_number_spin'] = await message.answer_dice(emoji="🎰", reply_markup=markup_games)
                                    data['random_number_spin'] = data['random_number_spin']['dice']['value']
                                try:
                                    user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                                    betting = user_db.bet
                                    await asyncio.sleep(2)
                                    await achivement.update.values(game_slot=achivement.game_slot + 1).where(achivement.user_id == message.from_user.id).gino.status()
                                    session.commit()
                                    if data['random_number_spin'] in (1, 22, 43):  # три в ряд без сімок
                                        await users.update.values(bal_trx=users.bal_trx + betting * 3).where(users.user_id == message.from_user.id).gino.status()
                                        session.commit()
                                        markup_games = await kb.markup_games(message)
                                        await bot.send_message(call.message.chat.id, _("----------------------------------------------\n\n\n❤ Вітаю!\n\n💶 Ви виграли - {} TRX").format(betting * 3), reply_markup=markup_games)
                                        user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                                        bal_trx = user_db.bal_trx
                                        markup_again_slot = await kb.markup_again_slot(message)
                                        await bot.send_message(message.chat.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_slot, parse_mode='html')
                                        await state.finish()
                                    elif data['random_number_spin'] in (16, 32, 48):  # дві сімки на початку
                                        await users.update.values(bal_trx=users.bal_trx + betting * 4).where(users.user_id == message.from_user.id).gino.status()
                                        session.commit()
                                        markup_games = await kb.markup_games(message)
                                        await bot.send_message(message.chat.id, _("----------------------------------------------\n\n\n❤ Вітаю!\n\n💶 Ви виграли - {} TRX").format(betting * 5), reply_markup=markup_games)
                                        user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                                        bal_trx = user_db.bal_trx
                                        markup_again_slot = await kb.markup_again_slot(message)
                                        await bot.send_message(message.chat.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_slot, parse_mode='html')
                                        await state.finish()
                                    # два співпадіння
                                    elif data['random_number_spin'] in (2, 3, 4, 5, 6, 9, 13, 17, 33, 49, 18, 21, 23, 24, 26, 30, 38, 54, 11, 27, 35, 39, 41, 42, 44, 47, 59, 52, 56, 60, 61, 62, 63):
                                        await users.update.values(bal_trx=users.bal_trx - betting * 0.7).where(users.user_id == message.from_user.id).gino.status()
                                        session.commit()
                                        markup_games = await kb.markup_games(message)
                                        await bot.send_message(message.chat.id, _("----------------------------------------------\n\n\n❤ Вітаю!\n\n💶 Ви виграли - {} TRX").format(betting * 0.3), reply_markup=markup_games)
                                        user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                                        bal_trx = user_db.bal_trx
                                        markup_again_slot = await kb.markup_again_slot(message)
                                        await bot.send_message(message.chat.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_slot, parse_mode='html')
                                        await state.finish()
                                    elif data['random_number_spin'] == 64:  # три сімки
                                        await users.update.values(bal_trx=users.bal_trx + betting * 14).where(users.user_id == message.from_user.id).gino.status()
                                        session.commit()
                                        await bot.send_message(message.chat.id, _("----------------------------------------------\n\n\n❤ Вітаю. Ви виграли ДЖЕКПОТ Х15!\n\n💶 Ви виграли - {} TRX").format(betting * 15))
                                        await bot.send_message(message.chat.id, _("📯 Ви виграли ДЖЕКПОТ Х15! 📯"))
                                        user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                                        bal_trx = user_db.bal_trx
                                        markup_again_slot = await kb.markup_again_slot(message)
                                        await bot.send_message(message.chat.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_slot, parse_mode='html')
                                        await state.finish()
                                    else:
                                        await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == message.from_user.id).gino.status()
                                        session.commit()
                                        markup_games = await kb.markup_games(message)
                                        await bot.send_message(message.chat.id, _("----------------------------------------------\n\n\n💔 Ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
                                        user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                                        bal_trx = user_db.bal_trx
                                        markup_again_slot = await kb.markup_again_slot(message)
                                        await bot.send_message(message.chat.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_slot, parse_mode='html')
                                        await state.finish()
                                except:
                                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                                await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                        else:
                            await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
                            await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                    else:
                        await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
                    await state.finish()

        if call.data == 'crush_buy_game':
            await states.crush.bet_crush.set()
            user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
            bal_trx = user_db.bal_trx
            await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
            await bot.delete_message(call.message.chat.id, call.message.message_id)

            async def stop_crush():
                try:
                    crush_db = await Crush_model.query.where(Crush_model.user_id == call.message.chat.id).gino.first()
                    stop = crush_db.stop
                    return stop
                except:
                    pass

            @dp.message_handler(state=states.crush.bet_crush)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_crush(message: types.Message, state: FSMContext):
                try:
                    db_commands.register_user_crush(message.from_user.id)
                    crush_db = await Crush_model.query.where(Crush_model.user_id == call.message.chat.id).gino.first()
                    coef = crush_db.coef
                    num_game = crush_db.num_game
                    async with state.proxy() as data:
                        data['bet_crush'] = float(message.text)
                        data['coef'] = coef
                        data['num_game'] = num_game

                        betting = data['bet_crush']
                        if betting <= 1000:
                            if betting > 0:
                                user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                                bal_trx = user_db.bal_trx
                                if betting <= bal_trx:
                                    await users.update.values(bet=betting).where(users.user_id == message.chat.id).gino.status()
                                    await states.crush.next()
                                    await bot.send_message(message.chat.id, _("🛩 Літак готовий, встигни забрати свій виграш"), reply_markup=kb.markup_select_crush)
                                    if data['num_game'] != 1.0 or data['num_game'] != 1.1:
                                        while round(data['coef'], 1) < data['num_game'] and await stop_crush() == False:
                                            await Crush_model.update.values(coef=Crush_model.coef + 0.2).where(Crush_model.user_id == message.from_user.id).gino.status()
                                            crush_db = await Crush_model.query.where(Crush_model.user_id == call.message.chat.id).gino.first()
                                            coef = crush_db.coef
                                            data['coef'] = coef
                                            await asyncio.sleep(1)
                                            await bot.send_message(message.chat.id, _("🛫 Літак летить\n\n<b>Коефіцієнт: {}</b>").format(round(data['coef'], 1)), reply_markup=kb.markup_select_crush)
                                            await state.update_data(coef=data['coef'], num_game=data['num_game'], bet=data['bet_crush'])
                                            if round(data['coef'], 1) >= data['num_game']:
                                                await Crush_model.delete.where(Crush_model.user_id == message.from_user.id).gino.status()
                                                markup_games = await kb.markup_games(message)
                                                await bot.send_message(message.chat.id, _("----------------------------------------------\n\n\n💥 Літак розбився\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(data['bet_crush']), reply_markup=markup_games)
                                                await users.update.values(bal_trx=users.bal_trx - data['bet_crush']).where(users.user_id == message.from_user.id).gino.status()
                                                markup_again_crush = await kb.markup_again_crush(message)
                                                user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
                                                bal_trx = user_db.bal_trx
                                                await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Множитель був</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, round(data['coef'], 1) ), reply_markup=markup_again_crush, parse_mode='html')
                                                await state.finish()
                                    else:
                                        await Crush_model.delete.where(Crush_model.user_id == message.from_user.id).gino.status()
                                        markup_games = await kb.markup_games(message)
                                        await bot.send_message(message.chat.id, _("----------------------------------------------\n\n\n💥 Літак розбився\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(data['bet_crush']), reply_markup=markup_games)
                                        await users.update.values(bal_trx=users.bal_trx - data['bet_crush']).where(users.user_id == message.from_user.id).gino.status()
                                        markup_again_crush = await kb.markup_again_crush(message)
                                        user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
                                        bal_trx = user_db.bal_trx
                                        await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Множитель був</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, round(data['coef'], 1)), reply_markup=markup_again_crush, parse_mode='html')
                                        await state.finish()
                                else:
                                    await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
                                    await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                            else:
                                await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
                                await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                        else:
                            await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
                            await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_games = await kb.markup_games(message)
                    await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
                    await state.finish()


            @dp.message_handler(state=states.crush.game_crush)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_crush(message: types.Message, state: FSMContext):
                crush_db = await Crush_model.query.where(Crush_model.user_id == call.message.chat.id).gino.first()
                coef = crush_db.coef
                num_game = crush_db.num_game
                user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
                bet = user_db.bet
                if round(coef, 1) < num_game:
                    if message.text == '⬇ Забрати':
                        await Crush_model.update.values(stop=True).where(Crush_model.user_id == message.from_user.id).gino.status()
                        await state.finish()
                        await asyncio.sleep(1)
                        markup_games = await kb.markup_games(message)
                        await users.update.values(bal_trx=users.bal_trx + bet * round(coef, 1) - bet).where(users.user_id == message.from_user.id).gino.status()
                        await bot.send_message(message.chat.id, _("----------------------------------------------\n\n\n🛬 Літак успішно приземлився\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(bet * round(coef, 1)), reply_markup=markup_games, parse_mode='html')
                        await asyncio.sleep(0.5)
                        await bot.delete_message(message.chat.id, message.message_id + 1)
                    else:
                        await state.finish()
                else:
                    await state.finish()
                    await asyncio.sleep(1)
                    markup_games = await kb.markup_games(message)
                    await users.update.values(bal_trx=users.bal_trx - bet).where(users.user_id == message.from_user.id).gino.status()
                    await bot.send_message(message.chat.id, _("----------------------------------------------\n\n\n💥 Літак розбився\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(bet), reply_markup=markup_games)
                await Crush_model.delete.where(Crush_model.user_id == message.from_user.id).gino.status()
                markup_again_crush = await kb.markup_again_crush(message)
                user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
                bal_trx = user_db.bal_trx
                await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Множитель був</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, num_game), reply_markup=markup_again_crush, parse_mode='html')

        if call.data == 'lot_buy_game':
            if not await db_commands.select_lottery_user(call.message.chat.id):
                user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
                bal_trx = user_db.bal_trx
                if bal_trx >= 15:
                    await db_commands.add_lot(call.message.chat.id)
                    await call.answer(_("✅ Підтверджено"))
                    await users.update.values(bal_trx=users.bal_trx - 15).where(users.user_id == call.message.chat.id).gino.status()
                    await call.message.answer(_("Вітаю!"))
                    await call.message.answer(_("✅ Ви взяли участь у лотереї. Щасти 🎫"))
                    return session.commit()
                else:
                    await call.message.answer(_("❌ Недостатньо коштів ‼"))
            else:
                await call.message.answer("❗ Ви вже взяли участь у цьому розіграші лотереї")



        if call.data == 'mailing_admin':
            await bot.send_message(call.message.chat.id, _("✍ Введіть текст розсилки:"), reply_markup=types.ReplyKeyboardRemove())
            await mailing.text.set()

        if call.data == 'pay_admin':
            markup_admin = types.InlineKeyboardMarkup(row_width=1)
            del_trx_admin = types.InlineKeyboardButton(_('⬆ Заявки на вивід ({})').format(await db_commands.count_del_trx_admin(0)), callback_data='del_trx_admin_day')
            add_trx_admin = types.InlineKeyboardButton(_('💶 Заявки на поповнення TRX ({})').format(await db_commands.count_add_trx_admin(0)), callback_data='add_trx_admin_day')
            add_usd_admin = types.InlineKeyboardButton(_('💲 Заявки на поповнення USDT ({})').format(await db_commands.count_add_usd_admin(0)), callback_data='add_usd_admin_day')
            say_hi_admin_kb = types.InlineKeyboardButton(_('🗣 Поділитись історією/музикою ({})').format(await db_commands.count_say_hi_admin(0)), callback_data='say_hi_admin_kb_day')
            work_user_admin = types.InlineKeyboardButton(_('🤖 Робота з користувачем'), callback_data='work_user_admin')
            mailing_admin = types.InlineKeyboardButton(_('✍ Розсилка'), callback_data='mailing_admin')
            markup_admin.add(del_trx_admin, add_trx_admin, add_usd_admin, say_hi_admin_kb, mailing_admin, work_user_admin)
            await bot.send_message(call.message.chat.id, f'👤 Адмін панель:                                                                        ㅤ', reply_markup=markup_admin)

        if call.data == 'del_trx_admin_day' or call.data == 'del_trx_pay_history_admin_day' or call.data == 'del_trx_pay_history_admin_mon' or call.data == 'del_trx_pay_history_admin_yea' or call.data == 'del_trx_pay_history_admin_all':
            try:
                within_als = {
                    "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                    "mon": ('month', 'МІСЯЦЬ'),
                    "yea": ('year', 'РІК'),
                    "all": ('all', 'ВЕСЬ ЧАС'),
                }
                within = call.data[-3:]
                all_users = await db_commands.get_users()
                for user in all_users:
                    records = await db_commands.get_records(user, within)
                    if (len(records)):
                        answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user}</code></b>\n")
                        for r in records:
                            if r.del_trx != 0:
                                answer += (f"<b><i>ID</i> = <code>{r.id}</code></b>\n\n")
                                answer += ("<b>" + ("➖ ") + "</b>")
                                if r.del_trx != 0:
                                    answer += f"<b><u><i>{r.del_trx} TRX</i></u></b>"
                                answer += f"\n🕐 {r.date}  "
                                answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                answer += (f"📬 Адреса: <code>{r.adress}</code>\n")
                                if r.acces == 0:
                                    answer += f"<b>❌ Не виконано</b>\n\n"
                                elif r.acces == 1:
                                    answer += f"<b>✅ Виконано</b>\n\n"
                                else:
                                    answer += f"<b>💢 Помилка виконання</b>\n\n"
                            else:
                                pass
                        await sleep(0.33)
                        await call.message.answer(answer, parse_mode='html')
                    else:
                        pass
                await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin)
            except:
                pass

        if call.data == 'pay_history_all_not_acces_admin_del_trx':
            try:
                within_als = {
                    "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                    "mon": ('month', 'МІСЯЦЬ'),
                    "yea": ('year', 'РІК'),
                    "all": ('all', 'ВЕСЬ ЧАС'),
                }
                within = 'yea'
                all_users = await db_commands.get_users()
                for user in all_users:
                    records = await db_commands.get_records(user, within)
                    if (len(records)):
                        answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user}</code></b>\n")
                        for r in records:
                            if r.acces == 0:
                                if r.del_trx != 0:
                                    answer += (f"<b><i>ID</i> = <code>{r.id}</code></b>\n\n")
                                    answer += ("<b>" + ("➖ ") + "</b>")
                                    if r.del_trx != 0:
                                        answer += f"<b><u><i>{r.del_trx} TRX</i></u></b>"
                                    answer += f"\n🕐 {r.date}  "
                                    answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                    answer += (f"📬 Адреса: <code>{r.adress}</code>\n")
                                    if r.acces == 0:
                                        answer += f"<b>❌ Не виконано</b>\n\n"
                                    elif r.acces == 1:
                                        answer += f"<b>✅ Виконано</b>\n\n"
                                    else:
                                        answer += f"<b>💢 Помилка виконання</b>\n\n"
                                else:
                                    pass
                            else:
                                pass
                        await sleep(0.33)
                        await call.message.answer(answer, parse_mode='html')
                    else:
                        pass
                await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin)
            except:
                pass

        if call.data == 'add_trx_admin_day' or call.data == 'add_trx_pay_history_admin_day' or call.data == 'add_trx_pay_history_admin_mon' or call.data == 'add_trx_pay_history_admin_yea' or call.data == 'add_trx_pay_history_admin_all':
            try:
                within_als = {
                    "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                    "mon": ('month', 'МІСЯЦЬ'),
                    "yea": ('year', 'РІК'),
                    "all": ('all', 'ВЕСЬ ЧАС'),
                }
                within = call.data[-3:]
                all_users = await db_commands.get_users()
                for user in all_users:
                    records = await db_commands.get_records(user, within)
                    if (len(records)):
                        answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user}</code></b>\n")
                        for r in records:
                            if r.add_trx != 0:
                                answer += (f"<b><i>ID</i> = <code>{r.id}</code></b>\n\n")
                                answer += ("<b>" + ("➖ ") + "</b>")
                                if r.add_trx != 0:
                                    answer += f"<b><u><i>{r.add_trx} TRX</i></u></b>"
                                answer += f"\n🕐 {r.date}  "
                                answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                answer += (f"📬 Адреса: <code>{r.adress}</code>\n")
                                if r.acces == 0:
                                    answer += f"<b>❌ Не виконано</b>\n\n"
                                elif r.acces == 1:
                                    answer += f"<b>✅ Виконано</b>\n\n"
                                else:
                                    answer += f"<b>💢 Помилка виконання</b>\n\n"
                            else:
                                pass
                        await sleep(0.33)
                        await call.message.answer(answer, parse_mode='html')
                    else:
                        pass
                await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin_add_trx)
            except:
                pass

        if call.data == 'pay_history_all_not_acces_admin_add_trx':
            try:
                within_als = {
                    "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                    "mon": ('month', 'МІСЯЦЬ'),
                    "yea": ('year', 'РІК'),
                    "all": ('all', 'ВЕСЬ ЧАС'),
                }
                within = 'yea'
                all_users = await db_commands.get_users()
                for user in all_users:
                    records = await db_commands.get_records(user, within)
                    if (len(records)):
                        answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user}</code></b>\n")
                        for r in records:
                            if r.acces == 0:
                                if r.add_trx != 0:
                                    answer += (f"<b><i>ID</i> = <code>{r.id}</code></b>\n\n")
                                    answer += ("<b>" + ("➖ ") + "</b>")
                                    if r.add_trx != 0:
                                        answer += f"<b><u><i>{r.add_trx} TRX</i></u></b>"
                                    answer += f"\n🕐 {r.date}  "
                                    answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                    answer += (f"📬 Адреса: <code>{r.adress}</code>\n")
                                    if r.acces == 0:
                                        answer += f"<b>❌ Не виконано</b>\n\n"
                                    elif r.acces == 1:
                                        answer += f"<b>✅ Виконано</b>\n\n"
                                    else:
                                        answer += f"<b>💢 Помилка виконання</b>\n\n"
                                else:
                                    pass
                            else:
                                pass
                        await sleep(0.33)
                        await call.message.answer(answer, parse_mode='html')
                    else:
                        pass
                await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin_add_trx)
            except:
                pass

        if call.data == 'add_usd_admin_day' or call.data == 'add_usd_pay_history_admin_day' or call.data == 'add_usd_pay_history_admin_mon' or call.data == 'add_usd_pay_history_admin_yea' or call.data == 'add_usd_pay_history_admin_all':
            try:
                within_als = {
                    "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                    "mon": ('month', 'МІСЯЦЬ'),
                    "yea": ('year', 'РІК'),
                    "all": ('all', 'ВЕСЬ ЧАС'),
                }
                within = call.data[-3:]
                all_users = await db_commands.get_users()
                for user in all_users:
                    records = await db_commands.get_records(user, within)
                    if (len(records)):
                        answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user}</code></b>\n")
                        for r in records:
                            if r.add_usd != 0:
                                answer += (f"<b><i>ID</i> = <code>{r.id}</code></b>\n\n")
                                answer += ("<b>" + ("➖ ") + "</b>")
                                if r.add_usd != 0:
                                    answer += f"<b><u><i>{r.add_usd} USDT</i></u></b>"
                                answer += f"\n🕐 {r.date}  "
                                answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                answer += (f"📬 Адреса: <code>{r.adress}</code>\n")
                                if r.acces == 0:
                                    answer += f"<b>❌ Не виконано</b>\n\n"
                                elif r.acces == 1:
                                    answer += f"<b>✅ Виконано</b>\n\n"
                                else:
                                    answer += f"<b>💢 Помилка виконання</b>\n\n"
                            else:
                                pass
                        await sleep(0.33)
                        await call.message.answer(answer, parse_mode='html')
                    else:
                        pass
                await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin_add_usd)
            except:
                pass

        if call.data == 'pay_history_all_not_acces_admin_add_usd':
            try:
                within_als = {
                    "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                    "mon": ('month', 'МІСЯЦЬ'),
                    "yea": ('year', 'РІК'),
                    "all": ('all', 'ВЕСЬ ЧАС'),
                }
                within = 'yea'
                all_users = await db_commands.get_users()
                for user in all_users:
                    records = await db_commands.get_records(user, within)
                    if (len(records)):
                        answer = (f"📖 Істория транзакцій за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user}</code></b>\n")
                        for r in records:
                            if r.acces == 0:
                                if r.add_usd != 0:
                                    answer += (f"<b><i>ID</i> = <code>{r.id}</code></b>\n\n")
                                    answer += ("<b>" + ("➖ ") + "</b>")
                                    if r.add_usd != 0:
                                        answer += f"<b><u><i>{r.add_usd} USDT</i></u></b>"
                                    answer += f"\n🕐 {r.date}  "
                                    answer += ("<b>" + ("|  Вивід") + "</b>\n")
                                    answer += (f"📬 Адреса: <code>{r.adress}</code>\n")
                                    if r.acces == 0:
                                        answer += f"<b>❌ Не виконано</b>\n\n"
                                    elif r.acces == 1:
                                        answer += f"<b>✅ Виконано</b>\n\n"
                                    else:
                                        answer += f"<b>💢 Помилка виконання</b>\n\n"
                                else:
                                    pass
                            else:
                                pass
                        await sleep(0.33)
                        await call.message.answer(answer, parse_mode='html')
                    else:
                        pass
                await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_pay_history_admin_add_usd)
            except:
                pass

        if call.data == 'pay_admin_kb_do_acces':
            await states.pay_admin_kb_do_acces.user_id.set()
            await bot.send_message(call.message.chat.id, _('🔑 Введіть ID запису (id)'), reply_markup=kb.cancel_num, parse_mode='html')

            @dp.message_handler(state=states.pay_admin_kb_do_acces.user_id)
            @dp.throttled(anti_flood, rate=1)
            async def acces_say_hi_admin(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    data['user_id'] = int(message.text)
                    await bot.send_message(call.message.chat.id, _('Оберіть операцію'), parse_mode='html', reply_markup=kb.markup_cancel)
                await bot.send_message(call.message.chat.id, _('Оберіть операцію'), parse_mode='html', reply_markup=kb.markup_pay_admin_kb_do_acces)
                await states.pay_admin_kb_do_acces.next()

            @dp.callback_query_handler(state=states.pay_admin_kb_do_acces.select)
            @dp.throttled(anti_flood, rate=1)
            async def answer(call: types.CallbackQuery, state: FSMContext):
                if call.data == 'pay_admin_kb_do_acces_set_null':
                    try:
                        async with state.proxy() as data:
                            record_id = data['user_id']
                        await Paymants_model.update.values(acces=0).where(Paymants_model.id == record_id).gino.status()
                        session.commit()
                        paymants_db = await Paymants_model.query.where(Paymants_model.id == record_id).gino.first()
                        user_id = paymants_db.user_id
                        user_db = await users.query.where(users.user_id == user_id).gino.first()
                        bal_trx = user_db.bal_trx
                        bal_usd = user_db.bal_usd
                        user_id_mod = user_db.user_id
                        markup_admin = await kb.markup_admin(call.message)
                        await bot.send_message(call.message.chat.id,_('❌ Баланс TRX: \n{} | Баланс USDT: \n{} TRX\n\n👤 Користувача: \n{}\n\n🔑 Запис: {}\n\n❌ ВІДМІНЕНО').format(bal_trx, bal_usd, user_id_mod, record_id), parse_mode='html', reply_markup=markup_admin)
                        await state.finish()
                    except:
                        await bot.send_message(call.message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                        markup_games = await kb.markup_games(call.message)
                        await bot.send_message(call.message.chat.id, _("❌ Ви вийшли ‼"), reply_markup=markup_games, parse_mode='html')
                        await state.finish()
                elif call.data == 'pay_admin_kb_do_acces_set_one':
                    try:
                        async with state.proxy() as data:
                            record_id = data['user_id']
                        await Paymants_model.update.values(acces=1).where(Paymants_model.id == record_id).gino.status()
                        session.commit()
                        paymants_db = await Paymants_model.query.where(Paymants_model.id == record_id).gino.first()
                        user_id = paymants_db.user_id
                        user_db = await users.query.where(users.user_id == user_id).gino.first()
                        bal_trx = user_db.bal_trx
                        user_id_mod = user_db.user_id
                        markup_admin = await kb.markup_admin(call.message)
                        await bot.send_message(call.message.chat.id,_('✅ Баланс TRX: \n{} TRX\n\n👤 Користувача: \n{}\n\n🔑 Запис: {}\n\n✅ ВИКОНАНО').format(bal_trx, user_id_mod, record_id), parse_mode='html', reply_markup=markup_admin)
                        await state.finish()
                    except:
                        await bot.send_message(call.message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                        markup_games = await kb.markup_games(call.message)
                        await bot.send_message(call.message.chat.id, _("❌ Ви вийшли ‼"), reply_markup=markup_games, parse_mode='html')
                        await state.finish()
                elif call.data == 'pay_admin_kb_do_acces_set_two':
                    try:
                        async with state.proxy() as data:
                            record_id = data['user_id']
                        await Paymants_model.update.values(acces=2).where(Paymants_model.id == record_id).gino.status()
                        session.commit()
                        paymants_db = await Paymants_model.query.where(Paymants_model.id == record_id).gino.first()
                        user_id = paymants_db.user_id
                        user_db = await users.query.where(users.user_id == user_id).gino.first()
                        bal_trx = user_db.bal_trx
                        user_id_mod = user_db.user_id
                        markup_admin = await kb.markup_admin(call.message)
                        await bot.send_message(call.message.chat.id, _('💢 Баланс TRX: \n{} TRX\n\n👤 Користувача: \n{}\n\n🔑 Запис: {}\n\n💢 ПОСТАВЛЕНА ПОМИЛКА').format(bal_trx, user_id_mod, record_id), parse_mode='html', reply_markup=markup_admin)
                        await state.finish()
                    except:
                        await bot.send_message(call.message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                        markup_games = await kb.markup_games(call.message)
                        await bot.send_message(call.message.chat.id, _("❌ Ви вийшли ‼"), reply_markup=markup_games, parse_mode='html')
                        await state.finish()

        if call.data == 'work_user_admin':
            await call.message.edit_text(_('👷 Який вид робіт буде проходити: '), parse_mode='html', reply_markup=kb.markup_work_admin)

        if call.data == 'work_admin_trx':
            await call.message.edit_text(_('🛠 Оберіть операцію: '), parse_mode='html', reply_markup=kb.markup_work_admin_select_trx)

        if call.data == 'work_admin_trx_select_trx':
            await states.work_trx_admin.user_id.set()
            await bot.send_message(call.message.chat.id, _('🔑 Введіть ID користувача (user_id)'), reply_markup=kb.markup_cancel)

            @dp.message_handler(state=states.work_trx_admin.user_id)
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        await states.work_trx_admin.user_id.set()
                        data['user_id'] = int(message.text)
                        user_db = await users.query.where(users.user_id == data['user_id']).gino.first()
                        bal_trx = user_db.bal_trx
                        bal_usd = user_db.bal_usd
                        username = user_db.name
                        await message.answer(_('👤 Kористувач <b><i>{}</i></b> {}\n\n💰 Його баланс становить - <b><i>{} TRX</i></b>| {} USDT\n\n↘ Оберіть суму що хочете додати із клавіатури або введіть її самі').format(data["user_id"], username, bal_trx, bal_usd), parse_mode='html', reply_markup=kb.markup_select_add_trx)
                        await states.work_trx_admin.next()
                except:
                    await message.answer(_("Це не число, або щось пішло не так.Ви можете натиснути на кнопку /cancel"))

            @dp.message_handler(state=states.work_trx_admin.sum_trx)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_hun(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['sum_trx'] = float(message.text)
                        data['user_id'] = int(data['user_id'])
                    betting = data['sum_trx']
                    user_db = await users.query.where(users.user_id == data['user_id']).gino.first()
                    bal_trx = user_db.bal_trx
                    username = user_db.name
                    if betting <= 10000:
                        if betting > 0:
                            await states.work_trx_admin.next()
                            await message.answer(_('👤 Kористувач <b><i>{}</i></b> {}\n\n💰 Його баланс становить - <b><i>{}</i></b> TRX\n\n💸 Поповнити на {} TRX\n\nБаланс буде становити - {}').format(data["user_id"], username, bal_trx, data["sum_trx"], bal_trx + data["sum_trx"]), parse_mode='html', reply_markup=kb.markup_work_balance_operation)
                        else:
                            await bot.send_message(message.chat.id, _('❌ Мінімальна сума поповнення <b><i>1</i></b> TRX ‼'), parse_mode='html')
                            await bot.send_message(message.chat.id, _('❌ Введіть іншу суму поповнення (або можете вийти з гри /cancel):'), parse_mode='html')
                    else:
                        await bot.send_message(message.chat.id, _('❌ Максимальна сума поповнення <b><i>10000</i></b> TRX ‼'), parse_mode='html')
                        await bot.send_message(message.chat.id, _('❌ Введіть іншу суму поповнення (або можете вийти з гри /cancel):'), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_start = await kb.markup_start(message)
                    await bot.send_message(message.chat.id, _('❌ Ви вийшли з режиму поповнення ‼'), reply_markup=markup_start, parse_mode='html')
                    await state.finish()


            @dp.callback_query_handler(text='next', state=states.work_trx_admin.accept)
            @dp.throttled(anti_flood, rate=1)
            async def start(call: types.callback_query, state: FSMContext):
                async with state.proxy() as data:
                    try:
                        user_id_text = int(data['user_id'])
                        sum_trx = float(data['sum_trx'])
                        await users.update.values(bal_trx=users.bal_trx + sum_trx).where(users.user_id == user_id_text).gino.status()
                        session.commit()
                        user_db = await users.query.where(users.user_id == user_id_text).gino.first()
                        bal_trx = user_db.bal_trx
                        markup_admin = await kb.markup_admin(call.message)
                        await call.message.answer(_('----------------------------------------------\n\n\nБаланс користувача <b><i>{}</i></b> поповнено на <b><u>{}</u></b> TRX\n\n\n\n💳 Його баланс становить - {} TRX\n\n\n----------------------------------------------').format(data["user_id"], sum_trx, bal_trx), reply_markup=markup_admin, parse_mode='html')
                        await state.finish()
                    except:
                        await call.message.answer(_("❌ Число введено некоректно ❗"), parse_mode='html')

            @dp.callback_query_handler(text='cancel', state=states.work_trx_admin.accept)
            @dp.throttled(anti_flood, rate=1)
            async def start(call: types.callback_query, state: FSMContext):
                markup_admin = await kb.markup_admin(call.message)
                await call.message.answer(_("❌ Ви відмінили поповнення ❗"), parse_mode='html', reply_markup=markup_admin)
                await state.finish()

        if call.data == 'work_admin_trx_del_select_trx':
            await states.work_trx_admin.user_id_del.set()
            await bot.send_message(call.message.chat.id, _('🔑 Введіть ID користувача (user_id)'), reply_markup=kb.markup_cancel)

            @dp.message_handler(state=states.work_trx_admin.user_id_del)
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        await states.work_trx_admin.user_id_del.set()
                        data['user_id'] = int(message.text)
                        user_db = await users.query.where(users.user_id == data['user_id']).gino.first()
                        bal_trx = user_db.bal_trx
                        bal_usd = user_db.bal_usd
                        username = user_db.name
                        await message.answer(_('👤 Kористувач <b><i>{}</i></b> {}\n\n💰 Його баланс становить - <b><i>{} TRX</i></b>| {} USDT\n\n↘ Оберіть суму що хочете додати із клавіатури або введіть її самі').format(data["user_id"], username, bal_trx, bal_usd), parse_mode='html', reply_markup=kb.markup_select_add_trx)
                        await states.work_trx_admin.next()
                except:
                    await message.answer(_("Це не число, або щось пішло не так.Ви можете натиснути на кнопку /cancel"))


            @dp.message_handler(state=states.work_trx_admin.sum_trx_del)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_hun(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['sum_trx_del'] = float(message.text)
                        data['user_id'] = int(data['user_id'])
                    user_db = await users.query.where(users.user_id == data['user_id']).gino.first()
                    bal_trx = user_db.bal_trx
                    username = user_db.name
                    betting = data['sum_trx_del']
                    if betting <= bal_trx:
                        if betting <= 10000:
                            if betting > 0:
                                await states.work_trx_admin.next()
                                await message.answer(_('👤 Kористувач <b><i>{}</i></b> {}\n\n💰 Його баланс становить - <b><i>{}</i></b> TRX\n\n💸 Зняти {} TRX\n\nБаланс буде становити - {}').format(data["user_id"], username, bal_trx, data["sum_trx_del"], bal_trx - data["sum_trx_del"]), parse_mode='html', reply_markup=kb.markup_work_balance_operation)
                            else:
                                await bot.send_message(message.chat.id, _('❌ Мінімальна сума зняття <b><i>1</i></b> TRX ‼'), parse_mode='html')
                                await bot.send_message(message.chat.id, _('❌ Введіть іншу суму зняття (або можете вийти з гри /cancel):'), parse_mode='html')
                        else:
                            await bot.send_message(message.chat.id, _('❌ Максимальна сума зняття <b><i>10000</i></b> TRX ‼'), parse_mode='html')
                            await bot.send_message(message.chat.id, _('❌ Введіть іншу суму зняття (або можете вийти з гри /cancel):'), parse_mode='html')
                    else:
                        await bot.send_message(message.chat.id, _('❌ Зняття більше балансу.\n\nБаланс - {}\n Зняття - {} ‼'.format(bal_trx, data['sum_trx'])), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_start = await kb.markup_start(message)
                    await bot.send_message(message.chat.id, _('❌ Ви вийшли з режиму зняття ‼'), reply_markup=markup_start, parse_mode='html')
                    await state.finish()


            @dp.callback_query_handler(text='next', state=states.work_trx_admin.accept_del)
            @dp.throttled(anti_flood, rate=1)
            async def start(call: types.callback_query, state: FSMContext):
                async with state.proxy() as data:
                    try:
                        user_id_text = int(data['user_id'])
                        sum_trx_del = float(data['sum_trx_del'])
                        await users.update.values(bal_trx=users.bal_trx - sum_trx_del).where(users.user_id == user_id_text).gino.status()
                        session.commit()
                        user_db = await users.query.where(users.user_id == user_id_text).gino.first()
                        bal_trx = user_db.bal_trx
                        markup_admin = await kb.markup_admin(call.message)
                        await call.message.answer(_('----------------------------------------------\n\n\nБаланс користувача <b><i>{}</i></b> зменшено на <b><u>{}</u></b> TRX\n\n\n\n💳 Його баланс становить - {} TRX\n\n\n----------------------------------------------').format(data["user_id"], sum_trx_del, bal_trx), reply_markup=markup_admin, parse_mode='html')
                        await state.finish()
                    except:
                        await call.message.answer(_("❌ Число введено некоректно ❗"), parse_mode='html')

            @dp.callback_query_handler(text='cancel', state=states.work_trx_admin.accept_del)
            @dp.throttled(anti_flood, rate=1)
            async def start(call: types.callback_query, state: FSMContext):
                markup_admin = await kb.markup_admin(call.message)
                await call.message.answer(_("❌ Ви відмінили зняття ❗"), parse_mode='html', reply_markup=markup_admin)
                await state.finish()

        if call.data == 'work_admin_usd':
            await call.message.edit_text(_('🛠 Оберіть операцію: '), parse_mode='html', reply_markup=kb.markup_work_admin_select_usd)

        if call.data == 'work_admin_add_usd':
            await states.work_usd_admin.user_id.set()
            await bot.send_message(call.message.chat.id, _('🔑 Введіть ID користувача (user_id)'), reply_markup=kb.markup_cancel)

            @dp.message_handler(state=states.work_usd_admin.user_id)
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        await states.work_usd_admin.user_id.set()
                        data['user_id'] = int(message.text)
                        user_db = await users.query.where(users.user_id == data['user_id']).gino.first()
                        bal_trx = user_db.bal_trx
                        bal_usd = user_db.bal_usd
                        username = user_db.name
                        await message.answer(_('👤 Kористувач <b><i>{}</i></b> {}\n\n💰 Його баланс становить - {} TRX | <b><i>{} USDT</i></b>\n\n↘ Оберіть суму що хочете додати із клавіатури або введіть її самі').format(data["user_id"], username, bal_trx, bal_usd), parse_mode='html', reply_markup=kb.markup_select_add_usdt)
                        await states.work_usd_admin.next()
                except:
                    await message.answer(_("Це не число, або щось пішло не так.Ви можете натиснути на кнопку /cancel"))

            @dp.message_handler(state=states.work_usd_admin.sum_trx)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_hun(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['sum_usd'] = float(message.text)
                        data['user_id'] = int(data['user_id'])
                    betting = data['sum_usd']
                    user_db = await users.query.where(users.user_id == data['user_id']).gino.first()
                    bal_usd = user_db.bal_usd
                    username = user_db.name
                    if betting <= 1000:
                        if betting > 0:
                            await states.work_usd_admin.next()
                            await message.answer(_('👤 Kористувач <b><i>{}</i></b> {}\n\n💰 Його баланс становить - <b><i>{}</i></b> USDT\n\n💸 Поповнити на {} USDT\n\nБаланс буде становити - {}').format(data["user_id"], username, bal_usd, data["sum_usd"], bal_usd + data["sum_usd"]), parse_mode='html', reply_markup=kb.markup_work_balance_operation)
                        else:
                            await bot.send_message(message.chat.id, _('❌ Мінімальна сума поповнення <b><i>1</i></b> USDT ‼'), parse_mode='html')
                            await bot.send_message(message.chat.id, _('❌ Введіть іншу суму поповнення (або можете вийти з гри /cancel):'), parse_mode='html')
                    else:
                        await bot.send_message(message.chat.id, _('❌ Максимальна сума поповнення <b><i>1000</i></b> USDT ‼'), parse_mode='html')
                        await bot.send_message(message.chat.id, _('❌ Введіть іншу суму поповнення (або можете вийти з гри /cancel):'), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_start = await kb.markup_start(message)
                    await bot.send_message(message.chat.id, _('❌ Ви вийшли з режиму поповнення ‼'), reply_markup=markup_start, parse_mode='html')
                    await state.finish()

            @dp.callback_query_handler(text='next', state=states.work_usd_admin.accept)
            @dp.throttled(anti_flood, rate=1)
            async def start(call: types.callback_query, state: FSMContext):
                async with state.proxy() as data:
                    try:
                        user_id_text = int(data['user_id'])
                        sum_usd = float(data['sum_usd'])
                        await users.update.values(bal_usd=users.bal_usd + sum_usd).where(users.user_id == user_id_text).gino.status()
                        session.commit()
                        user_db = await users.query.where(users.user_id == user_id_text).gino.first()
                        bal_usd = user_db.bal_usd
                        markup_admin = await kb.markup_admin(call.message)
                        await call.message.answer(_('----------------------------------------------\n\n\nБаланс користувача <b><i>{}</i></b> поповнено на <b><u>{}</u></b> USDT\n\n\n\n💳 Його баланс становить - {} USDT\n\n\n----------------------------------------------').format(data["user_id"], sum_usd, bal_usd), reply_markup=markup_admin, parse_mode='html')
                        await state.finish()
                    except:
                        await call.message.answer(_("❌ Число введено некоректно ❗"), parse_mode='html')

            @dp.callback_query_handler(text='cancel', state=states.work_usd_admin.accept)
            @dp.throttled(anti_flood, rate=1)
            async def start(call: types.callback_query, state: FSMContext):
                markup_admin = await kb.markup_admin(call.message)
                await call.message.answer(_("❌ Ви відмінили поповнення ❗"), parse_mode='html', reply_markup=markup_admin)
                await state.finish()

        if call.data == 'work_admin_del_usd':
            await states.work_usd_admin.user_id_del.set()
            await bot.send_message(call.message.chat.id, _('🔑 Введіть ID користувача (user_id)'), reply_markup=kb.markup_cancel)

            @dp.message_handler(state=states.work_usd_admin.user_id_del)
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        await states.work_usd_admin.user_id_del.set()
                        data['user_id'] = int(message.text)
                        user_db = await users.query.where(users.user_id == data['user_id']).gino.first()
                        bal_trx = user_db.bal_trx
                        bal_usd = user_db.bal_usd
                        username = user_db.name
                        await message.answer(_('👤 Kористувач <b><i>{}</i></b> {}\n\n💰 Його баланс становить - {} TRX | <b><i>{} USDT</i></b>\n\n↘ Оберіть суму що хочете зняти із клавіатури або введіть її самі').format(data["user_id"], username, bal_trx, bal_usd), parse_mode='html', reply_markup=kb.markup_select_add_usdt)
                        await states.work_usd_admin.next()
                except:
                    await message.answer(_("Це не число, або щось пішло не так.Ви можете натиснути на кнопку /cancel"))

            @dp.message_handler(state=states.work_usd_admin.sum_trx_del)
            @dp.throttled(anti_flood, rate=1)
            async def random_number_hun(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['sum_usd'] = float(message.text)
                        data['user_id'] = int(data['user_id'])
                    betting = data['sum_usd']
                    user_db = await users.query.where(users.user_id == data['user_id']).gino.first()
                    bal_usd = user_db.bal_usd
                    username = user_db.name
                    if data['sum_usd'] <= bal_usd:
                        if betting <= 1000:
                            if betting > 0:
                                await states.work_usd_admin.next()
                                await message.answer(_('👤 Kористувач <b><i>{}</i></b>\n\n💰 Його баланс становить - <b><i>{}</i></b> USDT\n\n💸 Зняти {} USDT\n\nБаланс буде становити - {}').format(data["user_id"], username, bal_usd, data["sum_usd"], bal_usd - data["sum_usd"]), parse_mode='html', reply_markup=kb.markup_work_balance_operation)
                            else:
                                await bot.send_message(message.chat.id, _('❌ Мінімальна сума зняття <b><i>1</i></b> USDT ‼'), parse_mode='html')
                                await bot.send_message(message.chat.id, _('❌ Введіть іншу суму зняття (або можете вийти з гри /cancel):'), parse_mode='html')
                        else:
                            await bot.send_message(message.chat.id, _('❌ Максимальна сума зняття <b><i>1000</i></b> USDT ‼'), parse_mode='html')
                            await bot.send_message(message.chat.id, _('❌ Введіть іншу суму зняття (або можете вийти з гри /cancel):'), parse_mode='html')
                    else:
                        await bot.send_message(message.chat.id, _('❌ Зняття більше балансу.\n\nБаланс - {}\n Зняття - {} ‼'.format(bal_usd, data['sum_usd'])), parse_mode='html')
                except:
                    await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                    markup_start = await kb.markup_start(message)
                    await bot.send_message(message.chat.id, _('❌ Ви вийшли з режиму зняття ‼'), reply_markup=markup_start, parse_mode='html')
                    await state.finish()

            @dp.callback_query_handler(text='next', state=states.work_usd_admin.accept_del)
            @dp.throttled(anti_flood, rate=1)
            async def start(call: types.callback_query, state: FSMContext):
                async with state.proxy() as data:
                    try:
                        user_id_text = int(data['user_id'])
                        sum_usd = float(data['sum_usd'])
                        await users.update.values(bal_usd=users.bal_usd - sum_usd).where(users.user_id == user_id_text).gino.status()
                        session.commit()
                        user_db = await users.query.where(users.user_id == user_id_text).gino.first()
                        bal_usd = user_db.bal_usd
                        markup_admin = await kb.markup_admin(call.message)
                        await call.message.answer(_('----------------------------------------------\n\n\nБаланс користувача <b><i>{}</i></b> знято <b><u>{}</u></b> USDT\n\n\n\n💳 Його баланс становить - {} USDT\n\n\n----------------------------------------------').format(data["user_id"], sum_usd, bal_usd), reply_markup=markup_admin, parse_mode='html')
                        await state.finish()
                    except:
                        await call.message.answer(_("❌ Число введено некоректно ❗"), parse_mode='html')

            @dp.callback_query_handler(text='cancel', state=states.work_usd_admin.accept_del)
            @dp.throttled(anti_flood, rate=1)
            async def start(call: types.callback_query, state: FSMContext):
                markup_admin = await kb.markup_admin(call.message)
                await call.message.answer(_("❌ Ви відмінили зняття ❗"), parse_mode='html', reply_markup=markup_admin)
                await state.finish()

        if call.data == 'say_hi_admin_kb_day' or call.data == 'say_hi_admin_kb_mon' or call.data == 'say_hi_admin_kb_yea' or call.data == 'say_hi_admin_kb_all':
            try:
                within_als = {
                    "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                    "mon": ('month', 'МІСЯЦЬ'),
                    "yea": ('year', 'РІК'),
                    "all": ('all', 'ВЕСЬ ЧАС'),
                }
                within = call.data[-3:]
                all_users = await db_commands.get_users()
                for user in all_users:
                    records = await db_commands.get_say_hi(user, within)
                    if (len(records)):
                        answer = (f"📖 Істория розсилок користувачів за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user}</code></b>\n")
                        for r in records:
                            answer += (f"<b><i>ID</i> = <code>{r.id}</code></b>\n\n")
                            answer += ("➕ " if r.acces != 0 else "➖ TEXT\n\n")
                            answer += f"{r.text_message}\n\n"
                            answer += f"\n🖼 PHOTO: <b><i>{r.photo}</i></b>  "
                            answer += f"\n🎹 AUDIO: <b><i>{r.audio}</i></b>  \n"
                            answer += f"\n🕐 {r.date}  "
                            if r.acces == 0:
                                answer += f"<b>❌ Не виконано</b>\n\n"
                            elif r.acces == 1:
                                answer += f"<b>✅ Виконано</b>\n\n"
                            else:
                                answer += f"<b>💢 Помилка виконання</b>\n\n"
                        await sleep(0.33)
                        await call.message.answer(answer, parse_mode='html')
                    else:
                        pass
                await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_say_hi_admin_kb)
            except:
                pass

        if call.data == 'say_hi_all_not_acces_admin':
            try:
                within_als = {
                    "day": ('today', 'day', 'СЬОГОДНІ', 'ДЕНЬ'),
                    "mon": ('month', 'МІСЯЦЬ'),
                    "yea": ('year', 'РІК'),
                    "all": ('all', 'ВЕСЬ ЧАС'),
                }
                within = 'all'
                all_users = await db_commands.get_users()
                for user in all_users:
                    records = await db_commands.get_say_hi(user, within)
                    if (len(records)):
                        answer = (f"📖 Істория розсилок користувачів за <b>{within_als[within][-1]}</b>.\n\n<b><i>USER_ID</i> = <code>{user}</code></b>\n")
                        for r in records:
                            if r.acces == 0:
                                answer += (f"<b><i>ID</i> = <code>{r.id}</code></b>\n\n")
                                answer += ("➕ " if r.acces != 0 else "➖ TEXT\n\n")
                                answer += f"{r.text_message}\n\n"
                                answer += f"\n🖼 PHOTO: <b><i>{r.photo}</i></b>  "
                                answer += f"\n🎹 AUDIO: <b><i>{r.audio}</i></b>  \n"
                                answer += f"\n🕐 {r.date}  "
                                if r.acces == 0:
                                    answer += f"<b>❌ Не виконано</b>\n\n"
                                elif r.acces == 1:
                                    answer += f"<b>✅ Виконано</b>\n\n"
                                else:
                                    answer += f"<b>💢 Помилка виконання</b>\n\n"
                            else:
                                pass
                        await sleep(0.33)
                        await call.message.answer(answer, parse_mode='html')
                    else:
                        pass
                await call.message.answer('Дані за різний період часу', parse_mode='html', reply_markup=kb.markup_say_hi_admin_kb)
            except:
                pass

        if call.data == 'say_hi_admin_kb_do_acces':
            await states.say_hi_admin_kb_do_acces.user_id.set()
            await bot.send_message(call.message.chat.id, f'🔑 Введіть ID запису (id)', reply_markup=kb.cancel_num, parse_mode='html')

            @dp.message_handler(state=states.say_hi_admin_kb_do_acces.user_id)
            @dp.throttled(anti_flood, rate=1)
            async def acces_say_hi_admin(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    data['user_id'] = int(message.text)
                    await bot.send_message(call.message.chat.id, _('Оберіть операцію'), parse_mode='html', reply_markup=kb.markup_cancel)
                await bot.send_message(call.message.chat.id, _('Оберіть операцію'), parse_mode='html', reply_markup=kb.markup_say_admin_kb_do_acces)
                await states.say_hi_admin_kb_do_acces.next()

            @dp.callback_query_handler(state=states.say_hi_admin_kb_do_acces.select)
            @dp.throttled(anti_flood, rate=1)
            async def acces_say_hi_admin(call: types.CallbackQuery, state: FSMContext):
                if call.data == 'say_admin_kb_do_acces_set_null':
                    try:
                        async with state.proxy() as data:
                            record_id = data['user_id']
                        say_db = await Say_model.query.where(Say_model.id == record_id).gino.first()
                        text_message = say_db.text_message
                        user_id = say_db.user_id
                        await Say_model.update.values(acces=0).where(Say_model.id == record_id).gino.status()
                        session.commit()
                        markup_admin = await kb.markup_admin(call.message)
                        await bot.send_message(call.message.chat.id, _('✅ Повідомлення: \n{}\n\n👤 Користувача: \n{}\n\n🔑 Запис: {}\n\n❌ ВІДМІНЕНО').format(text_message, user_id, record_id), parse_mode='html', reply_markup=markup_admin)
                        await state.finish()
                    except:
                        await bot.send_message(call.message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                        markup_games = await kb.markup_games(call.message)
                        await bot.send_message(call.message.chat.id, _("❌ Ви вийшли ‼"), reply_markup=markup_games, parse_mode='html')
                        await state.finish()
                elif call.data == 'say_admin_kb_do_acces_set_one':
                    try:
                        async with state.proxy() as data:
                            record_id = data['user_id']
                        say_db = await Say_model.query.where(Say_model.id == record_id).gino.first()
                        text_message = say_db.text_message
                        user_id = say_db.user_id
                        await Say_model.update.values(acces=1).where(Say_model.id == record_id).gino.status()
                        session.commit()
                        markup_admin = await kb.markup_admin(call.message)
                        await bot.send_message(call.message.chat.id, _('✅ Повідомлення: \n{}\n\n👤 Користувача: \n{}\n\n🔑 Запис: {}\n\n✅ ВИКОНАНО').format(text_message, user_id, record_id), parse_mode='html', reply_markup=markup_admin)
                        await state.finish()
                    except:
                        await bot.send_message(call.message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                        markup_games = await kb.markup_games(call.message)
                        await bot.send_message(call.message.chat.id, _("❌ Ви вийшли ‼"), reply_markup=markup_games, parse_mode='html')
                        await state.finish()
                if call.data == 'say_admin_kb_do_acces_set_two':
                    try:
                        async with state.proxy() as data:
                            record_id = data['user_id']
                        say_db = await Say_model.query.where(Say_model.id == record_id).gino.first()
                        text_message = say_db.text_message
                        user_id = say_db.user_id
                        await Say_model.update.values(acces=2).where(Say_model.id == record_id).gino.status()
                        session.commit()
                        markup_admin = await kb.markup_admin(call.message)
                        await bot.send_message(call.message.chat.id, _('✅ Повідомлення: \n{}\n\n👤 Користувача: \n{}\n\n🔑 Запис: {}\n\n💢 ПОСТАВЛЕНА ПОМИЛКА').format(text_message, user_id, record_id), parse_mode='html', reply_markup=markup_admin)
                        await state.finish()
                    except:
                        await bot.send_message(call.message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
                        markup_games = await kb.markup_games(call.message)
                        await bot.send_message(call.message.chat.id, _("❌ Ви вийшли ‼"), reply_markup=markup_games, parse_mode='html')
                        await state.finish()

        if call.data == 'work_admin_patreon':
            await call.message.edit_text(_('🛠 Оберіть операцію: '), parse_mode='html', reply_markup=kb.markup_work_admin_select_patreon)

        if call.data == 'work_admin_select_patreon':
            await states.work_patreon.patron.set()
            await bot.send_message(call.message.chat.id, '🔑 Введіть ID користувача (user_id)', reply_markup=kb.markup_cancel)

            @dp.message_handler(state=states.work_patreon.patron)
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    await states.work_patreon.patron.set()
                    data['user_id'] = int(message.text)
                    user_db = await users.query.where(users.user_id == data['user_id']).gino.first()
                    bal_trx = user_db.bal_trx
                    username = user_db.name
                    markup_admin = await kb.markup_admin(call.message)
                    await message.answer('ℹ Kористувач <b><i>{}</i></b> {}. Його баланс становить - <b><i>{}</i></b> TRX\n\n<b>👍 Тепер наш ПАТРОН !</b>'.format(data["user_id"], username, bal_trx), parse_mode='html', reply_markup=markup_admin)
                    await users.update.values(patron=1).where(users.user_id == data['user_id']).gino.status()
                    session.commit()
                    await state.finish()

        if call.data == 'work_admin_del_select_patreon':
            await states.work_patreon.unpatron.set()
            await bot.send_message(call.message.chat.id, '🔑 Введіть ID користувача (user_id)', reply_markup=kb.markup_cancel)

            @dp.message_handler(state=states.work_patreon.unpatron)
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    await states.work_patreon.unpatron.set()
                    data['user_id'] = int(message.text)
                    user_db = await users.query.where(users.user_id == data['user_id']).gino.first()
                    bal_trx = user_db.bal_trx
                    username = user_db.name
                    markup_admin = await kb.markup_admin(call.message)
                    await message.answer('ℹ Kористувач <b><i>{}</i></b> {}. Його баланс становить - <b><i>{}</i></b> TRX\n\n<b>👎 Тепер НЕ наш ПАТРОН !</b>'.format(data["user_id"], username, bal_trx), parse_mode='html', reply_markup=markup_admin)
                    await users.update.values(patron=0).where(users.user_id == data['user_id']).gino.status()
                    session.commit()
                    await state.finish()

        if call.data == 'work_admin_ban':
            await call.message.edit_text(_('🛠 Оберіть операцію: '), parse_mode='html', reply_markup=kb.markup_work_admin_select_ban)

        if call.data == 'work_admin_ban_select_ban':
            await states.work_ban.ban.set()
            await bot.send_message(call.message.chat.id, '🔑 Введіть ID користувача (user_id)', reply_markup=kb.markup_cancel)

            @dp.message_handler(state=states.work_ban.ban)
            async def answer(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    await states.work_ban.ban.set()
                    data['user_id'] = int(message.text)
                    user_db = await users.query.where(users.user_id == data['user_id']).gino.first()
                    bal_trx = user_db.bal_trx
                    username = user_db.name
                    markup_admin = await kb.markup_admin(call.message)
                    await message.answer('ℹ Kористувач <b><i>{}</i></b> {}. Його баланс становить - <b><i>{}</i></b> TRX\n\n<b>❌ Тепер ЗАБАНЕНО !</b>'.format(data["user_id"], username, bal_trx), parse_mode='html', reply_markup=markup_admin)
                    await users.update.values(ban=1).where(users.user_id == data['user_id']).gino.status()
                    session.commit()
                    await state.finish()

        if call.data == 'work_admin_unban_select_ban':
            await states.work_ban.unban.set()
            await bot.send_message(call.message.chat.id, '🔑 Введіть ID користувача (user_id)', reply_markup=kb.markup_cancel)

            @dp.message_handler(state=states.work_ban.unban)
            async def answer(message: types.Message, state: FSMContext):
                async with state.proxy() as data:
                    await states.work_ban.unban.set()
                    data['user_id'] = int(message.text)
                    user_db = await users.query.where(users.user_id == data['user_id']).gino.first()
                    bal_trx = user_db.bal_trx
                    username = user_db.name
                    markup_admin = await kb.markup_admin(call.message)
                    await message.answer('ℹ Kористувач <b><i>{}</i></b> {}. Його баланс становить - <b><i>{}</i></b> TRX\n\n<b>✅ Тепер НЕ ЗАБАНЕНО !</b>'.format(data["user_id"], username, bal_trx), parse_mode='html', reply_markup=markup_admin)
                    await users.update.values(ban=0).where(users.user_id == data['user_id']).gino.status()
                    session.commit()
                    await state.finish()

        if call.data == 'work_admin_info':
            await states.user_info.user_id.set()
            await bot.send_message(call.message.chat.id, '🔑 Введіть ID користувача (user_id)', reply_markup=kb.markup_cancel)

            @dp.message_handler(state=states.user_info.user_id)
            @dp.throttled(anti_flood, rate=1)
            async def answer(message: types.Message, state: FSMContext):
                try:
                    async with state.proxy() as data:
                        data['user_id'] = int(message.text)
                        user_db = await users.query.where(users.user_id == data['user_id']).gino.first()
                        user_id = data['user_id']
                        id = user_db.id
                        bal_trx = user_db.bal_trx
                        bal_usd = user_db.bal_usd
                        username = user_db.name
                        user_level = user_db.user_level
                        join_date = user_db.join_date
                        patron = user_db.patron
                        ban = user_db.ban
                        first = await db_commands.count_first_ref(user_id)
                        second = await db_commands.count_second_ref(user_id)
                        third = await db_commands.count_third_ref(user_id)
                        all = await db_commands.count_first_ref(user_id) + await db_commands.count_second_ref(user_id) + await db_commands.count_third_ref(user_id)
                        markup_admin = await kb.markup_admin(call.message)
                        await message.answer(_("ℹ Kористувач <b><i>{user_id}</i></b>. \n🔑 ID в базі: {id}\n\n🔤 Ім'я та логін: {username}\n\n🏅 Рівень аккаунту: {user_level}\n\n🅿️ Наш патрон: {patron}️\n\n💀 БАН: {ban}"
                                               "\n\n💳 Баланс: {bal_usd} USDT TRC20 | {bal_trx} TRX\n\n👤 Перший вхід: {join_date}\n\n🚀 Всього рефералів: {all}\n➖ 1 лінія: {first}\n➖ 2 лінія: {second}\n➖ 3 лінія: {third}")
                                             .format(user_id=user_id, id=id, username = username, user_level = user_level, patron=patron, ban=ban, join_date=join_date, bal_usd=bal_usd, bal_trx=bal_trx, all=all, first=first, second=second, third=third)
                                             , parse_mode='html', reply_markup=markup_admin)
                        await state.finish()
                except:
                    await message.answer(_("❌ Не коректно введено user_id. Або такого користувача в базі немає\n\nℹ Ви можете вийти через команду: /cancel"))
    else:
        await call.message.answer(_('❗ Ваш аккаунт ЗАБАНЕНО !\n\n💭 Якщо виникли якісь питання, звертайтесь у тех.підтримку: @Christooo1'), reply_markup=types.ReplyKeyboardRemove())


