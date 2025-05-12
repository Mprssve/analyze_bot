import os
import re
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters
)

# Парсер panic-логов
def parse_panic_log(text: str) -> str:
    output = []

    if "panic" in text.lower():
        timestamp = re.search(r'timestamp\s*:\s*(.+)', text)
        panic_string = re.search(r'panicString\s*:\s*(.+)', text)
        version = re.search(r'OS Version:\s*(.+)', text) or re.search(r'os_version\s*:\s*(.+)', text)
        bug_type = re.search(r'bug_type\s*:\s*(\d+)', text)

        output.append("Обнаружен **iOS PANIC-лог**:")
        if timestamp:
            output.append(f"- Время сбоя: {timestamp.group(1)}")
        if version:
            output.append(f"- Версия iOS: {version.group(1)}")
        if panic_string:
            output.append(f"- Причина сбоя: {panic_string.group(1)}")
        if bug_type:
            output.append(f"- Тип ошибки: {bug_type.group(1)}")

        return "\n".join(output)
    else:
        return "Файл не содержит panic-лога или имеет неизвестный формат."

# Обработка команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот для анализа iOS panic-логов.\n"
        "Отправь мне файл .ips или .txt, и я покажу расшифровку."
    )

# Обработка полученного файла
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    if not document:
        await update.message.reply_text("Пожалуйста, отправьте файл .ips или .txt.")
        return

    filename = document.file_name.lower()
    if not (filename.endswith(".ips") or filename.endswith(".txt")):
        await update.message.reply_text("Файл должен быть с расширением .ips или .txt.")
        return

    telegram_file = await document.get_file()
    file_bytes = await telegram_file.download_as_bytearray()
    text = file_bytes.decode("utf-8", errors="ignore")

    result = parse_panic_log(text)
    await update.message.reply_text(result)

# Точка входа
def main():
    token = os.getenv("7150429783:AAG_t8pbChxSEK008aCoGmvyHpjDcUQ84qk")
    if not token:
        print("Ошибка: переменная окружения TELEGRAM_BOT_TOKEN не задана.")
        return

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()