from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    keyword = ''
    hasil = []
    
    if request.method == 'POST':
        keyword = request.form.get('keyword', '')
        
        if keyword:
            try:
                # Header untuk bypass blocking
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                }
                
                # URL Amazon search
                url = f'https://www.amazon.com/s?k={keyword.replace(" ", "+")}'
                
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Scraping produk Amazon
                products = soup.find_all('div', {'data-component-type': 's-search-result'})
                
                for product in products[:10]:  # Ambil 10 produk pertama
                    try:
                        nama = product.find('h2', class_='a-size-mini').text.strip()
                        harga_elem = product.find('span', class_='a-price-whole')
                        
                        if harga_elem:
                            harga = f"${harga_elem.text.strip()}"
                        else:
                            harga = "N/A"
                        
                        hasil.append({
                            'nama': nama,
                            'harga': harga
                        })
                    except:
                        continue
                        
            except Exception as e:
                print(f"Error: {e}")
    
    return render_template('index.html', keyword=keyword, hasil=hasil)

# Untuk Vercel
if __name__ == '__main__':
    app.run(debug=True)
