from aiogram.dispatcher import FSMContext
from sqlalchemy import func

from config import dp, bot, _
from aiogram import types
import keyboards as kb
from db_api import db_quick_commands
from db_api.schemas.paymants import Paymants_model
from db_api.schemas.users import Users_model as users
from settings import session
from .states import pay_operation


@dp.message_handler(state=pay_operation.del_trx)
async def get_sum(message: types.Message, state: FSMContext):
    try:
        user = await users.query.where(users.user_id == message.from_user.id).gino.first()
        bal_trx_db = user.bal_trx
        wallet_trx_db = user.wallet_trx
        count = await Paymants_model.query.where((Paymants_model.user_id == message.from_user.id) & (Paymants_model.del_trx > 0) & (Paymants_model.acces == 0)).with_only_columns([func.count()]).gino.scalar()
        async with state.proxy() as data:
            data['del_trx'] = float(message.text)
            if count < 2:
                if (data['del_trx'] <= bal_trx_db):
                    if(data['del_trx'] >= 100):
                        await pay_operation.next()
                        if wallet_trx_db == '0':
                            await bot.send_message(message.chat.id, _("✍ Введіть адресу вашого гаманця TRX"), reply_markup=kb.markup_cancel, parse_mode='html')
                        else:
                            markup_save_wallet_trx = types.ReplyKeyboardMarkup(resize_keyboard=True ,row_width=1)
                            save_wallet_trx = types.KeyboardButton(f'{wallet_trx_db}')
                            save_wallet_trx_cancel = types.KeyboardButton(f'/cancel')
                            markup_save_wallet_trx.add(save_wallet_trx, save_wallet_trx_cancel)
                            await bot.send_message(message.chat.id, _("✍ Введіть адресу вашого гаманця TRX\n\nАбо оберіть останній використаний гаманець"), reply_markup=markup_save_wallet_trx, parse_mode='html')
                    else:
                        markup_start = await kb.markup_start(message)
                        await bot.send_message(message.chat.id, _("❌ Мінімальна сума виводу = 100 TRX❕"), reply_markup=markup_start, parse_mode='html')
                        await bot.send_message(message.chat.id, _("❌ Операція скасована ‼"), parse_mode='html')
                        await state.finish()
                else:
                    markup_start = await kb.markup_start(message)
                    await bot.send_message(message.chat.id, _("❌ Недостатньо коштів"), reply_markup=markup_start, parse_mode='html')
                    await bot.send_message(message.chat.id, _("❌ Операція скасована ‼"), parse_mode='html')
                    await state.finish()
            else:
                markup_start = await kb.markup_start(message)
                await bot.send_message(message.chat.id, _("❌ Можна поставити тільки дві операції одночасно"), reply_markup=markup_start,parse_mode='html')
                await bot.send_message(message.chat.id, _("❌ Операція скасована ‼"), parse_mode='html')
                await state.finish()
    except:
        markup_start = await kb.markup_start(message)
        await bot.send_message(message.chat.id, _("❌ Число введене не коректно ❗"), reply_markup=markup_start, parse_mode='html')
        await bot.send_message(message.chat.id, _("❌ Операція скасована ‼"), parse_mode='html')
        await state.finish()

@dp.message_handler(state=pay_operation.add_trx)
async def get_sum_trx(message: types.Message, state: FSMContext):
    try:
        user = await users.query.where(users.user_id == message.from_user.id).gino.first()
        bal_trx_db = user.bal_trx
        bal_usd_db = user.bal_usd
        wallet_trx_db = user.wallet_trx
        wallet_usd_db = user.wallet_usdt
        count = await Paymants_model.query.where((Paymants_model.user_id == message.from_user.id) & (Paymants_model.add_trx > 0) & (Paymants_model.acces == 0)).with_only_columns([func.count()]).gino.scalar()
        async with state.proxy() as data:
            data['add_trx'] = float(message.text)
            if count < 2:
                if (data['add_trx'] >= 100):
                    await pay_operation.next()
                    if wallet_trx_db == '0':
                        await bot.send_message(message.chat.id, _("✍ Введіть адресу вашого гаманця TRX"), reply_markup=kb.markup_cancel, parse_mode='html')
                    else:
                        markup_save_wallet_trx = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                        save_wallet_trx = types.KeyboardButton(f'{wallet_trx_db}')
                        save_wallet_trx_cancel = types.KeyboardButton(f'/cancel')
                        markup_save_wallet_trx.add(save_wallet_trx, save_wallet_trx_cancel)
                        await bot.send_message(message.chat.id, _("✍ Введіть адресу вашого гаманця TRX\n\nАбо оберіть останній використаний гаманець"), reply_markup=markup_save_wallet_trx, parse_mode='html')
                else:
                    markup_start = await kb.markup_start(message)
                    await bot.send_message(message.chat.id, _("❌ Мінімальна сума поповнення = 100 TRX❕"), reply_markup=markup_start, parse_mode='html')
                    await bot.send_message(message.chat.id, _("❌ Операція скасована ‼"), parse_mode='html')
                    await state.finish()
            else:
                markup_start = await kb.markup_start(message)
                await bot.send_message(message.chat.id, _("❌ Можна поставити тільки дві операції одночасно"), reply_markup=markup_start,parse_mode='html')
                await bot.send_message(message.chat.id, _("❌ Операція скасована ‼"), parse_mode='html')
                await state.finish()

    except:
        markup_start = await kb.markup_start(message)
        await bot.send_message(message.chat.id, _("❌ Число введене не коректно ❗"), reply_markup=markup_start, parse_mode='html')
        await bot.send_message(message.chat.id, _("❌ Операція скасована ‼"), parse_mode='html')
        await state.finish()


