import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# 🔍 Расшифровка panic-лога
def diagnose_from_panic(text: str) -> str:
    text = text.lower()
    conclusions = []

    if "audio-codec" in text or "audiocodec" in text:
        conclusions.append(
            "1) Нарушение работы аудио кодека\n"
            "Проверьте работу микрофонов через диктофон:\n"
            "- Если кнопка записи не нажимается — проблема в самом аудио кодеке\n"
            "- Если нажимается, но нет звука — проблема в периферии (микрофоны, шлейфы)"
        )

    if "iap" in text or "portmicro" in text or "hydra" in text or "lightning" in text:
        conclusions.append(
            "2) Нарушение работы контроллера Lightning\n"
            "- Возможный дефект: контроллер Hydra\n"
            "- Также проверьте нижний системный шлейф"
        )

    if "baseband" in text:
        conclusions.append(
            "3) Обнаружены проблемы с модемом (Baseband)\n"
            "- Возможные причины: неисправность модема, модемного питания или контроллера питания"
        )

    if "smc-charger" in text:
        conclusions.append(
            "4) Нарушение работы зарядного контроллера (smc-charger)\n"
            "- Проверьте цепи питания и зарядки устройства"
        )

    if not conclusions:
        conclusions.append("Не удалось поставить диагноз: неизвестный тип сбоя.")

    return "\n\n".join(conclusions)


# 📨 Обработка присланного файла
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if not document:
        return

    file = await context.bot.get_file(document.file_id)
    file_path = f"/tmp/{document.file_name}"
    await file.download_to_drive(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        await update.message.reply_text(f"Ошибка при чтении файла: {str(e)}")
        return
    finally:
        os.remove(file_path)

    diagnosis = diagnose_from_panic(content)
    await update.message.reply_text(f"Обнаружен iOS PANIC-лог:\n\n{diagnosis}")


# 🚀 Запуск Telegram-бота
def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        print("❌ Ошибка: переменная окружения TELEGRAM_BOT_TOKEN не задана.")
        return

    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(
        filters.Document.FILE_EXTENSION("ips") | filters.Document.FILE_EXTENSION("txt"),
        handle_file
    ))

    print("✅ Бот успешно запущен.")
    app.run_polling()


if __name__ == "__main__":
    main()
