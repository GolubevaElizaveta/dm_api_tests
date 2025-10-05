from pathlib import Path
from telebot import TeleBot
from vyper import v

# Установка пути к конфигурации
config = Path(__file__).parent.parent.parent.joinpath('config')
v.set_config_name("prod")
v.add_config_path(config)
v.read_in_config()


def send_file() -> None:
    telegram_bot = TeleBot(v.get("telegram.token"))

    # Путь к файлу в корне проекта
    file_path = Path(__file__).parent.parent.parent.joinpath("swagger-coverage-dm-api-account.html")

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path.resolve()}")

    with open(file_path, 'rb') as document:
        telegram_bot.send_document(
            v.get("telegram.chat_id"),
            document=document,
            caption="coverage",
        )


if __name__ == '__main__':
    send_file()