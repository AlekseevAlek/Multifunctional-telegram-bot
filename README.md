Многофункциональный телеграм-бот

Данный бот сейчас умеет работать с фотографиями и делать ASCII-арт. Предлагается доработать бот, добавив свои функции.

Описание функционала:

Импорты и настройки

- telebot используется для взаимодействия с Telegram API.

- PIL (Python Imaging Library), известная как Pillow, предоставляет инструменты для работы с изображениями.

- TOKEN — это строковая переменная, куда вы должны поместить токен вашего бота, полученный от @BotFather в Telegram.

- bot = telebot.TeleBot(TOKEN) создает экземпляр бота для взаимодействия с Telegram.

Хранение состояний пользователей

- user_states используется для отслеживания действий или состояний пользователей. Например, какое изображение было отправлено.

Пикселизация

pixelate_image(image, pixel_size):

- Принимает изображение и размер пикселя. Уменьшает изображение до размера, где один пиксель представляет большую область, затем увеличивает обратно, создавая пиксельный эффект.

Преобразование в ASCII-арт

Подготовка изображения:

- resize_image(image, new_width=100): Изменяет размер изображения с сохранением пропорций.

- grayify(image): Преобразует цветное изображение в оттенки серого.

- image_to_ascii(image_stream, new_width=40): Основная функция для преобразования изображения в ASCII-арт. Изменяет размер, преобразует в градации серого и затем в строку ASCII-символов.

pixels_to_ascii(image):

- Конвертирует пиксели изображения в градациях серого в строку ASCII-символов, используя предопределенную строку ASCII_CHARS.

Взаимодействие с пользователем

Обработчики сообщений:

- @bot.message_handler(commands=['start', 'help']): Реагирует на команды /start и /help, отправляя приветственное сообщение.

- @bot.message_handler(content_types=['photo']): Реагирует на изображения, отправляемые пользователем, и предлагает варианты обработки.

Клавиатура для взаимодействия:

- get_options_keyboard(): Создает клавиатуру с кнопками для выбора пользователем, как обработать изображение: через пикселизацию или преобразование в ASCII-арт.

Обработка запросов

Обработка колбэков:

- @bot.callback_query_handler(func=lambda call: True): Определяет действия в ответ на выбор пользователя (например, пикселизация или ASCII-арт) и вызывает соответствующую функцию обработки.

Отправка результатов

Функции отправки:

- pixelate_and_send(message): Пикселизирует изображение и отправляет его обратно пользователю.

- ascii_and_send(message): Преобразует изображение в ASCII-арт и отправляет результат в виде текстового сообщения.

- invert_and_send(message): Применяет функцию инвертирования цветов к изображению и отправляет результат.

- mirror_and_send(message, axis): Применяет функцию отражения к изображению и отправляет результат.

-  heatmap_and_send(message): Применяет функцию конвертации в тепловую карту к изображению и отправляет результат.

-  resize_and_send(message): Применяет функцию адаптации размера к изображению и отправляет результат.

Функции для работы с пользовательским набором символов:

- get_custom_chars(message): Запрашивает у пользователя новый набор символов.

- process_custom_chars(message): Обрабатывает введенный пользователем набор символов.

Функция для создания  "негатива" изображения:

- invert_colors(image): Применяет функцию ImageOps.invert к изображению.

Функция для создания отражения изображения:

- mirror_image(image, axis='horizontal'): Создает отраженную копию изображения по горизонтали или вертикали.

Функция для создания тепловой карты:

-  convert_to_heatmap(image): Преобразует изображение в тепловую карту.

Функция изменения размера изображения для стикера:

-resize_for_sticker(image, max_size=512): Изменяет размер изображения для стикера, сохраняя пропорции и ограничивая максимальный размер.

![Image alt](https://github.com/AlekseevAlek/Multifunctional-telegram-bot/blob/master/тепловая%20карта.png)
