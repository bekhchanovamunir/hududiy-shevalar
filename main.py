import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def load_data():
    try:
        # Excelni yuklash va barcha kataklarni matnga aylantirish
        data = pd.read_excel('sheva_lugat.xlsx')
        data.columns = data.columns.str.strip()
        # Bo'sh kataklarni bo'sh matn bilan to'ldirish
        data = data.fillna('')
        return data
    except Exception as e:
        print(f"Excel yuklashda xato: {e}")
        return pd.DataFrame()

df = load_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search():
    query = request.args.get('q', '').strip().lower()
    if not query or df.empty:
        return jsonify([])

    # Qidiruv: Har bir qatorda so'z borligini tekshirish
    results = []
    for _, row in df.iterrows():
        # Qatordagi barcha qiymatlarni bitta matnga birlashtirib qidirish
        row_content = " ".join(row.astype(str)).lower()
        if query in row_content:
            results.append(row.to_dict())
    
    return jsonify(results[:10])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
