import pandas as pd
import asyncio
import threading
import json
import os
from flask import Flask, render_template, request, jsonify
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# --- SOZLAMALAR ---
API_TOKEN = '8381607769:AAFyGBi_PGXOdGkZHcD50hFecpbgGxaSwhw'
WEB_APP_URL = "https://hududiy-shevalar.onrender.com"

app = Flask(__name__)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# --- MA'LUMOTLARNI YUKLASH ---
def load_data():
    try:
        # Excelni yuklash va ustunlardagi ortiqcha bo'shliqlarni olib tashlash
        df = pd.read_excel('sheva_lugat.xlsx')
        df.columns = df.columns.str.strip()
        return df.fillna('')
    except Exception as e:
        print(f"Xato: {e}")
        return pd.DataFrame()

df = load_data()

# --- VEB-SAYT YO'LLARI ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_map')
def get_map():
    file_path = 'uzbekistan_regional.geojson'
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return jsonify(json.load(f))
    return jsonify({"type": "FeatureCollection", "features": []})

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    word = data.get('word', '').strip().lower()
    
    if not word or df.empty:
        return jsonify({"found": False})

    for _, row in df.iterrows():
        # Qatordagi barcha matnlarni birlashtirib qidirish
        row_str = " ".join(row.astype(str)).lower()
        if word in row_str:
            return jsonify({
                "found": True,
                "data": {
                    # SIZNING JADVALINGIZDAGI USTUN NOMLARI BILAN MOSLASHTIRILDI
                    "adabiy": row.get('Adabiy shakl', 'Topilmadi'),
                    "dialects": {
                        "andijon": row.get('Andijon(qarluq)', ''),
                        "buxoro": row.get('Buxoro(qipchoq)', ''),
                        "qashqadaryo": row.get('Qashqadaryo(qipchoq)', ''),
                        "samarqand": row.get('Samarqand(qipchoq)', ''),
                        "xorazm": row.get('Xorazm(o\'g\'uz)', '')
                    }
                }
            })
    return jsonify({"found": False})

# --- BOT QISMI ---
@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    markup = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🗺️ Xaritani ochish", web_app=WebAppInfo(url=WEB_APP_URL))]],
        resize_keyboard=True
    )
    await message.answer("Xush kelibsiz! Xarita orqali shevalarni izlab ko'ring:", reply_markup=markup)

async def run_bot():
    await dp.start_polling(bot)

if __name__ == '__main__':
    threading.Thread(target=lambda: asyncio.run(run_bot()), daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
