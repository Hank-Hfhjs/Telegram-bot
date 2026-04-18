import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8662743970:AAFHCsLcJ8LfGhsacRtYMoGt13Ix_H0YS6M"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "tiktok.com" in text:
        await update.message.reply_text("Downloading...")

        try:
            api_url = f"https://tikwm.com/api/?url={text}"
            res = requests.get(api_url).json()

            video_url = res["data"]["play"]

            await update.message.reply_video(video_url)

        except:
            await update.message.reply_text("❌ Failed to download.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

print("Bot is running...")
import asyncio
asyncio.run(app.run_polling())