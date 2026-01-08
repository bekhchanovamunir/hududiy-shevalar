import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Excel faylni yuklash
try:
    df = pd.read_excel('sheva_lugat.xlsx')
    # Ustun nomlaridagi bo'shliqlarni olib tashlash
    df.columns = df.columns.str.strip()
    print("Excel fayl muvaffaqiyatli yuklandi!")
except Exception as e:
    print(f"Xato: {e}")
    df = pd.DataFrame()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    if not query or df.empty:
        return jsonify([])

    # Qidiruv logikasi: barcha ustunlar bo'ylab qidirish
    # Bu qism foydalanuvchi yozgan so'z qaysi ustunda bo'lishidan qat'i nazar topadi
    mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False, na=False).any(), axis=1)
    filtered_df = df[mask]

    results = []
    for _, row in filtered_df.iterrows():
        # Ma'lumotlarni lug'at ko'rinishida yuborish
        results.append(row.to_dict())
    
    return jsonify(results[:10]) # Dastlabki 10 ta natijani qaytarish

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
