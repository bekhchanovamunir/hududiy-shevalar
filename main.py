import pandas as pd
import asyncio
import threading
from flask import Flask, render_template, request, jsonify
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# --- 1. SOZLAMALAR ---
API_TOKEN = '8381607769:AAFyGBi_PGXOdGkZHcD50hFecpbgGxaSwhw'
WEB_APP_URL = "https://hududiy-shevalar.onrender.com"

app = Flask(__name__)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- 2. MA'LUMOTLARNI YUKLASH ---
try:
    df = pd.read_excel('sheva_lugat.xlsx')
    df.columns = df.columns.str.strip()
    df = df.fillna('')
    print("Excel muvaffaqiyatli yuklandi!")
except Exception as e:
    print(f"Excel xatosi: {e}")
    df = pd.DataFrame()

# --- 3. VEB-SAYT QISMI (FLASK) ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    if not query or df.empty:
        return jsonify([])
    results = []
    for _, row in df.iterrows():
        if query in " ".join(row.astype(str)).lower():
            results.append(row.to_dict())
    return jsonify(results[:10])

# --- 4. TELEGRAM BOT QISMI (AIOGRAM) ---
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🗺️ Xaritani ochish", web_app=WebAppInfo(url=WEB_APP_URL))]],
        resize_keyboard=True
    )
    await message.answer("Xush kelibsiz! Quyidagi tugma orqali xaritani oching:", reply_markup=markup)

async def run_bot():
    await dp.start_polling(bot)

# --- 5. IKKALASINI BIRGA ISHG'A TUSHIRISH ---
def start_bot_thread():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())

if __name__ == '__main__':
    # Botni alohida oqimda (thread) boshlash
    threading.Thread(target=start_bot_thread, daemon=True).start()
    # Veb-serverni asosiy oqimda boshlash
    app.run(host='0.0.0.0', port=10000)
