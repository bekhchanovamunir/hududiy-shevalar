import logging
import asyncio
import pandas as pd
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

# 1. API Tokeningiz
API_TOKEN = '8381607769:AAFyGBi_PGXOdGkZHCd50hFecpbggxaSwhw'

# 2. Excel faylni yuklash
try:
    df = pd.read_excel('sheva_lugat.xlsx')
    df.columns = df.columns.str.strip()
    print("Excel fayl muvaffaqiyatli yuklandi!")
except Exception as e:
    print(f"Excelni yuklashda xato: {e}")

# Bot va Dispatcher sozlamalari
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    # BU YERGA Render'dan olgan sayt manzilingizni qo'ying
    # Hozircha test uchun o'z saytingiz linkini yozib turing
    web_app_url = "https://hududiy-shevalar.onrender.com" 
    
    markup = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🗺️ Xaritani ochish", web_app=WebAppInfo(url=web_app_url))]
        ],
        resize_keyboard=True
    )
    
    await message.reply(
        "Assalomu alaykum! 🇺🇿\nSheva lug'ati botiga xush kelibsiz.\n\n"
        "So'z yuboring yoki pastdagi tugma orqali xaritani oching!",
        reply_markup=markup
    )

@dp.message()
async def search_word(message: types.Message):
    if not message.text:
        return
        
    word = message.text.strip()
    # Exceldan qidirish
    match = df[df['Adabiy shakl'].astype(str).str.contains(word, case=False, na=False)]
    
    if match.empty:
        await message.answer("⚠️ Kechirasiz, bu so'z lug'atdan topilmadi.")
        return

    row = match.iloc[0]
    
    # Ma'lumotlarni xavfsiz o'zgaruvchilarga olamiz (SyntaxError oldini olish uchun)
    adabiy = str(row.get('Adabiy shakl', '---'))
    andijon = str(row.get('Andijon(qarluq)', '---'))
    buxoro = str(row.get('Buxoro(qipchoq)', '---'))
    qashqa = str(row.get('Qashqadaryo(qipchoq)', '---'))
    samarqand = str(row.get('Samarqand(qipchoq)', '---'))
    xorazm = str(row.get("Xorazm(o'g'uz)", '---'))

    # Matnni yig'ish
    res = f"✅ <b>Adabiy shakli:</b> {adabiy}\n"
    res += "━━━━━━━━━━━━━━\n"
    res += f"🔸 Andijon: {andijon}\n"
    res += f"🔹 Buxoro: {buxoro}\n"
    res += f"🔸 Qashqadaryo: {qashqa}\n"
    res += f"🔹 Samarqand: {samarqand}\n"
    res += f"🔸 Xorazm: {xorazm}\n"
    res += "━━━━━━━━━━━━━━"
    
    await message.answer(res, parse_mode="HTML")

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):

        print("Bot to'xtatildi")
