# Amazon Product Search - Flask App

Aplikasi web untuk mencari produk di Amazon dengan tampilan monokrom yang elegan.

## Struktur Project

```
cari_barang_diAPI_amazon/
├── app.py              # Main Flask application
├── vercel.json         # Vercel configuration
├── requirements.txt    # Python dependencies
├── templates/
│   └── index.html     # HTML template
└── .gitignore         # Git ignore file
```

## Cara Deploy ke Vercel

1. Push semua file ke GitHub repository Anda
2. Import repository di Vercel
3. Vercel akan otomatis mendeteksi Flask framework
4. Klik "Deploy"

## File Penting

- **vercel.json**: Konfigurasi untuk Vercel deployment
- **requirements.txt**: Daftar dependencies Python
- **app.py**: Main application file
- **templates/index.html**: Template HTML dengan design monokrom

## Dependencies

- Flask 3.0.0
- requests 2.31.0
- beautifulsoup4 4.12.2
- lxml 4.9.3

## Fitur

- 🔍 Search produk Amazon
- 🎨 UI Monokrom yang modern
- 📱 Responsive design
- ⚡ Fast loading

## Local Development

```bash
pip install -r requirements.txt
python app.py
```

Buka browser di `http://localhost:5000`
