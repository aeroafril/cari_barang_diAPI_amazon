from flask import Flask, render_template, request
from api.main import scrape_amazon

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    keyword = ""
    hasil = []

    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        if keyword:
            hasil = scrape_amazon(keyword)

    return render_template('index.html', hasil=hasil, keyword=keyword)

if __name__ == '__main__':
    app.run(debug=True)