@dp.message_handler(state=pay_operation.add_usd)
async def get_sum_trx(message: types.Message, state: FSMContext):
    try:
        user = await users.query.where(users.user_id == message.from_user.id).gino.first()
        bal_trx_db = user.bal_trx
        bal_usd_db = user.bal_usd
        wallet_trx_db = user.wallet_trx
        wallet_usd_db = user.wallet_usdt
        count = await Paymants_model.query.where((Paymants_model.user_id == message.from_user.id) & (Paymants_model.add_usd > 0) & (Paymants_model.acces == 0)).with_only_columns([func.count()]).gino.scalar()
        async with state.proxy() as data:
            data['add_usd'] = float(message.text)
            if count < 2:
                if (data['add_usd'] >= 10):
                    await pay_operation.next()
                    if wallet_usd_db == '0':
                        await bot.send_message(message.chat.id, _("✉ Введіть адресу вашого гаманця USDT 📩"), reply_markup=kb.markup_cancel, parse_mode='html')
                    else:
                        markup_save_wallet_usdt = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                        save_wallet_usdt = types.KeyboardButton(f'{wallet_usd_db}')
                        save_wallet_trx_cancel = types.KeyboardButton(f'/cancel')
                        markup_save_wallet_usdt.add(save_wallet_usdt, save_wallet_trx_cancel)
                        await bot.send_message(message.chat.id, _("✍ Введіть адресу вашого гаманця USDT\n\nАбо оберіть останній використаний гаманець"), reply_markup=markup_save_wallet_usdt, parse_mode='html')
                else:
                    markup_start = await kb.markup_start(message)
                    await bot.send_message(message.chat.id, _("❌ Мінімальна сума поповнення = 10 USDT❕"), reply_markup=markup_start, parse_mode='html')
                    await bot.send_message(message.chat.id, _("❌ Операція скасована ‼"), parse_mode='html')
                    await state.finish()
            else:
                markup_start = await kb.markup_start(message)
                await bot.send_message(message.chat.id, _("❌ Можна поставити тільки дві операції одночасно"), reply_markup=markup_start,parse_mode='html')
                await bot.send_message(message.chat.id, _("❌ Операція скасована ‼"), parse_mode='html')
                await state.finish()

    except:
        markup_start = await kb.markup_start(message)
        await bot.send_message(message.chat.id, _("❌ Число введене не коректно ❗"), reply_markup=markup_start, parse_mode='html')
        await bot.send_message(message.chat.id, _("❌ Операція скасована ‼"), parse_mode='html')
        await state.finish()


