import json
from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

# Fayllarni yuklash
excel_path = 'sheva_lugat.xlsx'
df = pd.read_excel(excel_path)
df.columns = df.columns.str.strip()

# Siz yuklagan GeoJSON faylni o'qish
with open('uzbekistan_regional.geojson', encoding='utf-8') as f:
    geojson_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_map')
def get_map():
    return jsonify(geojson_data)

@app.route('/search', methods=['POST'])
def search():
    word = request.json.get('word', '').strip()
    match = df[df['Adabiy shakl'].astype(str).str.contains(word, case=False, na=False)]
    
    if match.empty:
        return jsonify({'found': False})

    row = match.iloc[0]
    return jsonify({
        'found': True,
        'data': {
            'adabiy': row['Adabiy shakl'],
            'dialects': {
                'andijon': str(row.get("Andijon(qarluq)", "")),
                'buxoro': str(row.get("Buxoro(qipchoq)", "")),
                'qashqadaryo': str(row.get("Qashqadaryo(qipchoq)", "")),
                'samarqand': str(row.get("Samarqand(qipchoq)", "")),
                'xorazm': str(row.get("Xorazm(o'g'uz)", ""))
            }
        }
    })

if __name__ == '__main__':
    app.run(debug=True)