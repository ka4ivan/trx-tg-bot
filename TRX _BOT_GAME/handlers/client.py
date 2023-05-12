import smtplib
from email.mime.text import MIMEText

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.deep_linking import get_start_link

from db_api import db_quick_commands as db_commands
from db_api.schemas.achievement import Achievement_model as Achievement
from db_api.schemas.bonus import Bonus_model as Bonus
from db_api.schemas.users import Users_model as users
from db_api.schemas.stats import Stats_model as Stats
from config import dp, bot, _
import keyboards as kb
import handlers.states as states
import callback.games
import handlers.admin
import handlers.say_hi
import handlers.pay_operations
import pandas as pd
from openpyxl import Workbook

# Создаем новую таблицу Excel
wb = Workbook()
ws = wb.active

# Создаем заголовки для таблицы
ws.append(['ID відправника', 'Дата', 'Відправник', 'Сообщение'])
#######################################################################################################################################
from language_middleware import get_lang
from settings import session


async def anti_flood(*args, **kwargs):
    m = args[0]
    await m.answer(_("Не флуди :) Одне повідомлення в секунду"))

#######################################################################################################################################


#######################################################################################################################################

async def send_email(message: types.Message):
    sender = "bot.management.trx@gmail.com"
    password = "dztaoaixiiljstqi"
    recipient_mod = await users.query.where(users.user_id == message.from_user.id).gino.first()
    recipient = recipient_mod.mail
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    try:
        with open("gmail.html") as file:
            template = file.read()
    except IOError:
        return "The template file doesn't found!"

    try:
        server.login(sender, password)
        msg = MIMEText(template, "html")
        msg["From"] = sender
        msg["To"] = recipient
        msg["Subject"] = "Telegram TRX BOT registration confirmation"
        server.sendmail(sender, recipient, msg.as_string())
    except Exception as _ex:
        pass

#######################################################################################################################################



#######################################################################################################################################