@dp.message_handler(state=pay_operation.del_trx_get_adress)
async def get_adress_sum(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            ID = message.from_user.id
            data['id_del_trx'] = ID
            data['del_trx_get_adress'] = message.text
            a = data['del_trx_get_adress']
            b = data['del_trx']

        await db_quick_commands.add_del_trx(state)
        if message.text != '/cancel':
            markup_start = await kb.markup_start(message)
            await bot.send_message(message.chat.id, _("📌 Ви створили вивід <b><i>{}</i></b> TRX на гаманець: \n<b><i>{}</i></b>\n\nВаша заявка прийнята, і буде успішно опрацьована протягом 72 годин ⌛ , якщо кошти не прийшли , то напишіть у службу підтримки").format(b, a), reply_markup=markup_start, parse_mode='html')
            markup_succes = await kb.markup_succes(message)
            await bot.send_message(message.chat.id, _("✅ Операція зареєстрована Успішно!"), reply_markup=markup_succes, parse_mode='html')
            await users.update.values(bal_trx=users.bal_trx - b).where(users.user_id == message.from_user.id).gino.status()
            await users.update.values(wallet_trx=a).where(users.user_id == message.from_user.id).gino.status()
            session.commit()
            await state.finish()
        else:
            markup_start = await kb.markup_start(message)
            await bot.send_message(message.chat.id, _("❌ Ви відмінили вивід!"), reply_markup=markup_start, parse_mode='html')
            await state.finish()
        await Paymants_model.delete.where(Paymants_model.adress == '/cancel').gino.status()
        session.commit()
    except:
        await bot.send_message(message.chat.id, _("❌ Помилка ❗\n\nПри будь-яких питаннях звертайтесь до нашого менеджера: @Christooo1"), parse_mode='html')
        await state.finish()


@dp.message_handler(state=pay_operation.add_trx_get_adress)
async def get_adress_sum_(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            ID = message.from_user.id
            data['id_del_trx'] = ID
            data['add_trx_get_adress'] = message.text
            a = data['add_trx_get_adress']
            b = data['add_trx']

        await db_quick_commands.add_add_trx(state)
        if message.text != '/cancel':
            markup_start = await kb.markup_start(message)
            await bot.send_message(message.chat.id, _("📌 Ви створили поповнення <b><i>{}</i></b> TRX на гаманець: \n<b><i>{}</i></b>\n\nВаша заявка прийнята, і буде успішно опрацьована протягом 72 годин ⌛ , якщо кошти не прийшли , то напишіть у службу підтримки").format(b, a), reply_markup=markup_start, parse_mode='html')
            markup_succes = await kb.markup_succes(message)
            await bot.send_message(message.chat.id, _("✅ Операція зареєстрована Успішно!"), reply_markup=markup_succes, parse_mode='html')
            await users.update.values(wallet_trx=a).where(users.user_id == message.from_user.id).gino.status()
            session.commit()
            await state.finish()
        else:
            markup_start = await kb.markup_start(message)
            await bot.send_message(message.chat.id, _("❌ Ви відмінили поповнення!"), reply_markup=markup_start, parse_mode='html')
            await state.finish()
        await Paymants_model.delete.where(Paymants_model.adress == '/cancel').gino.status()
        session.commit()
    except:
        await bot.send_message(message.chat.id, _("❌ Помилка ❗\n\nПри будь-яких питаннях звертайтесь до нашого менеджера: @Christooo1"), parse_mode='html')
        await state.finish()


@dp.message_handler(state=pay_operation.add_usd_get_adress)
async def get_adress_sum__(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            ID = message.from_user.id
            data['id_del_trx'] = ID
            data['add_usd_get_adress'] = message.text
            a = data['add_usd_get_adress']
            b = data['add_usd']

        await db_quick_commands.add_add_usd(state)
        if message.text != '/cancel':
            markup_start = await kb.markup_start(message)
            await bot.send_message(message.chat.id, _("📌 Ви створили поповнення <b><i>{}</i></b> USD на гаманець: \n<b><i>{}</i></b>\n\nВаша заявка прийнята, і буде успішно опрацьована протягом 72 годин ⌛ , якщо кошти не прийшли , то напишіть у службу підтримки").format(b, a), reply_markup=markup_start, parse_mode='html')
            markup_succes = await kb.markup_succes(message)
            await bot.send_message(message.chat.id, _("✅ Операція зареєстрована Успішно!"), reply_markup=markup_succes, parse_mode='html')
            await users.update.values(wallet_usdt=a).where(users.user_id == message.from_user.id).gino.status()
            session.commit()
            await state.finish()
        else:
            markup_start = await kb.markup_start(message)
            await bot.send_message(message.chat.id, _("❌ Ви відмінили поповнення!"), reply_markup=markup_start, parse_mode='html')
            await state.finish()
        await Paymants_model.delete.where(Paymants_model.adress == '/cancel').gino.status()
        session.commit()
    except:
        await bot.send_message(message.chat.id, _("❌ Помилка ❗\n\nПри будь-яких питаннях звертайтесь до нашого менеджера: @Christooo1"), parse_mode='html')
        await state.finish()
