import telebot
from PIL import Image
import io
from telebot import types
import os


TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)

user_states = {}  # тут будем хранить информацию о действиях пользователя

# набор символов из которых составляем изображение
ASCII_CHARS = '@%#*+=-:. '


def resize_image(image, new_width=100):
    '''Изменяет размер изображения, сохраняя пропорции'''
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))


def grayify(image):
    '''Конвертирует изображение в оттенки серого'''
    return image.convert("L")


def image_to_ascii(image_stream, new_width=40):
    '''Преобразует изображение в ASCII art'''
    # Переводим в оттенки серого
    image = Image.open(image_stream).convert('L')

    # меняем размер сохраняя отношение сторон
    width, height = image.size
    aspect_ratio = height / float(width)
    new_height = int(
        aspect_ratio * new_width * 0.55)  # 0,55 так как буквы выше чем шире
    img_resized = image.resize((new_width, new_height))

    img_str = pixels_to_ascii(img_resized)
    img_width = img_resized.width

    max_characters = 4000 - (new_width + 1)
    max_rows = max_characters // (new_width + 1)

    ascii_art = ""
    for i in range(0, min(max_rows * img_width, len(img_str)), img_width):
        ascii_art += img_str[i:i + img_width] + "\n"

    return ascii_art


def pixels_to_ascii(image):
    '''Преобразует пиксели изображения в символы ASCII'''
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        characters += ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
    return characters


# Огрубляем изображение
def pixelate_image(image, pixel_size):
    '''Пикселизация изображения'''
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )
    return image


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    '''Обрабатывает команды /start и /help, отправляя приветственное сообщение'''
    bot.reply_to(message, "Send me an image, and I'll provide options for you!")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    '''Реагирует на изображения, отправляемые пользователем, и предлагает варианты обработки'''
    bot.reply_to(message, "I got your photo! Please choose what you'd like to do with it.",
                 reply_markup=get_options_keyboard())
    user_states[message.chat.id] = {'photo': message.photo[-1].file_id}


def get_options_keyboard():
    ''' Создает клавиатуру с опциями для обработки изображения'''
    keyboard = types.InlineKeyboardMarkup()
    pixelate_btn = types.InlineKeyboardButton("Pixelate", callback_data="pixelate")
    ascii_btn = types.InlineKeyboardButton("ASCII Art", callback_data="ascii")
    custom_chars_btn = types.InlineKeyboardButton("Custom Chars", callback_data="custom_chars")
    keyboard.add(pixelate_btn, ascii_btn, custom_chars_btn)
    return keyboard


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    '''Определяет действия в ответ на выбор пользователя и вызывает соответствующую функцию обработки'''
    if call.data == "pixelate":
        bot.answer_callback_query(call.id, "Pixelating your image...")
        pixelate_and_send(call.message)
    elif call.data == "ascii":
        bot.answer_callback_query(call.id, "Please enter your custom character set for ASCII art.")

        bot.send_message(call.message.chat.id,
                         "Please enter your custom character set for ASCII art. You can use up to 16 unique characters.",
                         reply_markup=types.ReplyKeyboardRemove())
        ascii_and_send(call.message)
    elif call.data == "custom_chars":
        bot.answer_callback_query(call.id, "Please enter your custom character set for ASCII art.")
        bot.register_next_step_handler(call.message, get_custom_chars)

def pixelate_and_send(message):
    '''Пикселизирует изображение и отправляет его пользователю'''
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)
    pixelated = pixelate_image(image, 20)

    output_stream = io.BytesIO()
    pixelated.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(message.chat.id, output_stream)


def ascii_and_send(message):
    '''Преобразует изображение в ASCII art и отправляет его пользователю'''
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    ascii_art = image_to_ascii(image_stream)
    bot.send_message(message.chat.id, f"```\n{ascii_art}\n```", parse_mode="MarkdownV2")

def get_custom_chars(message):
    '''Запрашивает у пользователя новый набор символов'''
    bot.reply_to(message, "Please enter your custom character set for ASCII art. You can use up to 16 unique characters.")
    bot.send_message(message.chat.id,
                     "Please enter your custom character set for ASCII art. You can use up to 16 unique characters.",
                     reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, process_custom_chars)


def process_custom_chars(message):
    '''Обрабатывает введенный пользователем набор символов'''
    custom_chars = message.text
    if len(custom_chars) > 16:
        bot.reply_to(message, "Please enter up to 16 unique characters.")
        return

    global ASCII_CHARS
    ASCII_CHARS = list(custom_chars)

    bot.reply_to(message, f"Your new character set: {ASCII_CHARS}")
    bot.send_message(message.chat.id, "I'll convert your image to ASCII art using this new set.",
                     reply_markup=get_options_keyboard())


bot.polling(none_stop=True)