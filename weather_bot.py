import subprocess
import telebot
import speech_recognition as sr
import message_responce

token = open("resources/API_KEY").read()
bot = telebot.TeleBot(token)


def ogg2wav(old_filename: str, new_filename: str) -> bool:
    """ Converts .ogg file to .wav"""
    converter = 'temp//ffmpeg.exe'
    process = subprocess.run([converter, '-y', '-i', old_filename, new_filename])
    return process.returncode == 0


@bot.message_handler(content_types=['voice', 'audio'])
def get_audio_messages(message):
    """Receives voice from user and converts it to text"""
    file_info = bot.get_file(message.voice.file_id)
    # Voice file downloading
    content = bot.download_file(file_info.file_path)
    old_file, new_file = 'temp//user_voice.ogg', 'temp//user_voice.wav'

    # Voice file saving into .ogg file
    with open(old_file, 'wb') as file:
        file.write(content)

    ogg2wav(old_file, new_file)

    with sr.WavFile(new_file) as source:
        recognizer = sr.Recognizer()
        audio = recognizer.record(source)

        try:
            # We use google services to recognize audio
            text = recognizer.recognize_google(audio, language="ru")
            bot.send_message(message.from_user.id, text)

            message.text = text
            get_text_messages(message)
        except sr.UnknownValueError:
            bot.send_message(message.from_user.id, "Не удалось распознать ваш голос, попробуйте говорить четче.")


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f'Привет, я - погодный бот. Приятно познакомиться, {message.from_user.first_name}')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    """Answer to user`s message"""
    answer = message_responce.answer(message.text)

    # Sends each message
    for ans in answer:
        bot.send_message(message.from_user.id, ans)


bot.polling(none_stop=True)
