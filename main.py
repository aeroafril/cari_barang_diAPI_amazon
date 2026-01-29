from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import json

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
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1'
                }
                
                # URL Tokopedia search
                url = f'https://www.tokopedia.com/search?q={keyword.replace(" ", "%20")}'
                
                response = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Scraping produk Tokopedia
                # Tokopedia menggunakan dynamic content, jadi kita coba ambil dari script tag
                script_tags = soup.find_all('script', type='application/ld+json')
                
                for script in script_tags:
                    try:
                        data = json.loads(script.string)
                        
                        if isinstance(data, dict) and 'itemListElement' in data:
                            for item in data['itemListElement'][:10]:
                                if 'item' in item:
                                    product = item['item']
                                    nama = product.get('name', 'N/A')
                                    harga_raw = product.get('offers', {}).get('price', 'N/A')
                                    
                                    # Format harga
                                    if harga_raw != 'N/A':
                                        try:
                                            harga = f"Rp {int(float(harga_raw)):,}".replace(',', '.')
                                        except:
                                            harga = f"Rp {harga_raw}"
                                    else:
                                        harga = 'N/A'
                                    
                                    hasil.append({
                                        'nama': nama,
                                        'harga': harga
                                    })
                    except:
                        continue
                
                # Jika JSON-LD tidak berhasil, coba scraping HTML biasa
                if not hasil:
                    # Coba beberapa selector yang mungkin dipakai Tokopedia
                    products = soup.find_all('div', attrs={'data-testid': 'divSRPContentProducts'})
                    
                    if not products:
                        products = soup.select('div[class*="css-"]')[:20]
                    
                    for product in products[:10]:
                        try:
                            # Cari nama produk
                            nama_elem = product.find('span', attrs={'data-testid': 'spnSRPProdName'})
                            if not nama_elem:
                                nama_elem = product.find('span', class_='css-20kt3o')
                            if not nama_elem:
                                nama_elem = product.find('div', class_='css-1bjwylw')
                            
                            # Cari harga
                            harga_elem = product.find('div', attrs={'data-testid': 'spnSRPProdPrice'})
                            if not harga_elem:
                                harga_elem = product.find('div', class_='css-o5uqvq')
                            if not harga_elem:
                                harga_elem = product.find('span', class_='css-o5uqvq')
                            
                            if nama_elem and harga_elem:
                                hasil.append({
                                    'nama': nama_elem.get_text(strip=True),
                                    'harga': harga_elem.get_text(strip=True)
                                })
                        except:
                            continue
                        
            except Exception as e:
                print(f"Error: {e}")
    
    return render_template('index.html', keyword=keyword, hasil=hasil)

# Untuk Vercel
if __name__ == '__main__':
    app.run(debug=True)
