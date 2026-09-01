import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)
import google.generativeai as genai

# ==================== CONFIGURATION ====================
TELEGRAM_TOKEN = "8757060796:AAFHI9W_fDCvvlijxoP8yPLN80UPzJ5ASGo"
GEMINI_API_KEY = "AIzaSyBcDqoV9snAOoYT3lREODBs14YW8iYTElw"

# Gemini AI কনফিগারেশন
genai.configure(api_key=GEMINI_API_KEY)

# স্মার্ট, ফ্রেন্ডলি ও অল-রাউন্ডার AI পার্সোনালিটি
system_instruction = (
    "You are an elite, highly intelligent, and friendly AI assistant. "
    "You excel at software development, full-stack coding, creative writing, "
    "problem solving, and conversational fun. "
    "You understand and reply in ANY language (Bengali, English, Hindi, etc.) fluently based on user preference. "
    "Be direct, humorous, witty, and highly helpful without giving artificial refusals."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=system_instruction
)

# ইউজার চ্যাট সেশন স্টোর করার ডিকশনারি
user_chats = {}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_chats[chat_id] = model.start_chat(history=[])
    
    welcome_text = (
        "🔥 **হাই! আমি আপনার পার্সোনাল সুপার AI অ্যাসিস্ট্যান্ট!**\n\n"
        "যেকোনো ভাষার প্রশ্ন, কোডিং প্রজেক্ট, স্ক্রিপ্ট, আইডিয়া বা ফান করার জন্য যা খুশি জিজ্ঞেস করতে পারেন।"
    )
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_text = update.message.text

    if chat_id not in user_chats:
        user_chats[chat_id] = model.start_chat(history=[])

    try:
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        
        response = user_chats[chat_id].send_message(user_text)
        answer = response.text
        
        if len(answer) > 4000:
            for i in range(0, len(answer), 4000):
                await context.bot.send_message(chat_id=chat_id, text=answer[i:i+4000])
        else:
            await update.message.reply_text(answer)

    except Exception as e:
        await update.message.reply_text(f"⚠️ একটি সমস্যা হয়েছে: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    print("🚀 Bot started successfully!")
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
