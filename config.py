from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher
from language_middleware import setup_middleware


API_TOKEN = ""


admins = [
    663493672,
    5143177713
    # 837846758
]


storage = MemoryStorage()


bot = Bot(token=API_TOKEN, parse_mode='html')
dp = Dispatcher(bot, storage=storage)


i18n = setup_middleware(dp)
_ = i18n.gettext