@dp.message_handler(commands=["start"])
@dp.throttled(anti_flood, rate=1)
async def start_handler(message: types.Message):
    date_time = pd.Timestamp.now().strftime('%Y-%m-%d %H-%M-%S')
    date_time_save = pd.Timestamp.now().strftime('%Y-%m-%d')
    ws.append([message.from_user.id, date_time, f"{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username}", message.text])
    file_name = 'messages_' + date_time_save + '.xlsx'
    wb.save(f'logging/{file_name}')
    if message.chat.type == 'private':
        try:
            if (not await db_commands.select_user(message.from_user.id)):
                db_commands.register_user(message)
                start_command = message.text
                first_referrer_id = str(start_command[7:])
                if first_referrer_id != "":
                    if str(first_referrer_id) != str(message.from_user.id):
                        await users.update.values(first_referrer_id=int(first_referrer_id)).where(users.user_id == message.from_user.id).gino.status()
                        session.commit()
                        await db_commands.give_bonus_ref(message.from_user.id)
                        await message.answer(_('ℹ Ви зареєструвались по реферальному посиланню, тому отримуєте бонус.\n\n🤑Вам нараховано : 2 trx'))
                        try:
                            second_referrer_id_mod = await users.query.where(users.user_id == int(first_referrer_id)).gino.first()
                            second_referrer_id = second_referrer_id_mod.first_referrer_id
                            if second_referrer_id_mod != "":
                                await users.update.values(second_referrer_id=int(second_referrer_id)).where(users.user_id == message.from_user.id).gino.status()
                                session.commit()
                            else:
                                pass
                        except:
                            pass
                        try:
                            third_referrer_id_mod = await users.query.where(users.user_id == int(second_referrer_id)).gino.first()
                            third_referrer_id = third_referrer_id_mod.first_referrer_id
                            if third_referrer_id != "":
                                await users.update.values(third_referrer_id=int(third_referrer_id)).where(users.user_id == message.from_user.id).gino.status()
                                session.commit()
                            else:
                                pass
                        except:
                            pass
                        try:
                            await db_commands.give_bonus_thi_ref(third_referrer_id)
                            await bot.send_message(third_referrer_id, f'ℹ Користувач @{message.from_user.username} приєднався до бота за вашим реферальним посиланням по третій лінії.\n\n🤑Вам нараховано : 0.2 trx')
                        except:
                            pass
                        try:
                            await db_commands.give_bonus_sec_ref(second_referrer_id)
                            await bot.send_message(second_referrer_id, f'ℹ Користувач @{message.from_user.username} приєднався до бота за вашим реферальним посиланням по другій лінії.\n\n🤑Вам нараховано : 0.5 trx')
                        except:
                            pass
                        try:
                            await db_commands.give_bonus_ref(int(first_referrer_id))
                            await bot.send_message(first_referrer_id, f'ℹ Користувач @{message.from_user.username} приєднався до бота за вашим реферальним посиланням по першій лінії.\n\n🤑Вам нараховано : 1 trx')
                        except:
                            pass
                    else:
                        await message.answer(_('ℹ Ви намагались зареєструватись по власному реферальному посиланні, тому ви зареєстровані без нього'))

            if (not await db_commands.select_user_bonus(message.from_user.id)):
                db_commands.register_user_bonus(message)
            if (not await db_commands.select_user_achievement(message.from_user.id)):
                db_commands.register_user_achievement(message)


            captcha_mod = await users.query.where(users.user_id == message.from_user.id).gino.first()
            captcha = captcha_mod.captcha
            if captcha != 1:
                await states.captcha.select_language.set()
                captcha_num = 633912
                await message.answer(f"💻 Оберіть мову інтерфейсу | Выберите язык интерфейса | Choose the interface language 💻", reply_markup=kb.markup_select_language)

                @dp.message_handler(state=states.captcha.select_language)
                async def language(message: types.Message, state: FSMContext):
                    try:
                        if message.text == '🇺🇦 Українська':
                            await message.answer(f"🇺🇦 Вітаю\n\nВи обрали українську мову\n\nМову можна міняти в будь-який момент у розділі '🆘 Тех. Підтримка'", reply_markup=types.ReplyKeyboardRemove())
                            await message.answer(f"ℹ Підтвердіть що ви не бот\n\n📨 Введіть вашу пошту")
                            await users.update.values(user_language='uk').where(users.user_id == message.from_user.id).gino.status()
                            session.commit()
                            await states.captcha.next()
                        elif message.text == '🇷🇺 Русский':
                            await message.answer(f"🇷🇺 Поздравляю\n\nУ вас русский язык интерфейса\n\nЯзык можно менять в любой момент в разделе \n\n'🆘 Тех. Поддержка'", parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
                            await message.answer(f"ℹ Подтвердите что вы не бот\n\n📨 Введите вашу почту")
                            await users.update.values(user_language='ru').where(users.user_id == message.from_user.id).gino.status()
                            session.commit()
                            await states.captcha.next()
                        elif message.text == '🇬🇧 English':
                            await message.answer(f"🇬🇧 Congratulations\n\n You have chosen English\n\n You can change the language at any time in the section \n\n'🆘 Support'", parse_mode='html', reply_markup=types.ReplyKeyboardRemove())
                            await message.answer(f"ℹ Confirm that you are not a bot\n\n📨 Enter your email")
                            await users.update.values(user_language='en').where(users.user_id == message.from_user.id).gino.status()
                            session.commit()
                            await states.captcha.next()
                        else:
                            await message.answer(f"ℹ Невідома мова! Неизвестный язык! Unknown language!", reply_markup=kb.markup_select_language)
                            await message.answer(f"ℹ \n\nОберіть із списку знизу \n\nВыберите из списка снизу \n\nChoose from the list below")
                    except:
                        await message.answer(f"ℹ Невідома мова! Неизвестный язык! Unknown language!", reply_markup=kb.markup_select_language)
                        await message.answer(f"ℹ \n\nОберіть із списку знизу \n\nВыберите из списка снизу \n\nChoose from the list below")

                @dp.message_handler(state=states.captcha.type_mail)
                async def mail(message: types.Message, state: FSMContext):
                    await users.update.values(mail=message.text).where(users.user_id == message.from_user.id).gino.status()

                    await message.answer(_("✉ Check your email. Enter the code: 👇"))
                    await send_email(message=message)
                    await states.captcha.next()


                @dp.message_handler(state=states.captcha.type_captcha)
                async def type_captcha(message: types.Message, state: FSMContext):
                    try:
                        if message.text.isdigit():
                            if int(message.text) == captcha_num:
                                await message.answer(_('ℹ Ви пройшли перевірку'))
                                markup_phone = await kb.markup_phone(message)
                                await message.answer(_('Для роботи бота, потрібно поділитись Вашим номером телефону 👇'), reply_markup=markup_phone)
                                await states.captcha.next()
                            else:
                                await message.answer(_('ℹ Капча введена не правильно'))
                                await message.answer(_('ℹ Підтвердіть що ви не бот'))
                        else:
                            await message.answer(_('ℹ Капча введена не правильно'))
                            await message.answer(_('ℹ Підтвердіть що ви не бот'))
                    except:
                        await message.answer(_('🚫 Номер телефону введено некоректно'))
                    if str(message.text) == 'Ввести іншу пошту' or message.text == "Ввести другую почту" or message.text == "Enter another mail":
                        await states.captcha.select_language.set()
                        await message.answer(_('📨 Введіть вашу пошту'), reply_markup=types.ReplyKeyboardRemove())
                        await states.captcha.next()
                    else:
                        pass

                @dp.message_handler(content_types=types.ContentType.CONTACT, state=states.captcha.type_phone)
                async def phone(message: types.Message, state: FSMContext):
                    try:
                        phone = message.contact.phone_number
                        # if phone[0] == '+' and phone[1] == '3' and phone[2] == '8' or phone[0] == '3' and phone[1] == '8':
                        await users.update.values(phone=phone).where(users.user_id == message.from_user.id).gino.status()
                        await users.update.values(captcha=1).where(users.user_id == message.from_user.id).gino.status()
                        session.commit()
                        markup_start = await kb.markup_start(message)
                        await message.answer(_('ℹ Ви зареєструвались'), reply_markup=markup_start)
                        if message.from_user.first_name == None:
                            markup_start = await kb.markup_start(message)
                            await message.answer(_('Привіт, <b><u>{last_name}</u></b>. 🎉 Вітаємо у нашому боті 🎉').format(last_name=message.from_user.last_name), parse_mode='html', reply_markup=markup_start)
                        elif message.from_user.last_name == None:
                            markup_start = await kb.markup_start(message)
                            await message.answer(_('Привіт, <b><u>{first_name}</u></b>. 🎉 Вітаємо у нашому боті 🎉').format(first_name=message.from_user.first_name), parse_mode='html', reply_markup=markup_start)
                        elif message.from_user.first_name == None and message.from_user.last_name == None:
                            markup_start = await kb.markup_start(message)
                            await message.answer(_('Привіт. 🎉 Вітаємо у нашому боті 🎉'), parse_mode='html', reply_markup=markup_start)
                        else:
                            markup_start = await kb.markup_start(message)
                            await message.answer(_('👋 Привіт, <b><u>{full_name}</u></b>. 🎉 Вітаємо у нашому боті 🎉').format(full_name=message.from_user.first_name + ' ' + message.from_user.last_name), parse_mode='html', reply_markup=markup_start)
                        await message.answer(_('🤔 Оберіть ваш варіант 💭'))
                        await state.finish()
                        # else:
                        #     await state.finish()
                        #     await bot.send_message(message.from_user.id, f"🚫 Даний бот працює тільки для УКРАЇНЦІВ 🚫")
                    except:
                        await message.answer(_(f"🚫 Номер телефону введено не коректно"))
            else:
                ban_mod = await users.query.where(users.user_id == message.from_user.id).gino.first()
                ban = ban_mod.ban
                if ban == 0:
                    markup_start = await kb.markup_start(message)
                    await message.answer(_('🔝 <b>Головне Меню</b>'), parse_mode='html', reply_markup=markup_start)
                    await message.answer(_('🤔 Оберіть ваш варіант 💭'))
                else:
                    await message.answer(_('❗ Ваш аккаунт ЗАБАНЕНО !\n\n💭 Якщо виникли якісь питання, звертайтесь у тех.підтримку: @Christooo1'), reply_markup=types.ReplyKeyboardRemove())

            @dp.message_handler(state=states.captcha.start)
            async def start_(message: types.Message, state: FSMContext):
                markup_start = await kb.markup_start(message)
                await message.answer(_('🔝 <b>Головне Меню</b>'), parse_mode='html', reply_markup=markup_start)
                await message.answer(_('🤔 Оберіть ваш варіант 💭'))
                await state.finish()
        except:
            await message.answer(_('❗ Бот розроблений для кожного особисто, не можна його добавляти в групи. Поспілкуйтесь з ним самі: @trx_games_bot\nЯкщо у вас виникли інші проблеми, звертайтесь до нашого менеджера: @Christooo1'))
    else:
        await message.answer(_('❗ Бот розроблений для кожного особисто, не можна його добавляти в групи. Поспілкуйтесь з ним самі: @trx_games_bot\nЯкщо у вас виникли інші проблеми, звертайтесь до нашого менеджера: @Christooo1'))

#######################################################################################################################################



#######################################################################################################################################
@dp.message_handler(commands=["help"])
@dp.throttled(anti_flood, rate=1)
async def help_handler(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(_("📺 Звернутись із проблемою"), url="https://t.me/Christooo1"))
    await message.answer(_("ℹ Якщо у вас виникли проблеми в боті, спробуйте написати команду: /start \n\n👨‍🔧 Якщо проблема лишилась, напишіть нашому менеджеру, він все владнає:\nhttps://t.me/Christooo1"), reply_markup=markup)
#######################################################################################################################################




#######################################################################################################################################
@dp.message_handler(commands='list_wins')
@dp.throttled(anti_flood, rate=1)
async def list_wins_combo(message: types.Message):
    await bot.send_message(message.from_user.id, _('📋 Список виграшних комбінацій у грі "Слоти"'
                           '\n\n<b><i>x0️⃣.3️⃣ від ставки</i></b>\n\n'
                           '<b>'
                           '🍇   BAR   BAR   |   🍋   BAR   BAR\n7️⃣   BAR   BAR   |   BAR   🍇   BAR\n🍇   🍇   BAR   |   '
                           'BAR   🍋   BAR\nBAR   7️⃣   BAR   |   BAR   BAR   🍇\nBAR   BAR   🍋   |   BAR   BAR   7️⃣\n'
                           '🍇   BAR   🍇   |   BAR   🍇   🍇\n🍋   🍇   🍇   |   7️⃣   🍇   🍇\n🍇   🍋   🍇   |   🍇   7️⃣   🍇\n'
                           '🍇   🍇   🍋   |   🍇   🍇   7️⃣\n🍋   🍋   BAR   |   🍋   🍋   🍇\n🍋   BAR   🍋   |   🍋   🍇   🍋\n'
                           'BAR   🍋   🍋   |   🍇   🍋   🍋\n7️⃣   🍋   🍋   |   🍋   7️⃣   🍋\n🍋   🍋   7️⃣   |   7️⃣   BAR   7️⃣\n'
                           '7️⃣   🍇   7️⃣   |   7️⃣   🍋   🍋\nBAR   7️⃣   7️⃣   |   🍇   7️⃣   7️⃣\n🍋   7️⃣   7️⃣'
                           '</b>'
                           '\n\n<b><i>x3️⃣ від ставки</i></b>\n\n'
                           '<b>'
                           'BAR   BAR   BAR\n🍇   🍇   🍇\n🍋   🍋   🍋'
                           '</b>'
                           '\n\n<b><i>x5️⃣ від ставки</i></b>\n\n'
                           '<b>'
                           '7️⃣   7️⃣   BAR\n7️⃣   7️⃣   🍇\n7️⃣   7️⃣   🍋'
                           '</b>'
                           '\n\n<b><i>x1️⃣5️⃣ від ставки</i></b> - ДЖЕКПОТ\n\n'
                           '7️⃣   7️⃣   7️⃣'), parse_mode='html')
#######################################################################################################################################



#######################################################################################################################################

@dp.message_handler(content_types=['text'])
@dp.throttled(anti_flood, rate=1)
async def text_message(message: types.Message):

    date_time = pd.Timestamp.now().strftime('%Y-%m-%d %H-%M-%S')
    date_time_save = pd.Timestamp.now().strftime('%Y-%m-%d')
    ws.append([message.from_user.id, date_time, f"{message.from_user.first_name} {message.from_user.last_name} @{message.from_user.username}", message.text])
    file_name = 'messages_' + date_time_save + '.xlsx'
    wb.save(f'logging/{file_name}')

    user = await users.query.where(users.user_id == message.from_user.id).gino.first()
    ban = user.ban
    if ban == 0:
        if (message.text == "🎯 Ігри 🎮" or message.text == "🎯 Игры 🎮" or message.text == "🎯 Games 🎮"):
            markup_games = await kb.markup_games(message)
            await message.answer(_('ℹ Список ігор 👀'), reply_markup=markup_games)
        elif (message.text == "🛩 Краш" or message.text == "🛩 Crash"):
            markup_crush_buy = await kb.markup_crush_buy(message)
            await bot.send_message(message.chat.id, _("🕹 Гра '<i><b>🛩 Краш</b></i>'\n\n <i>📢 Правила</i>:\nЗробіть ставку. Після ставки, вилетить літак який в любу хвилину може розбитись. Ваше завдання вчасно натиснути на кнопку '⬇ Забрати', до того як він розіб'ється і ви втратите всі гроші поставлені на ставку\n\n💎 Мінімальна сума ставки <b><i>1</i></b> TRX\n\nЩоб вийти з гри  /cancel \n\n🏆 Приз за перемогу:\n\nМножитель виграшу буде рости поки літак літає(він росте зі швидкістю <u><i><b>+0.2х</b></i></u> в секунду)"), reply_markup=markup_crush_buy, parse_mode='html')
        elif (message.text == "🔢 Вгадай число" or message.text == "🔢 Угадай число" or message.text == "🔢 Guess the number"):
            await bot.send_message(message.chat.id, _('🕹 Гра "<i><b>Вгадай число</b></i>"\n\n <i>📢 Правила</i>:\nДля початку гри обреіть кількість чисел. У будь-якій кількості, правильне число буде всього одне(!), проте будуть рости і нагороди. Зробіть ставку. Після ставки, випадковим чином, буде обране число. Ваше завдання відгадати загадане число\nДля того щоб грати в гру, необхідно щоб на аккаунті було більше <i>1 TRX</i>!!!\n\n💎 Мінімальна сума ставки <b><i>1</i></b> TRX\n\nЩоб вийти з гри  /cancel \n\n🏆 Приз за перемогу:\n\n5️⃣ Чисел - <u><i><b>x4.95</b></i></u> від ставки\n\n1️⃣0️⃣ Чисел - <u><i><b>x9.9</b></i></u> від ставки\n\n1️⃣0️⃣0️⃣ Чисел - <u><i><b>x95</b></i></u> від ставки'), reply_markup=kb.markup_guess_select, parse_mode='html')
        elif (message.text == "🌗 50/50"):
            await bot.send_message(message.chat.id, _('🕹 Гра "<i><b>50/50</b></i>"\n\n <i>📢 Правила</i>:\nЗробіть ставку. Після ставки, випадковим чином, буде обране число. Ваше завдання відгадати загадане число, з імовірністю перемоги 50%\n\nДля того щоб грати в гру, необхідно щоб на аккаунті було більше <i>1 TRX</i>!!!\n\n💎 Мінімальна сума ставки <b><i>1</i></b> TRX\n\nЩоб вийти з гри  /cancel \n\n🏆 Приз за перемогу:\n\n2️⃣ числа\n<u><i><b>x1.95</b></i></u> від ставки\n\n4️⃣ числа\n<u><i><b>x1.95</b></i></u> від ставки\n<u><i><b>x3.9</b></i></u> від ставки. Якщо два загадані числа співпадають'), reply_markup=kb.markup_fifty_select, parse_mode='html')
        elif (message.text == "🎲 Кубик" or message.text == "🎲 Dice"):
            markup_dice_select = await kb.markup_dice_select(message)
            await bot.send_message(message.chat.id, _('🕹 Гра "<i><b>Кубик</b></i>"\n\n <i>📢 Правила</i>:\nЗробіть ставку та оберіть варіант випадання кубика. \n\n🎲 Більше/менше 7️⃣: Потрібно вгадати яким чином випадуть два кубика\n\n🎲 Класичний кубик: Потрібно вгадати яке число випаде на кубику\n\n💎 Мінімальна сума ставки <b><i>1</i></b> TRX\n\nЩоб вийти з гри  /cancel \n\n🏆 Приз за перемогу:\n\n🎲 Більше/менше 7️⃣\n<u><i><b>x2</b></i></u> від ставки - Більше <i><b>7</b></i>\n<u><i><b>x5.8</b></i></u> від ставки - <i><b>7</b></i>\n<u><i><b>x2</b></i></u> від ставки - Менше <i><b>7</b></i>\n\n🎲 Класичний кубик\n <u><i><b>x5.8</b></i></u> від ставки'), reply_markup=markup_dice_select, parse_mode='html')
        elif (message.text == "💣 Сапер" or message.text == "💣 Сапёр" or message.text == "💣 Minesweeper"):
            await bot.send_message(message.chat.id, _('🕹 Гра "<i><b>Сапер</b></i>"\n\n <i>📢 Правила</i>:\nЗробіть ставку та оберіть варіант гри із певною кількістю бомб на полі. Ігрова зона складається із 9 полів(3*3), в яких знаходиться певна кількість бомб, в залежності від виду гри\n\n💎 Мінімальна сума ставки <b><i>1</i></b> TRX\n\nЩоб вийти з гри  /cancel \n\n🏆 Приз за перемогу:\n\n3️⃣ бомби - <u><i><b>x1.7</b></i></u> від ставки\n\n5️⃣ бомб - <u><i><b>x2</b></i></u> від ставки\n\n7️⃣ бомб - <u><i><b>x4.5</b></i></u> від ставки'), reply_markup=kb.markup_miner_select, parse_mode='html')
        elif (message.text == "🎰 Слоти" or message.text == "🎰 Слоты" or message.text == "🎰 Slots"):
            markup_spin_select = await kb.markup_spin_select(message)
            await bot.send_message(message.chat.id, _('🕹 Гра "<i><b>Слоти</b></i>"\n\n<i>📢 Правила</i>:\nЗробіть ставку. Після чого буде крутитись барабан із слотами. Ваш виграш буде залежати від того, яка комбінація випала на барабані.\n\n💎 Мінімальна сума ставки <b><i>1</i></b> TRX\n\nЩоб вийти з гри  /cancel \n\n🏆 Приз за перемогу:\n\nВинагорода залежить від комбінації яка випала на барабані.\n\n📋 Список комбінацій можна подивитись тут: <b><i>/list_wins</i></b>'), reply_markup=markup_spin_select, parse_mode='html')
        elif (message.text == "🎫 Взяти участь в лотереї" or message.text == "🎫 Принять участие в лотерее" or message.text == "🎫 Take part in the lottery"):
            markup_lot_buy = await kb.markup_lot_buy(message)
            await bot.send_message(message.chat.id, '🎫 Подія "<i><b>Лотерея</b></i>"\n\n <i>📢 Правила</i>:\n\nЛотерея відбувається один раз на день. Всьго є 100 білетів, по ціні за один - 15 TRX. При купівлі всіх ста білетів(або якщо вийшов час), відбувається розіграш, де переможець забере 85% від всієї суми\n\n🏆 Приз за перемогу:\n\n1 білет(15 TRX)\n<u><i><b>85%</b></i></u> від всієї суми', reply_markup=markup_lot_buy, parse_mode='html')
        elif (message.text == "📦 Кейси" or message.text == "📦 Кейсы" or message.text == "📦 Cases"):
            await bot.send_message(message.chat.id, _('🕹 Гра "<i><b>Кейси</b></i>"\n\n <i>📢 Правила</i>:\nОберіть кейс та відкрийте його. Всередині кейса знаходиться грошовий приз, який може бути як більший, так і менший від вартості самого кейса\n\nЩоб вийти з гри  /cancel \n\n🎛 Види кейсів:\n\n📦 - 💳 Вартість: 10 TRX\n        🏆 Винагорода: <u><i><b>5-15 TRX</b></i></u>\n\n🎒 - 💳 Вартість: 100 TRX\n        🏆 Винагорода: <u><i><b>50-150 TRX</b></i></u>\n\n💼 - 💳 Вартість: 500 TRX\n        🏆 Винагорода: <u><i><b>0-1000 TRX</b></i></u>'), reply_markup=kb.markup_select_cases, parse_mode='html')
        elif (message.text == "🆘 Тех. Підтримка") or (message.text == "🆘 Тех. Поддержка") or (message.text == "🆘 Tech. Support"):
            markup = types.InlineKeyboardMarkup(row_width=1)
            change_language = types.InlineKeyboardButton('🔄 \n\nПоміняти мову | Сменить язык | Change the language', callback_data="change_language")
            up_button = types.InlineKeyboardButton(_("📺 Зв'язатись із тех. підтримкою"), url="https://t.me/Christooo1")
            markup.add(change_language, up_button)
            photo = open('img/what-is-bot-management.png', 'rb')
            await bot.send_photo(message.from_user.id, photo, caption=_('При будь-яких питаннях звертайтесь до нашого менеджера: @Christooo1'), reply_markup=markup, parse_mode='html')
        elif (message.text == "🔙 Назад") or (message.text == "🔙 Back"):
            markup_start = await kb.markup_start(message)
            await message.answer(_('🔝 <b>Головне Меню</b>'), parse_mode='html', reply_markup=markup_start)
            await message.answer(_('🤔 Оберіть ваш варіант 💭'))
        elif (message.text == "👤 Партнерська програма" or message.text == "👤 Партнерская программа" or message.text == "👤 Affiliate program"):
            link = await get_start_link(message.from_user.id)
            photo = open('img/ref.jpg', 'rb')
            count_first = await db_commands.count_first_ref(message.from_user.id)
            if count_first == None:
                count_first = 0
            count_second = await db_commands.count_second_ref(message.from_user.id)
            if count_second == None:
                count_second = 0
            count_third = await db_commands.count_third_ref(message.from_user.id)
            if count_third == None:
                count_third = 0
            count_all = int(count_first) + int(count_second) + int(count_third)
            if count_all == None:
                count_all = 0
            await bot.send_photo(message.from_user.id, photo, caption='👥 Партнерська програма TRON\n\nℹ Заробляйте TRX на запрошення активних рефералів.\n\n🤑 Бонус по лініях:\n1 лінія – 1 TRX\n2 лінія – 0.6 TRX\n3 лінія – 0.2 TRX\n\n📌 Щоб отримувати бонус діліться своїм партнерським посиланням зі своїми друзями.\n\n▶ Партнерське посилання: {}\n\n👥 Ваші партнери:\n➖ Перша лінія: {}\n➖ Друга лінія: {}\n➖ Третя лінія: {}\n\n 🚀 Всього рефералів: {}' .format(link, count_first, count_second, count_third, count_all), parse_mode='html')
        elif (message.text == "🎁 BONUS"):
            photo = open('img/bonus_img.jpg', 'rb')
            markup_bonus = await kb.markup_bonus(message)
            await bot.send_photo(message.from_user.id, photo, caption=_("🤔 Обери вид бонусу 👀"), reply_markup=markup_bonus, parse_mode='html')
        elif (message.text == "📊 Статистика TRON" or message.text == "📊 TRON statistics"):
            stats_db = await Stats.query.gino.first()
            all_acc = stats_db.all_acc
            day_acc = stats_db.day_acc
            active_acc = stats_db.active_acc
            pay_trx = stats_db.pay_trx
            photo = open('img/stat_img.jpg', 'rb')
            await bot.send_photo(message.from_user.id, photo, caption=_("📊 Статистика проєкту(оновлюється кожні 24 год)\n\n👥 Аудиторія: <code>{}</code>\n👥 Користувачі за останні 24 год: <code>{}</code>\n👤 Активні користувачі: <code>{}</code>\nВиплачено TRX - <code>{}</code>").format(all_acc, day_acc, active_acc, pay_trx), parse_mode='html')
        elif (message.text == "🗣 Поділитись історією/музикою" or message.text == "🗣 Поделиться историей/музыкой" or message.text == "🗣 Share a story/music"):#👋 Передати всім привіт
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(_("👋 Надіслати всім повідомлення"), callback_data='say_hi_inline'))
            await bot.send_message(message.from_user.id, text=_("📋 Інформація кабінету:\n\nℹ  За допомогою кнопки <i>«👋 Надіслати всім повідомлення»</i>, ви зможете написати своє повідомлення, додати фотографію або ж додати музичний файл який, після перевірки модератора, побачать і почують всі користувачі бота\n\n<b>Вартість написання повідомлення</b> \n\n💳 1 Повідомлення(Текст): <u><b><i>50 TRX</i></b></u>\n💳 1 Повідомлення(Фото): <u><b><i>60 TRX</i></b></u>\n💳 1 Повідомлення(Музика): <u><b><i>60 TRX</i></b></u>\n💳 1 Повідомлення(Фото + Музика): <u><b><i>80 TRX</i></b></u>\n\n👨‍💼 Менеджер по повідомленням - @Christooo1"), reply_markup=markup, parse_mode='html')
        elif (message.text == "🤑 Отримати до 1.000 TRX" or message.text == "🤑 Получить до 1.000 TRX" or message.text == "🤑 Get up to 1.000 TRX"):
            markup = types.InlineKeyboardMarkup(row_width=1)
            up_button = types.InlineKeyboardButton(_("📺 Гугл форма"), url="https://docs.google.com/forms/d/e/1FAIpQLSf30jE_aWUzq81I9gAnZMnPRhW-63AnEJ8soUMTIPjUo7XHVQ/viewform?usp=sf_link")
            markup.add(up_button)
            photo = open('img/thousend_trx.jpg', 'rb')
            await bot.send_photo(message.from_user.id, photo, caption=_("🎥 Зніми відео на <i><b>YouTube/Tiktok</b></i> огляд на нашого бота і відправ посилання в <a href='https://docs.google.com/forms/d/e/1FAIpQLSf30jE_aWUzq81I9gAnZMnPRhW-63AnEJ8soUMTIPjUo7XHVQ/viewform?usp=sf_link'><i><b>Гугл форму</b></i></a> і отримай до 1 000 TRX! \n\n   ➡ Відео на Youtube має бути від 60 секунд/TikTok мають бути вказані хеш-теги ' заробіток,халява,роздача,без вкладень,криптовалюта,інвестиції' \n\n   ➡ В описі під відео має бути ваше реферальне посилання і ваш id"), reply_markup=markup, parse_mode='html')
        elif (message.text == "📱 Рекламний кабінет" or message.text == "📱 Рекламный кабинет" or message.text == "📱 Advertising office"):
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(_("📺 Зв'язатись по питанням реклами"), url="https://t.me/Christooo1"))
            await bot.send_message(message.from_user.id, text=_("📋 Інформація рекламного кабінету:\n\nℹ  За допомогою кнопки <i>«📺 Зв'язатись по питанням реклами»</i>, ви зможете додати свій канал в нашого бота, або ж запустити банерний пост\n\n<b>Вартість додавання вашого каналу в бота</b> \n\n💳1 тиждень: 50 USDT TRC20 \n💳1 місяць: 160 USDT TRC20\n\n<b>Вартість банерного поста:</b>\n\n💳1 пост: 10 USDT TRC20\n💳3 пост: 25 USDT TRC20\n\n👨‍💼 Менеджер по рекламі - @Christooo1"), reply_markup=markup, parse_mode='html')
        elif (message.text == "❤ Підтримати бота" or message.text == "❤ Поддержать бота" or message.text == "❤ Support the bot"):
            await bot.send_message(message.from_user.id, text=_('Підтримка працездатності бота\n❤️‍🔥Ми працюємо тільки завдяки вам та задля вас\n\nРеквізити (жмякни по ньому):\n\n💱BTC: <code>bc1qup63zllhsn9vmzwn2atm2jp6wwldhkn0h7yxau</code>\n\n💵USDT Tether20: <code>TQDtxNHBv7aHvQgNKGJryQ4PB8j2dToTKS</code>\n\n🌼 Також всі бажаючі, можуть нас підтримати на нашому <code>Patreon</code> та <code>Boosty</code>. Детальніша інформація по кнопці: \n"🅿 Наш Patreon and 🅱 Boosty"\n\nТі хто нас підтримали:\n\nМожуть замовити банер (текст і фото по бажанню) який побачать всі користувачі'), parse_mode='html')
        elif (message.text == "🅿 Наш Patreon and 🅱 Boosty" or message.text == "🅿 Our Patreon and 🅱 Boosty"):
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton("🅿 Patreon", url="patreon.com/TelegramTRXBot"), types.InlineKeyboardButton("🅱 Boosty", url="https://boosty.to/telegramtrxbot"))
            photo = open('img/patreon.png', 'rb')
            await bot.send_photo(message.from_user.id, photo, caption=_("💡 Інформація про наш Patreon i Boosty\n\nНа Patreon i Boosty є сторінка нашого телеграм бота. Ви можете стати нашим патроном і отримати доступ до унікального контенту. Чим вище ваш рівень в Patreon тим більші у вас будуть там привілегій\n\n🔱 Кожен наш патрон отримує:\n\n<i>➖ Ваш аккаунт отримує спеціальну відзнаку\n➖ Доступ до закритої тг групи\n➖ Унікальні промокоди\n➖ Різні івенти з іграми у ботi\n➖ Періодичні знижки\n➖ Вікторини \n➖ Та багато чого іншого...</i>\n\n🔗 Посилання на наш <b>Patreon</b>:  patreon.com/TelegramTRXBot\n🔗 Посилання на наш <b>Boosty</b>:  boosty.to/telegramtrxbot"), parse_mode='html', reply_markup=markup)
        elif (message.text == "📳 Мій кабінет" or message.text == "📳 Мой кабинет" or message.text == "📳 My account"):
            bal_trx = user.bal_trx
            await users.update.values(bal_trx=round(bal_trx, 2)).where(users.user_id == message.from_user.id).gino.status()
            user = await users.query.where(users.user_id == message.from_user.id).gino.first()
            bal_usd = user.bal_usd
            bal_trx = user.bal_trx
            user_id = user.user_id
            join_date = user.join_date
            user_level = user.user_level
            patron = user.patron
            first_ref = await db_commands.count_first_ref(user_id)
            second_ref = await db_commands.count_second_ref(user_id)
            third_ref = await db_commands.count_third_ref(user_id)
            all_ref = await db_commands.count_first_ref(user_id) + await db_commands.count_second_ref(user_id) + await db_commands.count_third_ref(user_id)
            photo = open('img/my_cab.jpg', 'rb')
            if patron == 0:
                patron = '❌😞'
            else:
                patron = '〰   👑   〰'
            markup_cab = await kb.markup_cab(message)
            await bot.send_photo(message.from_user.id, photo, caption=_("📱 Мій кабінет\n🔑 Мій ID: {}\n\n🏅 Рівень аккаунту:<u>____<b><i>{}</i></b>____</u>\n\n🅿 Наш патрон:   {}\n\n💳 Баланс: <b><u>{}</u></b> USDT TRC20 | <b><u>{}</u></b> TRX\n👤 Перший вхід: {}\n\n🚀 Всього рефералів: {}\n➖ 1 лінія: {}\n➖ 2 лінія: {}\n➖ 3 лінія: {}").format(user_id, user_level, patron, bal_usd, bal_trx, str(join_date)[:16], all_ref, first_ref, second_ref, third_ref), reply_markup=markup_cab, parse_mode='html')

        elif (message.text == "🏆 Досягнення" or message.text == "🏆 Достижения" or message.text == "🏆 Achievements"):
            achievement = await Achievement.query.where(Achievement.user_id == message.from_user.id).gino.first()

            daily_bonus = achievement.daily_bonus
            pay_trx = achievement.pay_trx
            c_daily_bonus = achievement.c_daily_bonus
            c_pay_trx = achievement.c_pay_trx
            pay_trx_th = achievement.pay_trx_th
            c_pay_trx_th = achievement.c_pay_trx_th
            c_f_ref = achievement.c_f_ref
            c_s_ref = achievement.c_s_ref
            c_a_ref = achievement.c_a_ref
            game_dice = achievement.game_dice
            c_game_dice = achievement.c_game_dice
            win_lot_ = achievement.win_lot
            c_win_lot = achievement.c_win_lot
            game_mine = achievement.game_mine
            c_game_mine = achievement.c_game_mine


            cub = _("➖ Зіграти в 'кубик' 50 раз")
            if game_dice >= 50:
                cub = _("✅ Зіграти в 'кубик' 50 раз")

            mine = _("➖ Зіграти в 'сапер' 40 раз")
            if game_mine >= 40:
                mine = _("✅ Зіграти в 'сапер' 40 раз")

            f = _("➖ Кількість рефералів першого рівня")
            if await db_commands.count_first_ref(message.from_user.id) >= 35:
                f = _("✅ Кількість рефералів першого рівня")

            s = _("➖ Кількість рефералів другого рівня")
            if await db_commands.count_second_ref(message.from_user.id) >= 15:
                s = _("✅ Кількість рефералів другого рівня")

            a = _("➖ Загальна кількість рефералів")
            if (await db_commands.count_first_ref(message.from_user.id) + await db_commands.count_second_ref(message.from_user.id) + await db_commands.count_third_ref(message.from_user.id)) >= 50:
                a = _("✅ Загальна кількість рефералів")

            day = _("➖ Отримати щоденний бонус 30 раз")
            if daily_bonus >= 30:
                day = _("✅ Отримати щоденний бонус 30 раз")

            pay = _("➖ Поповнити 250 TRX")
            if pay_trx >= 250:
                pay = _("✅ Поповнити 250 TRX")

            pay_th = _("➖ Поповнити 1000 TRX")
            if pay_trx_th >= 1000:
                pay_th = _("✅ Поповнити 1000 TRX")

            win_lot = _("➖ Виграти лотерею 2 рази")
            if win_lot_ >= 2:
                win_lot = _("✅ Виграти лотерею 2 рази")

            await bot.send_message(message.from_user.id, text=_("🏅 Виконуйте завдання та отримуйте винагороду за ваші досягнення 🎫\n\n📋 Список досягнень:\n\n\n{}: <b><i>{}/50</i></b>  \n🏆 Винагорода: 3.5 TRX\n\n{}: <b><i>{}/40</i></b>  \n🏆 Винагорода: 4 TRX\n\n{}: <b><i>{}/30</i></b>\n🏆 Винагорода: 2.5 TRX\n\n{}: <b><i>{}/35</i></b>\n🏆 Винагорода: 6.5 TRX\n\n{}: <b><i>{}/15</i></b>\n🏆 Винагорода: 3.5 TRX\n\n{}: <b><i>{}/50</i></b>\n🏆 Винагорода: 10 TRX\n\n{}: <b><i>{}/2</i></b>\n🏆 Винагорода: 17.5 TRX\n\n{}: <b><i>{}/250</i></b>\n🏆 Винагорода: 5 TRX\n\n{}: <b><i>{}/1000</i></b>\n🏆 Винагорода: 25 TRX").format(cub, game_dice, mine, game_mine, day, daily_bonus, f, await db_commands.count_first_ref(message.from_user.id), s, await db_commands.count_second_ref(message.from_user.id), a, await db_commands.count_first_ref(message.from_user.id) + await db_commands.count_second_ref(message.from_user.id) + await db_commands.count_third_ref(message.from_user.id), win_lot, win_lot_, pay, pay_trx, pay_th, pay_trx_th), parse_mode='html')

            if daily_bonus >= 30:
                if c_daily_bonus != 1:
                    await db_commands.give_achivement_day(message.from_user.id)
                    await bot.send_message(message.chat.id, _('📯 <b>Вітаю! Ви отримали досягнення <i><u>"Отримати щоденний бонус 30 раз"</u></i>. Вам нараховано 2.5 TRX</b> ⚜'), parse_mode='html')
            if pay_trx >= 250:
                if c_pay_trx != 1:
                    await db_commands.give_achivement_pay(message.from_user.id)
                    await bot.send_message(message.chat.id, _('📯 <b>Вітаю! Ви отримали досягнення <i><u>"Поповнити 250 TRX"</u></i>. Вам нараховано 5 TRX</b> ⚜'), parse_mode='html')
            if pay_trx_th >= 1000:
                if c_pay_trx_th != 1:
                    await db_commands.give_achivement_pay_th(message.from_user.id)
                    await bot.send_message(message.chat.id, _('📯 <b>Вітаю! Ви отримали досягнення <i><u>"Поповнити 1000 TRX"</u></i>. Вам нараховано 25 TRX</b> ⚜'), parse_mode='html')
            if await db_commands.count_first_ref(message.from_user.id) >= 35:
                if c_f_ref != 1:
                    await db_commands.give_achivement_f(message.from_user.id)
                    await bot.send_message(message.chat.id, _('📯 <b>Вітаю! Ви отримали досягнення <i><u>"Кількість рефералів першого рівня"</u></i>. Вам нараховано 6.5 TRX</b> ⚜'), parse_mode='html')
            if await db_commands.count_second_ref(message.from_user.id) >= 15:
                if c_s_ref != 1:
                    await db_commands.give_achivement_s(message.from_user.id)
                    await bot.send_message(message.chat.id, _('📯 <b>Вітаю! Ви отримали досягнення <i><u>"Кількість рефералів другого рівня"</u></i>. Вам нараховано 3.5 TRX</b> ⚜'), parse_mode='html')
            if (await db_commands.count_first_ref(message.from_user.id) + await db_commands.count_second_ref(message.from_user.id) + await db_commands.count_third_ref(message.from_user.id)) >= 50:
                if c_a_ref != 1:
                    await db_commands.give_achivement_a(message.from_user.id)
                    await bot.send_message(message.chat.id, _('📯 <b>Вітаю! Ви отримали досягнення <i><u>"Загальна кількість рефералів"</u></i>. Вам нараховано 10 TRX</b> ⚜'), parse_mode='html')
            if game_dice >= 50:
                if c_game_dice != 1:
                    await db_commands.give_achivement_cub(message.from_user.id)
                    await bot.send_message(message.chat.id, _('📯 <b>Вітаю! Ви отримали досягнення <i><u>"Зіграти в кубик 50 раз"</u></i>. Вам нараховано 3.5 TRX</b> ⚜'), parse_mode='html')
            if win_lot_ >= 2:
                if c_win_lot != 1:
                    await db_commands.give_achivement_win_lot(message.from_user.id)
                    await bot.send_message(message.chat.id, _('📯 <b>Вітаю! Ви отримали досягнення <i><u>"Виграти лотерею 2 рази"</u></i>. Вам нараховано 17.5 TRX</b> ⚜'), parse_mode='html')
            if game_mine >= 40:
                if c_game_mine != 1:
                    await db_commands.give_achivement_miner(message.from_user.id)
                    await bot.send_message(message.chat.id, _('📯 <b>Вітаю! Ви отримали досягнення <i><u>"Зіграти в cапер 40 раз"</u></i>. Вам нараховано 4 TRX</b> ⚜'), parse_mode='html')



        else:
            await bot.send_message(message.from_user.id, _("❌ Невідома команда!\n\nВи відправили повідомлення напряму в чат бота, або структура меню була змінена Адміном.\n\nℹ  Не відправляйте прямих повідомлень боту або обновіть Меню, натисніть /start"), parse_mode='html')



    else:
        await message.answer(_('❗ Ваш аккаунт ЗАБАНЕНО !\n\n💭 Якщо виникли якісь питання, звертайтесь у тех.підтримку: @Christooo1'), reply_markup=types.ReplyKeyboardRemove())

#######################################################################################################################################



#######################################################################################################################################

@dp.message_handler(state='*', commands='cancel')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    markup_games = await kb.markup_games(message)
    await message.answer(_("❌ Ви вийшли ‼"), reply_markup=markup_games)


@dp.message_handler(state='*', commands='cancel_promo_code')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    markup_start = await kb.markup_start(message)
    await message.answer(_("❌ Ви вийшли з введення промокоду ‼"), reply_markup=markup_start)

#######################################################################################################################################






