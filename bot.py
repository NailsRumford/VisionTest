import logging
import requests
import io
import json
from telegram import __version__ as TG_VER
try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram.ext import Application, MessageHandler, filters
from core import settings
import io
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)



async def process_text(update, context):
    # обработка текстовых сообщений пользователя
    await update.message.reply_text('Пришлите фото документа')
    
async def process_photo(update, context):
    # Получение объекта фотографии
    photo = update.message.photo[-1]  # Берем последнюю (наибольшую) фотографию


    photo_file = await photo.get_file()
    f = io.BytesIO()
    await photo_file.download_to_memory(out=f)
    f.seek(0)
 
    url = 'https://smarty.mail.ru/api/v1/docs/recognize'
    oauth_token = '2FuE889wC4i3kPCMuFceU72njrL3ixR6bCStZUfkQzFcuZSmcw'
    # Имя файла для передачи в поле 'file'
    file_name = 'file.jpg'
    meta = {
        "images": [
            {
                "name": "file"
            }
        ]
    }
    files = {
        'file': (file_name, f, 'image/jpeg')
    }
    params = {
        'oauth_token': oauth_token,
        'oauth_provider': 'mcs'
    }
    headers = {
        'Accept': 'application/json'
    }
    
    # Отправка запроса
    response = requests.post(url, files=files, data={'meta': json.dumps(meta)}, headers=headers, params=params)
    response_json = response.json()

# Преобразование JSON в удобочитаемый формат
    formatted_response = json.dumps(response_json, indent=4, ensure_ascii=False)

# Отправка отформатированного ответа в сообщении Telegram
    await update.message.reply_text(formatted_response)





def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(settings.TELEGRAM_TOKEN).build()
    application.add_handler(MessageHandler(
                filters.TEXT & ~filters.COMMAND, process_text))
    application.add_handler(MessageHandler(filters.PHOTO, process_photo ))
    application.run_polling()


if __name__ == "__main__":
    main()
