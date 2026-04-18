import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Get token from Railway environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Only respond to TikTok links
    if "tiktok.com" in text:
        await update.message.reply_text("Downloading...")

        try:
            api_url = f"https://tikwm.com/api/?url={text}"
            res = requests.get(api_url).json()

            # Try to get video (no watermark first)
            video_url = res["data"].get("play")

            # Fallback if not available
            if not video_url:
                video_url = res["data"].get("wmplay")

            if video_url:
                await update.message.reply_video(video_url)
            else:
                await update.message.reply_text("❌ Could not find video.")

        except Exception as e:
            print(e)
            await update.message.reply_text("❌ Failed to download.")

# Build bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Listen to messages
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

print("Bot is running...")

# Run bot (works on Railway)
import asyncio
asyncio.run(app.run_polling())
