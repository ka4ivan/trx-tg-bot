Название - telegram_trx_bot, можете сменить на любое другое

Запускаем первый раз
1. Вытаскиваем тексты из файлов (он сам находит)
pybabel extract . -o locales/telegram_trx_bot.pot
2. Создаем папку для перевода на английский
pybabel init -i locales/telegram_trx_bot.pot -d locales -D telegram_trx_bot -l en
3. То же, на русский
pybabel init -i locales/telegram_trx_bot.pot -d locales -D telegram_trx_bot -l ru
4. То же, на украинский
pybabel init -i locales/telegram_trx_bot.pot -d locales -D telegram_trx_bot -l uk
5. Переводим, а потом собираем переводы
pybabel compile -d locales -D telegram_trx_bot


Обновляем переводы
1. Вытаскиваем тексты из файлов, Добавляем текст в переведенные версии
pybabel extract . -o locales/telegram_trx_bot.pot
pybabel update -d locales -D telegram_trx_bot -i locales/telegram_trx_bot.pot
3. Вручную делаем переводы, а потом Собираем
pybabel compile -d locales -D telegram_trx_bot




