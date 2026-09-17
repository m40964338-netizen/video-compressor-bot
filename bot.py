import os
import subprocess
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters

TOKEN = os.environ["BOT_TOKEN"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎬 سلام! ویدیو رو بفرست تا حجمش رو کاهش بدم."
    )

async def compress_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if not message.video:
        return

    await message.reply_text("⏳ ویدیو دریافت شد؛ در حال کاهش حجم...")

    file = await context.bot.get_file(message.video.file_id)

    input_file = f"/tmp/{message.video.file_unique_id}.mp4"
    output_file = f"/tmp/compressed_{message.video.file_unique_id}.mp4"

    await file.download_to_drive(input_file)

    subprocess.run([
        "ffmpeg",
        "-i", input_file,
        "-vcodec", "libx264",
        "-crf", "28",
        "-preset", "fast",
        "-acodec", "aac",
        "-b:a", "96k",
        output_file,
        "-y"
    ], check=True)

    with open(output_file, "rb") as video:
        await message.reply_video(video)

    os.remove(input_file)
    os.remove(output_file)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, compress_video))

    app.run_polling()

if __name__ == "__main__":
    main()
