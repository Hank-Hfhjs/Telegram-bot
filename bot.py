import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is missing!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text

        if "tiktok.com" in text:
            await update.message.reply_text("Downloading...")

            api_url = f"https://tikwm.com/api/?url={text}"
            res = requests.get(api_url).json()

            video_url = res["data"].get("play") or res["data"].get("wmplay")

            if video_url:
                await update.message.reply_video(video_url)
            else:
                await update.message.reply_text("❌ No video found.")

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text("❌ Something went wrong.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

print("Bot is running...")

import asyncio
asyncio.run(app.run_polling())
