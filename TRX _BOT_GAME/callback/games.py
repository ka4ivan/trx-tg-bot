# import random
# from datetime import datetime, timedelta
# import asyncio
#
# from asyncio import sleep
#
# from aiogram import types
# from aiogram.dispatcher import FSMContext
# from db_api.schemas.achievement import Achievement_model as achivement
# from db_api.schemas.paymants import Paymants_model
# from db_api.schemas.users import Users_model as users
# from db_api.schemas.bonus import Bonus_model as Bonus
# from db_api.schemas.promo_code import Promo_model as Promo
# from db_api.schemas.promo_code_count import Promo_count_model as Promo_count
# from db_api import db_quick_commands as db_commands
# from config import dp, bot, _
# import keyboards as kb
# from handlers import states
# from handlers.states import say_hi, pay_operation
# from language_middleware import get_lang
# from settings import session, CHANNELS
#
#
# async def anti_flood(*args, **kwargs):
#     m = args[0]
#     await m.answer('One mess per second, pls')
#
#
# @dp.callback_query_handler()
# @dp.throttled(anti_flood, rate=1)
# async def callback_guess(call: types.callback_query):
#
#     ban_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#     ban = ban_db.ban
#     if ban == 0:
#
#         if call.data == 'again_guess_five':
#             await states.guess_number.bet_five.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#         if call.data == 'again_guess_ten':
#             await states.guess_number.bet_ten.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#         if call.data == 'again_guess_hun':
#             await states.guess_number.bet_hun.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#         if call.data == 'again_fifty_two':
#             await states.fifty_fifty.bet_two.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#         if call.data == 'again_fifty_four':
#                 await states.fifty_fifty.bet_four.set()
#                 user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#                 bal_trx = user_db.bal_trx
#                 await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#         if call.data == 'again_dice_classic':
#             await states.dice.bet_classic.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#         if call.data == 'again_dice_under':
#             await states.dice.bet_under.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#         if call.data == 'again_br_case':
#             await states.cases.case_br_buy.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             markup_accept_cases = await kb.markup_accept_cases(call.message)
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=markup_accept_cases, parse_mode='html')
#
#         if call.data == 'again_si_case':
#             await states.cases.case_si_buy.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             markup_accept_cases = await kb.markup_accept_cases(call.message)
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=markup_accept_cases, parse_mode='html')
#
#         if call.data == 'again_go_case':
#             await states.cases.case_go_buy.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             markup_accept_cases = await kb.markup_accept_cases(call.message)
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=markup_accept_cases, parse_mode='html')
#
#         if call.data == 'again_miner_three':
#             await states.miner.bet_three.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#         if call.data == 'again_miner_five':
#             await states.miner.bet_five.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#         if call.data == 'again_miner_seven':
#             await states.miner.bet_seven.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#         if call.data == 'again_slot':
#             await states.spin.bet_spin.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#
#         if call.data == 'five_num_guess_game':
#             num_game = 5
#             await states.guess_number.bet_five.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#             @dp.message_handler(state=states.guess_number.bet_five)
#             @dp.throttled(anti_flood, rate=1)
#             async def random_number_five(message: types.Message, state: FSMContext):
#                 try:
#                     async with state.proxy() as data:
#                         data['bet_five'] = float(message.text)
#                     betting = data['bet_five']
#                     if betting <= 1000:
#                         if betting > 0:
#                             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#                             bal_trx_bet = user_db.bal_trx
#                             if betting <= bal_trx_bet:
#                                 await states.guess_number.next()
#                                 await bot.send_message(message.chat.id, _("Загадано число від 1 до {}. Спробуй вгадати").format(num_game),reply_markup=kb.markup_select_rand_num_five)
#                             else:
#                                 await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
#                                 await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                         else:
#                             await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
#                             await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
#                         await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
#                 except:
#                     await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
#                     await state.finish()
#
#             @dp.message_handler(state=states.guess_number.random_number_five)
#             @dp.throttled(anti_flood, rate=1)
#             async def answer(message: types.Message, state: FSMContext):
#                 async with state.proxy() as data:
#                     await states.guess_number.random_number_five.set()
#                     data['random_number_five'] = random.randint(1, num_game)
#                 try:
#                     betting = data['bet_five']
#                     await achivement.update.values(game_num=achivement.game_num + 1).where(achivement.user_id == message.chat.id).gino.status()
#                     session.commit()
#                     if int(message.text) >= 1 and int(message.text) <= num_game:
#                         if int(message.text) == data['random_number_five']:
#                             await users.update.values(bal_trx=users.bal_trx + betting * 3.95).where(users.user_id == message.chat.id).gino.status()
#                             session.commit()
#                             anim_num = random.sample(range(1, num_game), 3)
#                             for rand_anim in anim_num:
#                                 await asyncio.sleep(0.5)
#                                 await message.answer(_("❓ Випадає число: ") + '<b>' + str(rand_anim) + '</b> ❓', parse_mode='html')
#                             markup_games = await kb.markup_games(message)
#                             await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(betting * 4.95), reply_markup=markup_games)
#                             markup_again_guess_five = await kb.markup_again_guess_five(message)
#                             user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_five']), reply_markup=markup_again_guess_five, parse_mode='html')
#                             await state.finish()
#                         else:
#                             await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == message.chat.id).gino.status()
#                             session.commit()
#                             anim_num = random.sample(range(1, num_game), 3)
#                             for rand_anim in anim_num:
#                                 await asyncio.sleep(0.5)
#                                 await message.answer(_("❓ Випадає число: ") + '<b>' + str(rand_anim) + '</b> ❓', parse_mode='html')
#                             markup_games = await kb.markup_games(message)
#                             await message.answer(_("----------------------------------------------\n\n\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
#                             markup_again_guess_five = await kb.markup_again_guess_five(message)
#                             user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_five']), reply_markup=markup_again_guess_five,parse_mode='html')
#                             await state.finish()
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Діапазон чисел <b><i>від 1 до {} включно</i></b>‼".format(num_game)), parse_mode='html')
#                         await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
#                 except:
#                     await message.answer(_("❌ Число введене не коректно ❗\n\nВведіть цифру <b><i>від 1 до {} включно</i></b>!!".format(num_game)), reply_markup=kb.markup_select_rand_num_five, parse_mode='html')
#
#         if call.data == 'ten_num_guess_game':
#             num_game = 10
#             await states.guess_number.bet_ten.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format( bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#             @dp.message_handler(state=states.guess_number.bet_ten)
#             @dp.throttled(anti_flood, rate=1)
#             async def random_number_ten(message: types.Message, state: FSMContext):
#                 try:
#                     async with state.proxy() as data:
#                         data['bet_ten'] = float(message.text)
#                     betting = data['bet_ten']
#                     if betting <= 1000:
#                         if betting > 0:
#                             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#                             bal_trx_bet = user_db.bal_trx
#                             if betting <= bal_trx_bet:
#                                 await states.guess_number.next()
#                                 await bot.send_message(message.chat.id, _("Загадано число від 1 до {}. Спробуй вгадати").format(num_game), reply_markup=kb.markup_select_rand_num_ten)
#                             else:
#                                 await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
#                                 await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                         else:
#                             await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
#                             await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
#                         await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
#                 except:
#                     await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
#                     await state.finish()
#
#             @dp.message_handler(state=states.guess_number.random_number_ten)
#             @dp.throttled(anti_flood, rate=1)
#             async def answer(message: types.Message, state: FSMContext):
#                 async with state.proxy() as data:
#                     await states.guess_number.random_number_ten.set()
#                     data['random_number_ten'] = random.randint(1, num_game)
#                 try:
#                     betting = data['bet_ten']
#                     await achivement.update.values(game_num=achivement.game_num + 1).where(achivement.user_id == message.chat.id).gino.status()
#                     session.commit()
#                     if int(message.text) >= 1 and int(message.text) <= num_game:
#                         if int(message.text) == data['random_number_ten']:
#                             await users.update.values(bal_trx=users.bal_trx + betting * 8.9).where(users.user_id == message.chat.id).gino.status()
#                             session.commit()
#                             anim_num = random.sample(range(1, num_game), 3)
#                             for rand_anim in anim_num:
#                                 await asyncio.sleep(0.5)
#                                 await message.answer(_("❓ Випадає число: ") + '<b>' + str(rand_anim) + '</b> ❓', parse_mode='html')
#                             markup_games = await kb.markup_games(message)
#                             await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(betting * 9.9), reply_markup=markup_games)
#                             markup_again_guess_ten = await kb.markup_again_guess_ten(message)
#                             user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_ten']), reply_markup=markup_again_guess_ten,parse_mode='html')
#                             await state.finish()
#                         else:
#                             await users.update.values(bal_trx=users.bal_trx - betting).where(
#                                 users.user_id == message.chat.id).gino.status()
#                             session.commit()
#                             anim_num = random.sample(range(1, num_game), 3)
#                             for rand_anim in anim_num:
#                                 await asyncio.sleep(0.5)
#                                 await message.answer(_("❓ Випадає число: ") + '<b>' + str(rand_anim) + '</b> ❓', parse_mode='html')
#                             markup_games = await kb.markup_games(message)
#                             await message.answer(_("----------------------------------------------\n\n\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
#                             markup_again_guess_ten = await kb.markup_again_guess_ten(message)
#                             user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_ten']), reply_markup=markup_again_guess_ten, parse_mode='html')
#                             await state.finish()
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Діапазон чисел <b><i>від 1 до {} включно</i></b>‼".format(num_game)), parse_mode='html')
#                         await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
#                 except:
#                     await message.answer(_("❌ Число введене не коректно ❗\n\nВведіть цифру <b><i>від 1 до {} включно</i></b>!!".format(num_game)), reply_markup=kb.markup_select_rand_num_ten, parse_mode='html')
#
#         if call.data == 'hun_num_guess_game':
#             num_game = 100
#             await states.guess_number.bet_hun.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format( bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#             @dp.message_handler(state=states.guess_number.bet_hun)
#             @dp.throttled(anti_flood, rate=1)
#             async def random_number_hun(message: types.Message, state: FSMContext):
#                 try:
#                     async with state.proxy() as data:
#                         data['bet_hun'] = float(message.text)
#                     betting = data['bet_hun']
#                     if betting <= 1000:
#                         if betting > 0:
#                             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#                             bal_trx_bet = user_db.bal_trx
#                             if betting <= bal_trx_bet:
#                                 await states.guess_number.next()
#                                 await bot.send_message(message.chat.id, _("Загадано число від 1 до {}. Спробуй вгадати").format(num_game), reply_markup=kb.markup_select_rand_num_hun)
#                             else:
#                                 await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
#                                 await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                         else:
#                             await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
#                             await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
#                         await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
#                 except:
#                     await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
#                     await state.finish()
#
#             @dp.message_handler(state=states.guess_number.random_number_hun)
#             @dp.throttled(anti_flood, rate=1)
#             async def answer(message: types.Message, state: FSMContext):
#                 async with state.proxy() as data:
#                     await states.guess_number.random_number_hun.set()
#                     data['random_number_hun'] = random.randint(1, num_game)
#                 try:
#                     betting = data['bet_hun']
#                     await achivement.update.values(game_num=achivement.game_num + 1).where(achivement.user_id == message.chat.id).gino.status()
#                     session.commit()
#                     if int(message.text) >= 1 and int(message.text) <= num_game:
#                         if int(message.text) == data['random_number_hun']:
#                             await users.update.values(bal_trx=users.bal_trx + betting * 94).where(users.user_id == message.chat.id).gino.status()
#                             session.commit()
#                             anim_num = random.sample(range(1, num_game), 3)
#                             for rand_anim in anim_num:
#                                 await asyncio.sleep(0.5)
#                                 await message.answer(_("❓ Випадає число: ") + '<b>' + str(rand_anim) + '</b> ❓', parse_mode='html')
#                             markup_games = await kb.markup_games(message)
#                             await achivement.update.values(game_num_win_hun=achivement.game_num_win_hun + 1).where(achivement.user_id == message.chat.id).gino.status()
#                             await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(betting * 95), reply_markup=markup_games)
#                             markup_again_guess_hun = await kb.markup_again_guess_hun(message)
#                             user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_hun']), reply_markup=markup_again_guess_hun,parse_mode='html')
#                             await state.finish()
#                         else:
#                             await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == message.chat.id).gino.status()
#                             session.commit()
#                             anim_num = random.sample(range(1, num_game), 3)
#                             for rand_anim in anim_num:
#                                 await asyncio.sleep(0.5)
#                                 await message.answer(_("❓ Випадає число: ") + '<b>' + str(rand_anim) + '</b> ❓', parse_mode='html')
#                             markup_games = await kb.markup_games(message)
#                             await message.answer(_("----------------------------------------------\n\n\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
#                             markup_again_guess_hun = await kb.markup_again_guess_hun(message)
#                             user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <b><i><u>{}</u></i></b>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_hun']), reply_markup=markup_again_guess_hun, parse_mode='html')
#                             await state.finish()
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Діапазон чисел <b><i>від 1 до {} включно</i></b>‼".format(num_game)), parse_mode='html')
#                         await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
#                 except:
#                     await message.answer(_("❌ Число введене не коректно ❗\n\nВведіть цифру <b><i>від 1 до {} включно</i></b>!!".format(num_game)), reply_markup=kb.markup_select_rand_num_hun, parse_mode='html')
#
#         if call.data == 'two_num_fifty_game':
#             num_game = 2
#             await states.fifty_fifty.bet_two.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#             @dp.message_handler(state=states.fifty_fifty.bet_two)
#             @dp.throttled(anti_flood, rate=1)
#             async def random_number_two(message: types.Message, state: FSMContext):
#                 try:
#                     async with state.proxy() as data:
#                         data['bet_two'] = float(message.text)
#                     betting = data['bet_two']
#                     if betting <= 1000:
#                         if betting > 0:
#                             user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             if betting <= bal_trx:
#                                 await states.fifty_fifty.next()
#                                 await bot.send_message(message.chat.id, _("Загадано число від 1 до {}. Спробуй вгадати".format(num_game)), reply_markup=kb.markup_select_fifty_two)
#                             else:
#                                 await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
#                                 await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                         else:
#                             await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
#                             await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
#                         await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                 except:
#                     await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
#                     await state.finish()
#
#             @dp.message_handler(state=states.fifty_fifty.random_number_two)
#             @dp.throttled(anti_flood, rate=1)
#             async def answer(message: types.Message, state: FSMContext):
#                 async with state.proxy() as data:
#                     await states.fifty_fifty.random_number_two.set()
#                     data['random_number_two'] = random.randint(1, num_game)
#                 try:
#                     betting = data['bet_two']
#                     if int(message.text) >= 1 and int(message.text) <= num_game:
#                         anim_num_f = random.randint(1, num_game)
#                         anim_num_s = random.randint(1, num_game)
#                         anim_num_t = random.randint(1, num_game)
#                         await asyncio.sleep(0.5)
#                         await message.answer(_("❓ Випадає число: ") + '<b>' + str(
#                             anim_num_f) + '</b> ❓', parse_mode='html')
#                         await asyncio.sleep(0.5)
#                         await message.answer(_("❓ Випадає число: ") + '<b>' + str(
#                             anim_num_s) + '</b> ❓', parse_mode='html')
#                         await asyncio.sleep(0.5)
#                         await message.answer(_("❓ Випадає число: ") + '<b>' + str(
#                             anim_num_t) + '</b> ❓', parse_mode='html')
#                         if int(message.text) == data['random_number_two']:
#                             await achivement.update.values(game_fifty=achivement.game_fifty + 1).where(achivement.user_id == message.chat.id).gino.status()
#                             await users.update.values(bal_trx=users.bal_trx + betting * 0.95).where(users.user_id == message.chat.id).gino.status()
#                             session.commit()
#                             user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             markup_games = await kb.markup_games(message)
#                             await message.answer("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX".format(betting * 1.95), reply_markup=markup_games)
#                             markup_again_fifty_two = await kb.markup_again_fifty_two(message)
#                             await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_two']), reply_markup=markup_again_fifty_two, parse_mode='html')
#                             await state.finish()
#                         else:
#                             await achivement.update.values(game_fifty=achivement.game_fifty + 1).where(achivement.user_id == message.chat.id).gino.status()
#                             await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == message.chat.id).gino.status()
#                             session.commit()
#                             user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             markup_games = await kb.markup_games(message)
#                             await message.answer(_("----------------------------------------------\n\n\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
#                             markup_again_fifty_two = await kb.markup_again_fifty_two(message)
#                             await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_two']), reply_markup=markup_again_fifty_two, parse_mode='html')
#                             await state.finish()
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Діапазон чисел <b><i>від 1 до {} включно</i></b>‼".format(num_game)), parse_mode='html')
#                         await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
#                 except:
#                     await message.answer(_("❌ Число введене некоректно ❗\n\nВведіть цифру <b><i>від 1 до {} включно</i></b>!!".format(num_game)), reply_markup=kb.markup_select_fifty_two, parse_mode='html')
#
#         if call.data == 'four_num_fifty_game':
#             num_game = 4
#             await states.fifty_fifty.bet_four.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format( bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#             @dp.message_handler(state=states.fifty_fifty.bet_four)
#             @dp.throttled(anti_flood, rate=1)
#             async def random_number_four(message: types.Message, state: FSMContext):
#                 try:
#                     async with state.proxy() as data:
#                         data['bet_four'] = float(message.text)
#                     betting = data['bet_four']
#                     if betting <= 1000:
#                         if betting > 0:
#                             user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             if betting <= bal_trx:
#                                 await states.fifty_fifty.next()
#                                 await bot.send_message(message.chat.id, _("Загадано число від 1 до {}. Спробуй вгадати".format(num_game)), reply_markup=kb.markup_select_fifty_four)
#                             else:
#                                 await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
#                                 await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                         else:
#                             await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
#                             await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
#                         await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                 except:
#                     await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
#                     await state.finish()
#
#             @dp.message_handler(state=states.fifty_fifty.random_number_four)
#             @dp.throttled(anti_flood, rate=1)
#             async def answer(message: types.Message, state: FSMContext):
#                 async with state.proxy() as data:
#                     await states.fifty_fifty.random_number_four.set()
#                     data['random_number_four_first'] = random.randint(1, num_game)
#                     data['random_number_four_second'] = random.randint(1, num_game)
#                     if data['random_number_four_first'] == data['random_number_four_second']:
#                         data['random_number_four_second'] = random.randint(1, num_game)
#                     if data['random_number_four_first'] == data['random_number_four_second']:
#                         data['random_number_four_second'] = random.randint(1, num_game)
#                     if data['random_number_four_first'] == data['random_number_four_second']:
#                         data['random_number_four_second'] = random.randint(1, num_game)
#                     try:
#                         betting = data['bet_four']
#                         if int(message.text) >= 1 and int(message.text) <= num_game:
#                             anim_num = random.sample(range(1, 5), 3)
#                             for rand_anim in anim_num:
#                                 await asyncio.sleep(0.5)
#                                 await message.answer(_("❓ Випадає число: ") + '<b>' + str(rand_anim) + '</b> ❓', parse_mode='html')
#                             if int(message.text) == data['random_number_four_first'] or int(message.text) == data['random_number_four_second']:
#                                 if int(message.text) == data['random_number_four_first'] and int(message.text) == data['random_number_four_second']:
#                                     await achivement.update.values(game_fifty=achivement.game_fifty + 1).where(achivement.user_id == message.chat.id).gino.status()
#                                     await users.update.values(bal_trx=users.bal_trx + betting * 2.9).where(users.user_id == message.chat.id).gino.status()
#                                     session.commit()
#                                     markup_games = await kb.markup_games(message)
#                                     await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли із множителем х2!\n\n💶 Ви виграли - {} TRX").format(betting * 3.9), reply_markup=markup_games)
#                                 else:
#                                     await achivement.update.values(game_fifty=achivement.game_fifty + 1).where(achivement.user_id == message.chat.id).gino.status()
#                                     await users.update.values(bal_trx=users.bal_trx + betting * 0.95).where(users.user_id == message.chat.id).gino.status()
#                                     session.commit()
#                                     markup_games = await kb.markup_games(message)
#                                     await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(betting * 1.95), reply_markup=markup_games)
#                                 user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                                 bal_trx = user_db.bal_trx
#                                 markup_again_fifty_four = await kb.markup_again_fifty_four(message)
#                                 await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <u><b><i>{}</i></b></u>\n🔢 <i>Загадане число було</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_four_first'], data['random_number_four_second']), reply_markup=markup_again_fifty_four, parse_mode='html')
#                                 await state.finish()
#                             else:
#                                 await achivement.update.values(game_fifty=achivement.game_fifty + 1).where(achivement.user_id == message.chat.id).gino.status()
#                                 await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == message.chat.id).gino.status()
#                                 session.commit()
#                                 user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                                 bal_trx = user_db.bal_trx
#                                 markup_games = await kb.markup_games(message)
#                                 await message.answer(_("----------------------------------------------\n\n\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
#                                 markup_again_fifty_four = await kb.markup_again_fifty_four(message)
#                                 await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Загадане число було</i>: <u><b><i>{}</i></b></u>\n🔢 <i>Загадане число було</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_four_first'],data['random_number_four_second']), reply_markup=markup_again_fifty_four,parse_mode='html')
#                                 await state.finish()
#                         else:
#                             await bot.send_message(message.chat.id, "❌ Діапазон чисел <b><i>від 1 до {} включно</i></b>‼".format(num_game), parse_mode='html')
#                             await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
#                     except:
#                         await message.answer(_("❌ Число введене некоректно ❗\n\nВведіть цифру <b><i>від 1 до {} включно</i></b>!!".format(num_game)), reply_markup=kb.markup_select_fifty_four, parse_mode='html')
#
#         if call.data == 'classic_dice_game':
#             await states.dice.bet_classic.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#             @dp.message_handler(state=states.dice.bet_classic)
#             @dp.throttled(anti_flood, rate=1)
#             async def random_number_classic(message: types.Message, state: FSMContext):
#                 try:
#                     async with state.proxy() as data:
#                         data['bet_classic'] = float(message.text)
#                     betting = data['bet_classic']
#                     if betting <= 1000:
#                         if betting > 0:
#                             user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             if betting <= bal_trx:
#                                 await states.dice.next()
#                                 await bot.send_message(message.chat.id, _("Кубик готовий до гри, оберіть ваше значення:"), reply_markup=kb.markup_select_dice_classic)
#                             else:
#                                 await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
#                                 await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                         else:
#                             await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
#                             await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
#                         await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                 except:
#                     await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
#                     await state.finish()
#
#             @dp.message_handler(state=states.dice.random_number_classic)
#             @dp.throttled(anti_flood, rate=1)
#             async def answer(message: types.Message, state: FSMContext):
#                 async with state.proxy() as data:
#                     await states.dice.random_number_classic.set()
#                     data['random_number_classic'] = await bot.send_dice(message.chat.id)
#                     data['random_number_classic'] = data['random_number_classic']['dice']['value']
#                 try:
#                     betting = data['bet_classic']
#                     await asyncio.sleep(4)
#                     if int(message.text) >= 1 and int(message.text) <= 6:
#                         if int(message.text) == data['random_number_classic']:
#                             await achivement.update.values(game_dice=achivement.game_dice + 1).where(achivement.user_id == message.chat.id).gino.status()
#                             await users.update.values(bal_trx=users.bal_trx + betting * 4.8).where(users.user_id == message.chat.id).gino.status()
#                             session.commit()
#                             user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             markup_games = await kb.markup_games(message)
#                             await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(betting * 5.8), reply_markup=markup_games)
#                             markup_again_dice_classic = await kb.markup_again_dice_classic(message)
#                             await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Випало число</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_classic']), reply_markup=markup_again_dice_classic, parse_mode='html')
#                             await state.finish()
#                         else:
#                             await achivement.update.values(game_dice=achivement.game_dice + 1).where(achivement.user_id == message.chat.id).gino.status()
#                             await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == message.chat.id).gino.status()
#                             session.commit()
#                             user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             markup_games = await kb.markup_games(message)
#                             await message.answer(_("----------------------------------------------\n\n\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
#                             markup_again_dice_classic = await kb.markup_again_dice_classic(message)
#                             await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Випало число</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_classic']), reply_markup=markup_again_dice_classic, parse_mode='html')
#                             await state.finish()
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Діапазон чисел <b><i>від 1 до 6 включно</i></b>‼"), parse_mode='html', reply_markup=kb.markup_select_dice_classic)
#                         await bot.send_message(message.chat.id, _("❌ Введіть інше число: "), parse_mode='html')
#                 except:
#                     await message.answer(_("❌ Число введене не коректно ❗\n\nВведіть цифру <b><i>від 1 до 6 включно</i></b>!!"), reply_markup=kb.markup_select_dice_classic, parse_mode='html')
#
#         if call.data == 'under_s_game':
#             await states.dice.bet_under.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#             @dp.message_handler(state=states.dice.bet_under)
#             @dp.throttled(anti_flood, rate=1)
#             async def random_number_under(message: types.Message, state: FSMContext):
#                 try:
#                     async with state.proxy() as data:
#                         data['bet_under'] = float(message.text)
#                     betting = data['bet_under']
#                     if betting <= 1000:
#                         if betting > 0:
#                             user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             if betting <= bal_trx:
#                                 await states.dice.next()
#                                 markup_select_dice_under = await kb.markup_select_dice_under(message)
#                                 await bot.send_message(message.chat.id, _("Кубик готовий до гри, оберіть ваше значення:"), reply_markup=markup_select_dice_under)
#                             else:
#                                 await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
#                                 await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                         else:
#                             await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
#                             await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
#                         await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                 except:
#                     await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.chat.id, "❌ Ви вийшли з гри ‼", reply_markup=markup_games, parse_mode='html')
#                     await state.finish()
#
#             @dp.message_handler(state=states.dice.random_number_under)
#             @dp.throttled(anti_flood, rate=1)
#             async def answer(message: types.Message, state: FSMContext):
#                 async with state.proxy() as data:
#                     await states.dice.random_number_under.set()
#                     data['random_number_under_first'] = await bot.send_dice(message.chat.id)
#                     data['random_number_under_second'] = await bot.send_dice(message.chat.id)
#                     if data['random_number_under_first']['dice']['value'] + data['random_number_under_second']['dice'][
#                         'value'] < 7:
#                         data['random_number_under'] = '(x2)\n🎲⬇7️⃣'
#                     elif data['random_number_under_first']['dice']['value'] + \
#                             data['random_number_under_second']['dice']['value'] == 7:
#                         data['random_number_under'] = '(x5.8)\n🎲🟰7️⃣'
#                     elif data['random_number_under_first']['dice']['value'] + \
#                             data['random_number_under_second']['dice']['value'] > 7:
#                         data['random_number_under'] = '(x2)\n🎲⬆7️⃣'
#                     else:
#                         markup_games = await kb.markup_games(message)
#                         await message.answer(f'Error', reply_markup=markup_games)
#                     try:
#                         betting = data['bet_under']
#                         await asyncio.sleep(4)
#                         if message.text == '(x2)\n🎲⬇7️⃣' or message.text == '(x5.8)\n🎲🟰7️⃣' or message.text == '(x2)\n🎲⬆7️⃣':
#                             if message.text == data['random_number_under']:
#                                 if data['random_number_under_first']['dice']['value'] + data['random_number_under_second']['dice']['value'] == 7:
#                                     await achivement.update.values(game_dice=achivement.game_dice + 1).where(achivement.user_id == message.chat.id).gino.status()
#                                     await users.update.values(bal_trx=users.bal_trx + betting * 4.8).where(users.user_id == message.chat.id).gino.status()
#                                     session.commit()
#                                     markup_games = await kb.markup_games(message)
#                                     await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(betting * 5.8), reply_markup=markup_games)
#                                 else:
#                                     await achivement.update.values(game_dice=achivement.game_dice + 1).where(achivement.user_id == message.chat.id).gino.status()
#                                     await users.update.values(bal_trx=users.bal_trx + betting).where(users.user_id == message.chat.id).gino.status()
#                                     session.commit()
#                                     markup_games = await kb.markup_games(message)
#                                     await message.answer(_("----------------------------------------------\n\n\n❤ Вітаю! Ви перемогли!\n\n💶 Ви виграли - {} TRX").format(betting * 2), reply_markup=markup_games)
#                                 user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
#                                 bal_trx = user_db.bal_trx
#                                 markup_again_dice_under = await kb.markup_again_dice_under(message)
#                                 await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Випало число</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_under']), reply_markup=markup_again_dice_under, parse_mode='html')
#                                 await state.finish()
#                             else:
#                                 await achivement.update.values(game_dice=achivement.game_dice + 1).where(achivement.user_id == message.chat.id).gino.status()
#                                 await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == message.chat.id).gino.status()
#                                 session.commit()
#                                 user_db = await users.query.where(users.user_id == message.chat.id).gino.first()
#                                 bal_trx = user_db.bal_trx
#                                 markup_games = await kb.markup_games(message)
#                                 await message.answer(_("----------------------------------------------\n\n\n💔 Нажаль ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
#                                 markup_again_dice_under = await kb.markup_again_dice_under(message)
#                                 await message.answer(_("💳 Ваш баланс - {} TRX\n\n🔢 <i>Випало число</i>: <u><b><i>{}</i></b></u>\n\n\n----------------------------------------------").format(bal_trx, data['random_number_under']), reply_markup=markup_again_dice_under, parse_mode='html')
#                                 await state.finish()
#                         else:
#                             markup_select_dice_under = await kb.markup_select_dice_under(message)
#                             await bot.send_message(message.chat.id, _("❌ Відповідь введена не коректно‼"), parse_mode='html', reply_markup=markup_select_dice_under)
#                             await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                     except:
#                         markup_select_dice_under = await kb.markup_select_dice_under(message)
#                         await message.answer(_("❌ Відповідь введена не коректно ❗\n\nНапишіть самі, або оберіть відповідь із клавіатури!!"), parse_mode='html', reply_markup=markup_select_dice_under)
#
#         if call.data == 'miner_three_game':
#             await states.miner.bet_three.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#             @dp.message_handler(state=states.miner.bet_three)
#             @dp.throttled(anti_flood, rate=1)
#             async def random_number_three(message: types.Message, state: FSMContext):
#                 try:
#                     async with state.proxy() as data:
#                         data['bet_three'] = float(message.text)
#                     betting = data['bet_three']
#                     if betting <= 1000:
#                         if betting > 0:
#                             user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             if betting <= bal_trx:
#                                 await states.miner.next()
#                                 random.shuffle(kb.list_buts)
#                                 markup = types.InlineKeyboardMarkup()
#                                 for text, data in kb.list_buts:
#                                     markup.insert(types.InlineKeyboardButton(text=text, callback_data=data))
#                                 await bot.send_message(message.chat.id, _("Де немає бомби?"), reply_markup=markup)
#                             else:
#                                 await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
#                                 await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                         else:
#                             await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
#                             await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
#                         await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                 except:
#                     await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
#                     await state.finish()
#
#             @dp.callback_query_handler(state=states.miner.random_number_three)
#             @dp.throttled(anti_flood, rate=1)
#             async def answer(call: types.CallbackQuery, state: FSMContext):
#                 async with state.proxy() as data:
#                     betting = data['bet_three']
#                 try:
#                     await call.message.answer("_🟡_", parse_mode='html')
#                     await asyncio.sleep(0.7)
#                     await call.message.answer("_💣_", parse_mode='html')
#                     await asyncio.sleep(0.7)
#                     if call.data == 'field_1' or call.data == 'field_2' or call.data == 'field_3' or call.data == 'field_4' or call.data == 'field_5' or call.data == 'field_6':
#                         await call.message.answer("👍", parse_mode='html')
#                         await asyncio.sleep(0.7)
#                         await achivement.update.values(game_mine=achivement.game_mine + 1).where(achivement.user_id == call.message.chat.id).gino.status()
#                         await users.update.values(bal_trx=users.bal_trx + betting * 0.7).where(users.user_id == call.message.chat.id).gino.status()
#                         markup_games = await kb.markup_games(call.message)
#                         await call.message.answer(_("----------------------------------------------\n\n\n❤ Бомба знешкоджена. Вітаю!\n\n💶 Ви виграли - {} TRX").format(betting * 1.7), reply_markup=markup_games)
#                         user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#                         bal_trx = user_db.bal_trx
#                         markup_again_miner_three = await kb.markup_again_miner_three(call.message)
#                         await call.message.answer(_("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_miner_three, parse_mode='html')
#                         await call.answer()
#                         await state.finish()
#                     else:
#                         await call.message.answer("💥", parse_mode='html')
#                         await asyncio.sleep(0.7)
#                         await achivement.update.values(game_mine=achivement.game_mine + 1).where(achivement.user_id == call.message.chat.id).gino.status()
#                         await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == call.message.chat.id).gino.status()
#                         session.commit()
#                         markup_games = await kb.markup_games(call.message)
#                         await call.message.answer(_("----------------------------------------------\n\n\n💔 Бомба зірвалась. Ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
#                         user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#                         bal_trx = user_db.bal_trx
#                         markup_again_miner_three = await kb.markup_again_miner_three(call.message)
#                         await call.message.answer(_("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_miner_three, parse_mode='html')
#                         await call.answer()
#                         await state.finish()
#                 except:
#                     await call.message.answer(_("❌ Значення введене не коректно ❗\n\nОберіть поле зі <b><i>списку</i></b>"), parse_mode='html')
#
#         if call.data == 'miner_five_game':
#             await states.miner.bet_five.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#             @dp.message_handler(state=states.miner.bet_five)
#             @dp.throttled(anti_flood, rate=1)
#             async def random_number_five(message: types.Message, state: FSMContext):
#                 try:
#                     async with state.proxy() as data:
#                         data['bet_five'] = float(message.text)
#                     betting = data['bet_five']
#                     if betting <= 1000:
#                         if betting > 0:
#                             user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             if betting <= bal_trx:
#                                 await states.miner.next()
#                                 random.shuffle(kb.list_buts)
#                                 markup = types.InlineKeyboardMarkup()
#                                 for text, data in kb.list_buts:
#                                     markup.insert(types.InlineKeyboardButton(text=text, callback_data=data))
#                                 await bot.send_message(message.chat.id, _("Де немає бомби?"), reply_markup=markup)
#                             else:
#                                 await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
#                                 await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                         else:
#                             await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
#                             await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
#                         await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                 except:
#                     await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
#                     await state.finish()
#
#             @dp.callback_query_handler(state=states.miner.random_number_five)
#             @dp.throttled(anti_flood, rate=1)
#             async def answer(call: types.CallbackQuery, state: FSMContext):
#                 async with state.proxy() as data:
#                     betting = data['bet_five']
#                 try:
#                     await call.message.answer("_🟡_", parse_mode='html')
#                     await asyncio.sleep(0.7)
#                     await call.message.answer("_💣_", parse_mode='html')
#                     await asyncio.sleep(0.7)
#                     if call.data == 'field_1' or call.data == 'field_2' or call.data == 'field_3' or call.data == 'field_4':
#                         await call.message.answer("👍", parse_mode='html')
#                         await asyncio.sleep(0.7)
#                         await achivement.update.values(game_mine=achivement.game_mine + 1).where(achivement.user_id == call.message.chat.id).gino.status()
#                         await users.update.values(bal_trx=users.bal_trx + betting * 1).where(users.user_id == call.message.chat.id).gino.status()
#                         markup_games = await kb.markup_games(call.message)
#                         await call.message.answer(_("----------------------------------------------\n\n\n❤ Бомба знешкоджена. Вітаю!\n\n💶 Ви виграли - {} TRX").format(betting * 2), reply_markup=markup_games)
#                         user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#                         bal_trx = user_db.bal_trx
#                         markup_again_miner_five = await kb.markup_again_miner_five(call.message)
#                         await call.message.answer(_("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_miner_five, parse_mode='html')
#                         await call.answer()
#                         await state.finish()
#                     else:
#                         await call.message.answer("💥", parse_mode='html')
#                         await asyncio.sleep(0.7)
#                         await achivement.update.values(game_mine=achivement.game_mine + 1).where(achivement.user_id == call.message.chat.id).gino.status()
#                         await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == call.message.chat.id).gino.status()
#                         session.commit()
#                         markup_games = await kb.markup_games(call.message)
#                         await call.message.answer(_("----------------------------------------------\n\n\n💔 Бомба зірвалась. Ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
#                         user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#                         bal_trx = user_db.bal_trx
#                         markup_again_miner_five = await kb.markup_again_miner_five(call.message)
#                         await call.message.answer(_("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_miner_five, parse_mode='html')
#                         await call.answer()
#                         await state.finish()
#                 except:
#                     await call.message.answer(_("❌ Значення введене не коректно ❗\n\nОберіть поле зі <b><i>списку</i></b>"), parse_mode='html')
#
#         if call.data == 'miner_seven_game':
#             await states.miner.bet_seven.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#             @dp.message_handler(state=states.miner.bet_seven)
#             @dp.throttled(anti_flood, rate=1)
#             async def random_number_seven(message: types.Message, state: FSMContext):
#                 try:
#                     async with state.proxy() as data:
#                         data['bet_seven'] = float(message.text)
#                     betting = data['bet_seven']
#                     if betting <= 1000:
#                         if betting > 0:
#                             user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             if betting <= bal_trx:
#                                 await states.miner.next()
#                                 random.shuffle(kb.list_buts)
#                                 markup = types.InlineKeyboardMarkup()
#                                 for text, data in kb.list_buts:
#                                     markup.insert(types.InlineKeyboardButton(text=text, callback_data=data))
#                                 await bot.send_message(message.chat.id, _("Де немає бомби?"), reply_markup=markup)
#                             else:
#                                 await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
#                                 await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                         else:
#                             await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
#                             await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
#                         await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                 except:
#                     await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
#                     await state.finish()
#
#             @dp.callback_query_handler(state=states.miner.random_number_seven)
#             @dp.throttled(anti_flood, rate=1)
#             async def answer(call: types.CallbackQuery, state: FSMContext):
#                 async with state.proxy() as data:
#                     betting = data['bet_seven']
#                 try:
#                     await call.message.answer("_🟡_", parse_mode='html')
#                     await asyncio.sleep(0.7)
#                     await call.message.answer("_💣_", parse_mode='html')
#                     await asyncio.sleep(0.7)
#                     if call.data == 'field_1' or call.data == 'field_2':
#                         await call.message.answer("👍", parse_mode='html')
#                         await asyncio.sleep(0.7)
#                         await achivement.update.values(game_mine=achivement.game_mine + 1).where(achivement.user_id == call.message.chat.id).gino.status()
#                         await users.update.values(bal_trx=users.bal_trx + betting * 3.5).where(users.user_id == call.message.chat.id).gino.status()
#                         session.commit()
#                         markup_games = await kb.markup_games(call.message)
#                         await call.message.answer(_("----------------------------------------------\n\n\n❤ Бомба знешкоджена. Вітаю!\n\n💶 Ви виграли - {} TRX").format(betting * 4.5), reply_markup=markup_games)
#                         user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#                         bal_trx = user_db.bal_trx
#                         markup_again_miner_seven = await kb.markup_again_miner_seven(call.message)
#                         await call.message.answer(_("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_miner_seven, parse_mode='html')
#                         await call.answer()
#                         await state.finish()
#                     else:
#                         await call.message.answer("💥", parse_mode='html')
#                         await asyncio.sleep(0.7)
#                         await achivement.update.values(game_mine=achivement.game_mine + 1).where(achivement.user_id == call.message.chat.id).gino.status()
#                         await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == call.message.chat.id).gino.status()
#                         session.commit()
#                         markup_games = await kb.markup_games(call.message)
#                         await call.message.answer(_("----------------------------------------------\n\n\n💔 Бомба зірвалась. Ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
#                         user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#                         bal_trx = user_db.bal_trx
#                         markup_again_miner_seven = await kb.markup_again_miner_seven(call.message)
#                         await call.message.answer(_("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_miner_seven, parse_mode='html')
#                         await call.answer()
#                         await state.finish()
#                 except:
#                     await call.message.answer(_("❌ Значення введене не коректно ❗\n\nОберіть поле зі <b><i>списку</i></b>"), parse_mode='html')
#
#         if call.data == 'br_case_game':
#             await states.cases.case_br_buy.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n.\n.\n.\n.\n.").format(bal_trx), parse_mode='html')
#             markup_accept_cases = await kb.markup_accept_cases(call.message)
#             await bot.send_message(call.message.chat.id, _("Ви дійсно хочете купити даний кейс за <b><i>10</i></b> TRX ?"), reply_markup=markup_accept_cases, parse_mode='html')
#
#             @dp.callback_query_handler(state=states.cases.case_br_buy, text_contains='accept_case_game')
#             @dp.throttled(anti_flood, rate=1)
#             async def answer(message: types.Message, state: FSMContext):
#                 user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                 bal_trx = user_db.bal_trx
#                 if bal_trx >= 10:
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.from_user.id, _("Ви купили кейс 📦"), reply_markup=markup_games, parse_mode='html')
#                     anim_num = random.sample(range(5, 15), 3)
#                     for rand_anim in anim_num:
#                         await asyncio.sleep(0.5)
#                         await bot.send_message(message.from_user.id, _("❓ Ви виграли: ") + '<b>' + str(rand_anim) + ' TRX</b> ❓', parse_mode='html')
#                     cash = random.randint(5, 15)
#                     if cash >= 13:
#                         cash = random.randint(5, 15)
#                     await achivement.update.values(game_case=achivement.game_case + 1).where(achivement.user_id == message.from_user.id).gino.status()
#                     await users.update.values(bal_trx=users.bal_trx + cash - 10).where(users.user_id == message.from_user.id).gino.status()
#                     session.commit()
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.from_user.id, _("----------------------------------------------\n\n\n❤ Вітаю!\n💶 Ви виграли - {} TRX").format(cash), reply_markup=markup_games)
#                     user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                     bal_trx = user_db.bal_trx
#                     markup_again_br_case = await kb.markup_again_br_case(message)
#                     await bot.send_message(message.from_user.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_br_case, parse_mode='html')
#                     await state.finish()
#                 else:
#                     await bot.send_message(message.from_user.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
#                     await state.finish()
#
#         if call.data == 'si_case_game':
#             await states.cases.case_si_buy.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n.\n.\n.\n.\n.").format(bal_trx), parse_mode='html')
#             markup_accept_cases = await kb.markup_accept_cases(call.message)
#             await bot.send_message(call.message.chat.id, _("Ви дійсно хочете купити даний кейс за <b><i>100</i></b> TRX ?"), reply_markup=markup_accept_cases, parse_mode='html')
#
#             @dp.callback_query_handler(state=states.cases.case_si_buy, text_contains='accept_case_game')
#             @dp.throttled(anti_flood, rate=1)
#             async def answer(message: types.Message, state: FSMContext):
#                 user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                 bal_trx = user_db.bal_trx
#                 if bal_trx >= 100:
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.from_user.id, _("Ви купили кейс 🎒"), reply_markup=markup_games, parse_mode='html')
#                     anim_num = random.sample(range(50, 150), 3)
#                     for rand_anim in anim_num:
#                         await asyncio.sleep(0.5)
#                         await bot.send_message(message.from_user.id, _("❓ Ви виграли: ") + '<b>' + str(rand_anim) + ' TRX</b> ❓', parse_mode='html')
#                     cash = random.randint(50, 150)
#                     if cash >= 135:
#                         cash = random.randint(50, 150)
#                     await achivement.update.values(game_case=achivement.game_case + 1).where(achivement.user_id == message.from_user.id).gino.status()
#                     await users.update.values(bal_trx=users.bal_trx + cash - 100).where(users.user_id == message.from_user.id).gino.status()
#                     session.commit()
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.from_user.id, _("----------------------------------------------\n\n\n❤ Вітаю!\n💶 Ви виграли - {} TRX").format(cash), reply_markup=markup_games)
#                     user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                     bal_trx = user_db.bal_trx
#                     markup_again_si_case = await kb.markup_again_si_case(message)
#                     await bot.send_message(message.from_user.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_si_case, parse_mode='html')
#                     await state.finish()
#                 else:
#                     await bot.send_message(message.from_user.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
#                     await state.finish()
#
#         if call.data == 'go_case_game':
#             await states.cases.case_go_buy.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n.\n.\n.\n.\n.").format(bal_trx), parse_mode='html')
#             markup_accept_cases = await kb.markup_accept_cases(call.message)
#             await bot.send_message(call.message.chat.id, _("Ви дійсно хочете купити даний кейс за <b><i>1000</i></b> TRX ?"), reply_markup=markup_accept_cases, parse_mode='html')
#
#             @dp.callback_query_handler(state=states.cases.case_go_buy, text_contains='accept_case_game')
#             @dp.throttled(anti_flood, rate=1)
#             async def answer(message: types.Message, state: FSMContext):
#                 user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                 bal_trx = user_db.bal_trx
#                 if bal_trx >= 1000:
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.from_user.id, _("Ви купили кейс 💼"), reply_markup=markup_games, parse_mode='html')
#                     anim_num = random.sample(range(0, 1500), 3)
#                     for rand_anim in anim_num:
#                         await asyncio.sleep(0.5)
#                         await bot.send_message(message.from_user.id, _("❓ Ви виграли: ") + '<b>' + str(rand_anim) + ' TRX</b> ❓', parse_mode='html')
#                     cash = random.randint(0, 1500)
#                     if cash >= 1350:
#                         cash = random.randint(0, 1500)
#                     await achivement.update.values(game_case=achivement.game_case + 1).where(achivement.user_id == message.from_user.id).gino.status()
#                     await users.update.values(bal_trx=users.bal_trx + cash - 1000).where(users.user_id == message.from_user.id).gino.status()
#                     session.commit()
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.from_user.id, _("----------------------------------------------\n\n\n❤ Вітаю!\n💶 Ви виграли - {} TRX").format(cash), reply_markup=markup_games)
#                     user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                     bal_trx = user_db.bal_trx
#                     markup_again_go_case = await kb.markup_again_go_case(message)
#                     await bot.send_message(message.from_user.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_go_case, parse_mode='html')
#                     await state.finish()
#                 else:
#                     await bot.send_message(message.from_user.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
#                     await state.finish()
#
#         if call.data == 'accept_spin':
#             await states.spin.bet_spin.set()
#             user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#             bal_trx = user_db.bal_trx
#             await bot.send_message(call.message.chat.id, _("\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\n.\nЩоб вийти з гри  /cancel\n.\n.\n.\n.\n.\n💳 <i>Ваш баланс</i> - <i><b>{}</b></i> TRX\n\n↘ Оберіть ставку із клавіатури або введіть її самі ↙\n💎 <i><b><u>Введіть ставку</u></b></i>:\n.\n.\n.\n.\n.").format(bal_trx), reply_markup=kb.markup_select_bet, parse_mode='html')
#
#             @dp.message_handler(state=states.spin.bet_spin)
#             @dp.throttled(anti_flood, rate=1)
#             async def random_number_spin(message: types.Message, state: FSMContext):
#                 try:
#                     async with state.proxy() as data:
#                         data['bet_spin'] = float(message.text)
#                     betting = data['bet_spin']
#                     if betting <= 1000:
#                         if betting > 0:
#                             user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                             bal_trx = user_db.bal_trx
#                             if betting <= bal_trx:
#                                 await bot.send_message(message.chat.id, _("Автомат готовий до гри"))
#                                 async with state.proxy() as data:
#                                     await states.spin.random_number_spin.set()
#                                     markup_games = await kb.markup_games(message)
#                                     data['random_number_spin'] = await message.answer_dice(emoji="🎰", reply_markup=markup_games)
#                                     data['random_number_spin'] = data['random_number_spin']['dice']['value']
#                                 try:
#                                     betting = data['bet_spin']
#                                     await asyncio.sleep(2)
#                                     await achivement.update.values(game_slot=achivement.game_slot + 1).where(achivement.user_id == message.from_user.id).gino.status()
#                                     session.commit()
#                                     if data['random_number_spin'] in (1, 22, 43):  # три в ряд без сімок
#                                         await users.update.values(bal_trx=users.bal_trx + betting * 3).where(users.user_id == message.from_user.id).gino.status()
#                                         session.commit()
#                                         markup_games = await kb.markup_games(message)
#                                         await bot.send_message(_("----------------------------------------------\n\n\n❤ Вітаю!\n\n💶 Ви виграли - {} TRX").format(betting * 3), reply_markup=markup_games)
#                                         user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                                         bal_trx = user_db.bal_trx
#                                         markup_again_slot = await kb.markup_again_slot(message)
#                                         await bot.send_message(message.chat.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_slot, parse_mode='html')
#                                         await state.finish()
#                                     elif data['random_number_spin'] in (16, 32, 48):  # дві сімки на початку
#                                         await users.update.values(bal_trx=users.bal_trx + betting * 4).where(users.user_id == message.from_user.id).gino.status()
#                                         session.commit()
#                                         markup_games = await kb.markup_games(message)
#                                         await bot.send_message(message.chat.id, _("----------------------------------------------\n\n\n❤ Вітаю!\n\n💶 Ви виграли - {} TRX").format(betting * 5), reply_markup=markup_games)
#                                         user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                                         bal_trx = user_db.bal_trx
#                                         markup_again_slot = await kb.markup_again_slot(message)
#                                         await bot.send_message(message.chat.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_slot, parse_mode='html')
#                                         await state.finish()
#                                     # два співпадіння
#                                     elif data['random_number_spin'] in (2, 3, 4, 5, 6, 9, 13, 17, 33, 49, 18, 21, 23, 24, 26, 30, 38, 54, 11, 27, 35, 39, 41, 42, 44, 47, 59, 52, 56, 60, 61, 62, 63):
#                                         await users.update.values(bal_trx=users.bal_trx - betting * 0.7).where(users.user_id == message.from_user.id).gino.status()
#                                         session.commit()
#                                         markup_games = await kb.markup_games(message)
#                                         await bot.send_message(message.chat.id, _("----------------------------------------------\n\n\n❤ Вітаю!\n\n💶 Ви виграли - {} TRX").format(betting * 0.3), reply_markup=markup_games)
#                                         user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                                         bal_trx = user_db.bal_trx
#                                         markup_again_slot = await kb.markup_again_slot(message)
#                                         await bot.send_message(message.chat.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_slot, parse_mode='html')
#                                         await state.finish()
#                                     elif data['random_number_spin'] == 64:  # три сімки
#                                         await users.update.values(bal_trx=users.bal_trx + betting * 14).where(users.user_id == message.from_user.id).gino.status()
#                                         session.commit()
#                                         await bot.send_message(message.chat.id, _("----------------------------------------------\n\n\n❤ Вітаю. Ви виграли ДЖЕКПОТ Х15!\n\n💶 Ви виграли - {} TRX").format(betting * 15))
#                                         await bot.send_message(message.chat.id, _("📯 Ви виграли ДЖЕКПОТ Х15! 📯"))
#                                         user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                                         bal_trx = user_db.bal_trx
#                                         markup_again_slot = await kb.markup_again_slot(message)
#                                         await bot.send_message(message.chat.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_slot, parse_mode='html')
#                                         await state.finish()
#                                     else:
#                                         await users.update.values(bal_trx=users.bal_trx - betting).where(users.user_id == message.from_user.id).gino.status()
#                                         session.commit()
#                                         markup_games = await kb.markup_games(message)
#                                         await bot.send_message(message.chat.id, _("----------------------------------------------\n\n\n💔 Ви програли :(... 🫥\n\n💸 Знято з балансу - {} TRX").format(betting), parse_mode='html', reply_markup=markup_games)
#                                         user_db = await users.query.where(users.user_id == message.from_user.id).gino.first()
#                                         bal_trx = user_db.bal_trx
#                                         markup_again_slot = await kb.markup_again_slot(message)
#                                         await bot.send_message(message.chat.id, _("💳 Ваш баланс - {} TRX\n\n\n----------------------------------------------").format(bal_trx), reply_markup=markup_again_slot, parse_mode='html')
#                                         await state.finish()
#                                 except:
#                                     await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
#                             else:
#                                 await bot.send_message(message.chat.id, _("❌ Недостатньо коштів ‼"), parse_mode='html')
#                                 await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                         else:
#                             await bot.send_message(message.chat.id, _("❌ Мінімальна сума ставки <b><i>1</i></b> TRX ‼"), parse_mode='html')
#                             await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                     else:
#                         await bot.send_message(message.chat.id, _("❌ Максимальна сума ставки <b><i>1000</i></b> TRX ‼"), parse_mode='html')
#                         await bot.send_message(message.chat.id, _("❌ Введіть іншу суму ставки (або можете вийти з гри /cancel):"), parse_mode='html')
#                 except:
#                     await bot.send_message(message.chat.id, _("❌ Число введено некоректно ❗"), parse_mode='html')
#                     markup_games = await kb.markup_games(message)
#                     await bot.send_message(message.chat.id, _("❌ Ви вийшли з гри ‼"), reply_markup=markup_games, parse_mode='html')
#                     await state.finish()
#
#         if call.data == 'lot_buy_game':
#             if not await db_commands.select_lottery_user(call.message.chat.id):
#                 user_db = await users.query.where(users.user_id == call.message.chat.id).gino.first()
#                 bal_trx = user_db.bal_trx
#                 if bal_trx >= 15:
#                     await db_commands.add_lot(call.message.chat.id)
#                     await call.answer(_("✅ Підтверджено"))
#                     await users.update.values(bal_trx=users.bal_trx - 15).where(users.user_id == call.message.chat.id).gino.status()
#                     await call.message.answer(_("Вітаю!"))
#                     await call.message.answer(_("✅ Ви взяли участь у лотереї. Щасти 🎫"))
#                     return session.commit()
#                 else:
#                     await call.message.answer(_("❌ Недостатньо коштів ‼"))
#             else:
#                 await call.message.answer("❗ Ви вже взяли участь у цьому розіграші лотереї")
#
#
#
#
#     else:
#         await call.message.answer(_('❗ Ваш аккаунт ЗАБАНЕНО !\n\n💭 Якщо виникли якісь питання, звертайтесь у тех.підтримку: @Christooo1'), reply_markup=types.ReplyKeyboardRemove())
